"""Library-agnostic FunctionRegistry: an in-memory, searchable index of
decorated functions plus a difflib + token-overlap scorer.

Adapted from the omicverse _registry.py, with all AnnData-specific
container-key validation replaced by a generic "valid contract keys"
allowlist that the decorator caller can override.
"""

from __future__ import annotations

import inspect
import re
import warnings
from difflib import get_close_matches
from typing import Any, Callable, Dict, List, Optional, Tuple


# Default contract-key allowlist. Domain libraries can override via
# `register_function(... requires_key_set=..., produces_key_set=...)`.
DEFAULT_CONTRACT_KEYS: set[str] = {
    "shape",        # generic input shape ("2d_array", "graph", ...)
    "attributes",   # attributes the function sets / reads on the object
    "files",        # files written / consumed
    "metrics",      # metrics emitted to logs / returned
    "fields",       # generic dict / dataclass fields
    # AnnData-flavoured keys retained for back-compat with omicverse:
    "layers", "obsm", "obsp", "uns", "var", "obs", "varm",
}


class FunctionRegistry:
    """Process-global registry of decorated functions.

    The internal dict maps every alias (and the short name, and the full
    dotted name) to the same canonical entry, so that any of those
    queries returns the same record in O(1). Categories are kept in a
    parallel `category -> [full_name, ...]` index for category browsing.
    """

    def __init__(self) -> None:
        self._registry: Dict[str, Dict[str, Any]] = {}
        self._function_map: Dict[Callable, str] = {}
        self._categories: Dict[str, List[str]] = {}

    # ---- registration ------------------------------------------------

    def _store_entry(
        self,
        entry: Dict[str, Any],
        *,
        register_short_name: bool = True,
        override_aliases: bool = True,
        map_function: Optional[Callable] = None,
    ) -> None:
        full_name = str(entry.get("full_name") or "").lower()
        short_name = str(entry.get("short_name") or "").lower()
        aliases = [str(a).strip().lower()
                   for a in (entry.get("aliases") or [])
                   if str(a).strip()]

        def _maybe_store(key: str) -> None:
            if not key:
                return
            if override_aliases or key not in self._registry:
                self._registry[key] = entry

        for a in aliases:
            _maybe_store(a)
        if register_short_name:
            _maybe_store(short_name)
        if full_name:
            self._registry[full_name] = entry

        cat = str(entry.get("category") or "")
        fn_name = str(entry.get("full_name") or "")
        if cat and fn_name:
            self._categories.setdefault(cat, [])
            if fn_name not in self._categories[cat]:
                self._categories[cat].append(fn_name)

        if map_function is not None and not entry.get("virtual_entry"):
            self._function_map[map_function] = entry.get("full_name", "")

    def register(
        self,
        func: Callable,
        *,
        aliases: List[str],
        category: str,
        description: str,
        examples: Optional[List[str]] = None,
        related: Optional[List[str]] = None,
        prerequisites: Optional[Dict[str, List[str]]] = None,
        requires: Optional[Dict[str, List[str]]] = None,
        produces: Optional[Dict[str, List[str]]] = None,
        auto_fix: str = "none",
        contract_keys: Optional[set] = None,
    ) -> Callable:
        """Validate metadata and store one entry."""

        if not aliases or not all(str(a).strip() for a in aliases):
            raise ValueError("Function registration requires ≥ 1 non-empty alias.")
        if not category or not category.strip():
            raise ValueError("Function registration requires a category.")
        if not description or not description.strip():
            raise ValueError("Function registration requires a description.")
        if auto_fix not in ("auto", "escalate", "none"):
            raise ValueError(
                f"Invalid auto_fix={auto_fix!r}. Must be 'auto', 'escalate' or 'none'."
            )

        valid_keys = contract_keys or DEFAULT_CONTRACT_KEYS

        if prerequisites is not None:
            if not isinstance(prerequisites, dict):
                raise TypeError("prerequisites must be a dict")
            for k in prerequisites:
                if k not in {"functions", "optional_functions"}:
                    raise ValueError(
                        f"Invalid prerequisites key {k!r} "
                        "(only 'functions', 'optional_functions')")
        for kind, m in [("requires", requires), ("produces", produces)]:
            if m is None:
                continue
            if not isinstance(m, dict):
                raise TypeError(f"{kind} must be a dict")
            for k in m:
                if k not in valid_keys:
                    raise ValueError(
                        f"Invalid {kind} key {k!r}; allowed: {sorted(valid_keys)}")

        try:
            sig = inspect.signature(func)
            params: List[str] = []
            for name, p in sig.parameters.items():
                s = name
                if p.default is not inspect.Parameter.empty:
                    s += f"={p.default!r}"
                params.append(s)
            signature = str(sig)
        except (ValueError, TypeError):
            signature = "(…)"
            params = []

        docstring = inspect.getdoc(func) or ""

        full_name = f"{getattr(func, '__module__', '')}.{getattr(func, '__name__', '?')}"
        short_name = getattr(func, "__name__", "?")

        entry = {
            "function":        func,
            "full_name":       full_name,
            "short_name":      short_name,
            "module":          getattr(func, "__module__", ""),
            "aliases":         list(aliases),
            "category":        category,
            "description":     description,
            "examples":        list(examples or []),
            "related":         list(related or []),
            "signature":       signature,
            "parameters":      params,
            "docstring":       docstring,
            "prerequisites":   prerequisites or {},
            "requires":        requires or {},
            "produces":        produces or {},
            "auto_fix":        auto_fix,
            "virtual_entry":   False,
            "source":          "runtime",
        }
        self._store_entry(entry, map_function=func)
        return func

    # ---- search ----------------------------------------------------

    @staticmethod
    def _query_tokens(text: str) -> List[str]:
        return [t for t in re.findall(
            r"[a-z0-9_.\-]+|[一-鿿]+", (text or "").lower()
        ) if t.strip()]

    @staticmethod
    def _token_overlap(query: str, field: str) -> float:
        f = (field or "").lower()
        if not f:
            return 0.0
        s = 0.0
        for t in FunctionRegistry._query_tokens(query):
            if t == f:
                s += 2.0
            elif t in f:
                s += 1.0
        return s

    def find(self, query: str, *, threshold: float = 0.6) -> List[Dict[str, Any]]:
        q = (query or "").strip().lower()
        if not q:
            return []
        results: List[Dict[str, Any]] = []
        if q in self._registry:
            results.append(self._registry[q])
        for m in get_close_matches(q, list(self._registry.keys()),
                                   n=5, cutoff=threshold):
            if self._registry[m] not in results:
                results.append(self._registry[m])
        # Substring search across description / docstring / aliases.
        for e in self._registry.values():
            if e in results:
                continue
            haystack = " ".join([
                str(e.get("description", "")),
                str(e.get("docstring", "")),
                " ".join(e.get("aliases", []) or []),
                " ".join(e.get("examples", []) or []),
                " ".join(e.get("related", []) or []),
                str(e.get("full_name", "")),
                str(e.get("short_name", "")),
            ]).lower()
            if q in haystack:
                results.append(e)
        # Deduplicate by full_name.
        seen: set = set()
        unique = []
        for e in results:
            n = e.get("full_name", "")
            if n not in seen:
                seen.add(n)
                unique.append(e)
        return unique

    def get_by_category(self, category: str) -> List[Dict[str, Any]]:
        if category not in self._categories:
            return []
        out = []
        for fn_name in self._categories[category]:
            for e in self._registry.values():
                if e["full_name"] == fn_name:
                    out.append(e)
                    break
        return out

    def list_categories(self) -> List[str]:
        return list(self._categories.keys())

    def all_parents(self) -> List[Dict[str, Any]]:
        """Unique parent (non-virtual) entries."""
        out: Dict[str, Dict[str, Any]] = {}
        for e in self._registry.values():
            if e.get("virtual_entry"):
                continue
            n = e.get("full_name", "")
            if n and n not in out:
                out[n] = e
        return list(out.values())

    def __len__(self) -> int:
        return len(self.all_parents())


_global_registry = FunctionRegistry()


def get_registry() -> FunctionRegistry:
    return _global_registry
