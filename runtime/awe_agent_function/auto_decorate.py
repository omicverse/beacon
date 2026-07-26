"""Walk a foreign Python package and synthesise registry entries for
every public function / class without modifying the package's source.

This is what lets A3F apply to packages that have not adopted the
decorator at the call site (sklearn, scipy, numpy, …). The synthesised
entries inherit defaults that score lower on the AFS rubric (because
the metadata is heuristic rather than authored), but they are
queryable and let an agent discover the package's public surface.
"""

from __future__ import annotations

import importlib
import inspect
import re
from types import ModuleType
from typing import Any, Iterable, List, Optional, Sequence, Set, Tuple

from .registry import get_registry


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


_CAMEL_SPLIT = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")


def _split_identifier(name: str) -> List[str]:
    """Split snake_case + camelCase + dotted names into lower-case tokens."""

    parts: List[str] = []
    for chunk in re.split(r"[._\-]+", name or ""):
        if not chunk:
            continue
        for sub in _CAMEL_SPLIT.split(chunk):
            if sub:
                parts.append(sub.lower())
    # de-duplicate, keep order
    seen: set = set()
    out: List[str] = []
    for p in parts:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def _first_sentence(text: str, max_chars: int = 240) -> str:
    """Return the first sentence of a docstring, capped at max_chars."""

    if not text:
        return ""
    text = inspect.cleandoc(text)
    # First paragraph
    para = text.split("\n\n", 1)[0].replace("\n", " ").strip()
    # First sentence
    m = re.search(r"^(.{20,}?[.!?])(\s|$)", para)
    s = (m.group(1) if m else para).strip()
    return s[: max_chars - 1] + ("…" if len(s) > max_chars else "")


_EXAMPLE_HEADER = re.compile(r"^\s*Examples?\s*\n[-=]{3,}\s*", re.MULTILINE)
_SEEALSO_HEADER = re.compile(r"^\s*See Also\s*\n[-=]{3,}\s*", re.MULTILINE)


def _extract_examples(doc: str, max_examples: int = 2) -> List[str]:
    """Pull at most max_examples short example lines from a numpy-style
    docstring's "Examples" section."""

    if not doc:
        return []
    m = _EXAMPLE_HEADER.search(doc)
    if not m:
        return []
    body = doc[m.end():]
    # Stop at the next section header (a line of ----).
    stop = re.search(r"\n[A-Za-z][^\n]{0,60}\n[-=]{3,}\s*", body)
    section = body[: stop.start()] if stop else body
    lines = [l.rstrip() for l in section.splitlines()
             if l.strip() and not l.lstrip().startswith(">>>")]  # raw-text examples
    # Prefer literal example calls ('>>> foo(...)') as cleaner snippets.
    snippets = re.findall(r">>>\s*(.+?)(?=\n>>>|\n\s*\n|\Z)", section, re.DOTALL)
    snippets = [s.strip().splitlines()[0] for s in snippets if s.strip()]
    if snippets:
        return snippets[:max_examples]
    return [l.strip() for l in lines[:max_examples] if l.strip()]


def _extract_see_also(doc: str, max_items: int = 5) -> List[str]:
    """Pull up to max_items names from a numpy-style 'See Also' section."""

    if not doc:
        return []
    m = _SEEALSO_HEADER.search(doc)
    if not m:
        return []
    body = doc[m.end():]
    stop = re.search(r"\n[A-Za-z][^\n]{0,60}\n[-=]{3,}\s*", body)
    section = body[: stop.start()] if stop else body
    names: List[str] = []
    for line in section.splitlines():
        m2 = re.match(r"^\s*([A-Za-z0-9_.]+)\s*[:|,]?", line)
        if m2:
            names.append(m2.group(1))
        if len(names) >= max_items:
            break
    return names


def _category_from_module(modname: str, root: str) -> str:
    """Map dotted module path to a coarse category."""

    parts = modname.split(".")
    if parts[0] != root:
        return "external"
    if len(parts) <= 1:
        return root
    return f"{root}.{parts[1]}"


def _is_public(name: str) -> bool:
    return bool(name) and not name.startswith("_")


def _walk_module(
    mod: ModuleType,
    root: str,
    *,
    seen: Set[int],
    max_depth: int,
    depth: int = 0,
) -> Iterable[Tuple[ModuleType, str, Any]]:
    """Yield (module, attr_name, attr) for public callables / classes
    rooted at `mod`, up to max_depth submodule levels."""

    if id(mod) in seen:
        return
    seen.add(id(mod))

    public = getattr(mod, "__all__", None)
    candidates = list(public) if public else [n for n in dir(mod) if _is_public(n)]

    for name in candidates:
        try:
            obj = getattr(mod, name)
        except Exception:
            continue
        if obj is None:
            continue
        # submodule recursion
        if (inspect.ismodule(obj)
                and depth < max_depth
                and getattr(obj, "__name__", "").startswith(root)):
            yield from _walk_module(obj, root, seen=seen,
                                     max_depth=max_depth, depth=depth + 1)
            continue
        # public callable / class
        if (inspect.isfunction(obj) or inspect.isclass(obj)
                or inspect.isbuiltin(obj)):
            # Only register objects defined in `root.*` to avoid
            # re-exposing third-party imports.
            obj_mod = getattr(obj, "__module__", "") or ""
            if obj_mod.startswith(root):
                yield mod, name, obj


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def auto_decorate(
    package: str,
    *,
    recurse_depth: int = 2,
    skip_classes: bool = False,
    contract_keys: Optional[set] = None,
    extra_aliases_from: Optional[Sequence[str]] = ("examples", "see_also"),
) -> int:
    """Walk `package`'s public surface and register every public callable.

    Returns the number of entries registered.

    Parameters
    ----------
    package : str
        Top-level dotted name of the package to scan (e.g. "sklearn").
    recurse_depth : int
        Submodule depth. Depth 0 → only `package.__init__`; depth 2 →
        `package.subpkg.module`.
    skip_classes : bool
        If True, only register functions (skip classes). Some libraries
        bundle their public API as classes (sklearn) — usually False.
    contract_keys : optional set[str]
        Override the default contract-key allowlist (e.g. drop the
        AnnData-flavoured keys when registering a non-omics library).
    extra_aliases_from : sequence
        Where to harvest extra alias tokens from. Defaults pull from
        the docstring's "Examples" and "See Also" sections.
    """

    pkg = importlib.import_module(package)
    seen: Set[int] = set()
    n_registered = 0

    for parent, name, obj in _walk_module(pkg, package,
                                           seen=seen,
                                           max_depth=recurse_depth):
        if skip_classes and inspect.isclass(obj):
            continue

        full_name = f"{getattr(obj, '__module__', '')}.{getattr(obj, '__name__', name)}"
        if get_registry()._registry.get(full_name.lower()):
            continue   # already registered

        doc = inspect.getdoc(obj) or ""
        description = _first_sentence(doc) or f"Auto-registered {name} from {package}."
        aliases: List[str] = list(dict.fromkeys(
            _split_identifier(name)
            + [name]
            + ([] if not parent else [f"{parent.__name__.split('.')[-1]} {name}"])
        ))
        if "see_also" in extra_aliases_from:
            for s in _extract_see_also(doc, max_items=3):
                if s and s not in aliases:
                    aliases.append(s)
        category = _category_from_module(getattr(obj, "__module__", "") or package,
                                         package)

        examples = _extract_examples(doc, max_examples=2)
        related = _extract_see_also(doc, max_items=5)

        try:
            get_registry().register(
                obj,
                aliases=aliases or [name],
                category=category,
                description=description,
                examples=examples,
                related=related,
                contract_keys=contract_keys,
            )
            n_registered += 1
        except Exception:
            # Defensive: an inscrutable signature should not break the scan.
            continue

    return n_registered
