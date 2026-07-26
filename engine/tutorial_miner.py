"""Mine tutorials for the three things docstrings cannot supply.

A docstring describes a function in isolation. A tutorial shows it *in use*,
and that difference is exactly the contract gap:

``examples``       a tutorial call site is a working example. A synthesized one
                   is a guess.
``prerequisites``  what ran before it in a working notebook is a candidate
                   dependency — a candidate only; see the warning below.
``related``        what appears alongside it, repeatedly, across independent
                   tutorials.
``aliases``        the prose around the call is how practitioners *name* the
                   operation. "Normalise the counts" sitting above
                   ``ov.pp.preprocess`` is the alias a docstring will never
                   contain.

The ordering trap
-----------------
Tutorial order encodes habit as much as necessity. An author who always runs
QC before PCA has not shown that PCA requires QC. This module therefore emits
*candidates with support counts*, never conclusions; only
``state_probe.probe_prerequisites`` — which drops the predecessor and re-runs —
can promote a candidate to a claim. Mining proposes; ablation disposes.

Support counting is per-tutorial, not per-call-site: a single notebook that
calls ``pca`` ten times after ``scale`` is one piece of evidence, not ten.
Otherwise one verbose tutorial outvotes every other source.
"""

from __future__ import annotations

import ast
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator

# Prose lead-ins that mark a naming phrase rather than commentary.
_ALIAS_CUES = re.compile(
    r"(?:^|\n)\s*(?:#+\s*)?(?:step\s*\d+[:.]?\s*)?"
    r"(?P<phrase>[A-Z][^.\n]{6,80}?)\s*(?:\.|:|\n)",
    re.MULTILINE,
)
_STOP = {
    "we", "then", "next", "now", "here", "this", "that", "note", "first",
    "finally", "let", "in", "the", "a", "an", "it", "you", "figure", "see",
}

# --- CJK -------------------------------------------------------------------
# `_ALIAS_CUES` is an ASCII device: it anchors on a capital letter and the
# phrase it captures is then tokenised with ``[A-Za-z][A-Za-z_-]+``, which
# deletes every CJK character. A corpus with Chinese prose therefore yields
# zero Chinese naming phrases — not few, zero — and the multilingual aliases a
# hand annotator writes (``质量控制``, ``对数归一化``) are unrecoverable by
# construction. That is a blind spot in the extractor, not a property of the
# corpus.
#
# Chinese has no capitalisation to anchor on and no spaces to tokenise on, so
# the ASCII rule does not transfer. What does transfer is the *shape* of the
# rule: take the text between delimiters, and keep it if it is short enough to
# be a name rather than a sentence. Here the delimiters are punctuation
# (Chinese and ASCII) plus a small set of function words that cannot begin or
# end a term.
_CJK = "㐀-䶿一-鿿豈-﫿぀-ヿ가-힯"
_CJK_CHAR = re.compile(f"[{_CJK}]")
# a segment is a maximal run of term characters: CJK, latin, digits, _ + -
_CJK_SEGMENT = re.compile(f"[{_CJK}A-Za-z0-9_+-]+")
# function words that join two terms; splitting on them turns
# "细胞类型注释的共识方法" into two names instead of one sentence.
# Deliberately conservative: characters that also occur *inside* domain terms
# (对 in 对数归一化, 在 in 潜在空间) are left out, because splitting on them
# would destroy the very aliases this is meant to recover.
_CJK_JOINERS = re.compile(
    "的|和|与|及|或|我们|使用|用于|进行|包括|可以|然后|首先|这里|因此|例如|"
    "以及|其中|需要|注意|来自|基于|以便|同时|并且"
)
_CJK_MIN, _CJK_MAX = 2, 14      # a name, not a sentence
_CJK_SEGMENT_MAX = 20


@dataclass
class CallSite:
    func: str                 # dotted name, e.g. "ov.pp.pca"
    code: str                 # the source line(s) of the call
    source: str               # tutorial path
    order: int                # position within that tutorial
    prose: str = ""           # nearest preceding markdown / comment block


@dataclass
class FunctionEvidence:
    func: str
    examples: list[str] = field(default_factory=list)
    prereq_candidates: Counter = field(default_factory=Counter)
    related_candidates: Counter = field(default_factory=Counter)
    alias_phrases: Counter = field(default_factory=Counter)
    n_tutorials: int = 0


def _dotted(node: ast.AST) -> str | None:
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return None


def _iter_cells(path: Path) -> Iterator[tuple[str, str]]:
    """Yield ``(kind, text)`` where kind is 'code' or 'prose'."""
    if path.suffix == ".ipynb":
        try:
            nb = json.loads(path.read_text())
        except Exception:
            return
        for cell in nb.get("cells", []):
            src = "".join(cell.get("source", []))
            if not src.strip():
                continue
            yield ("code" if cell.get("cell_type") == "code" else "prose", src)
    elif path.suffix in (".py", ".md"):
        text = path.read_text(errors="replace")
        if path.suffix == ".md":
            # fenced python blocks are code; everything else is prose
            for i, chunk in enumerate(re.split(r"```(?:python|py)?\n", text)):
                if i == 0:
                    yield ("prose", chunk)
                else:
                    code, _, rest = chunk.partition("```")
                    yield ("code", code)
                    if rest.strip():
                        yield ("prose", rest)
        else:
            yield ("code", text)


def _cjk_phrases(prose: str) -> list[str]:
    """Naming phrases from CJK prose.

    Two granularities, because a hand-written alias may be either: the
    punctuation-delimited segment (``质量控制和修剪``) and the joiner-split
    terms inside it (``质量控制``, ``修剪``). Mixed tokens survive intact —
    ``log变换`` and ``HVG选择`` are single segments, which is exactly how a
    practitioner writes them.
    """
    if not _CJK_CHAR.search(prose):
        return []
    out: list[str] = []
    for seg in _CJK_SEGMENT.findall(prose):
        if not _CJK_CHAR.search(seg):
            continue                      # pure-ASCII: the ASCII rule owns it
        seg = seg.strip("_+-")
        if _CJK_MIN <= len(seg) <= _CJK_SEGMENT_MAX:
            out.append(seg)
        for part in _CJK_JOINERS.split(seg):
            part = part.strip("_+-")
            if (part != seg and _CJK_CHAR.search(part)
                    and _CJK_MIN <= len(part) <= _CJK_MAX):
                out.append(part)
    return out


def _alias_phrases(prose: str) -> list[str]:
    out: list[str] = []
    for m in _ALIAS_CUES.finditer(prose):
        phrase = m.group("phrase").strip().strip("#*` ")
        words = [w for w in re.findall(r"[A-Za-z][A-Za-z_-]+", phrase.lower())]
        if not 1 <= len(words) <= 6:
            continue
        if not words or words[0] in _STOP:
            continue
        out.append(" ".join(words))
    out.extend(_cjk_phrases(prose))
    return out


def mine_tutorial(path: Path, package: str) -> list[CallSite]:
    """Extract ordered call sites to ``package`` from one tutorial."""
    sites: list[CallSite] = []
    pending_prose = ""
    order = 0
    for kind, text in _iter_cells(path):
        if kind == "prose":
            pending_prose = text
            continue
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = _dotted(node.func)
            if not name or not name.split(".")[0] == package.split(".")[0]:
                continue
            try:
                snippet = ast.unparse(node)
            except Exception:
                snippet = name + "(...)"
            sites.append(CallSite(func=name, code=snippet, source=str(path),
                                  order=order, prose=pending_prose))
            order += 1
        pending_prose = ""
    return sites


def mine_corpus(
    roots: Iterable[Path],
    package: str,
    related_window: int = 3,
) -> dict[str, FunctionEvidence]:
    """Aggregate evidence across a tutorial corpus.

    ``related_window`` bounds co-occurrence to nearby calls; without a bound
    every function in a long notebook is "related" to every other, which is
    true and useless.
    """
    evidence: dict[str, FunctionEvidence] = defaultdict(
        lambda: FunctionEvidence(func="")
    )
    seen_in_tutorial: dict[str, set[str]] = defaultdict(set)

    files = [p for root in roots for p in Path(root).rglob("*")
             if p.suffix in (".ipynb", ".py", ".md")]

    for path in files:
        sites = mine_tutorial(path, package)
        if not sites:
            continue
        names = [s.func for s in sites]
        for i, site in enumerate(sites):
            ev = evidence[site.func]
            ev.func = site.func
            if site.code not in ev.examples and len(ev.examples) < 8:
                ev.examples.append(site.code)
            for phrase in _alias_phrases(site.prose):
                ev.alias_phrases[phrase] += 1
            seen_in_tutorial[site.func].add(str(path))
            # per-tutorial dedup: count each predecessor/neighbour once
            for prev in dict.fromkeys(names[:i]):
                if prev != site.func:
                    ev.prereq_candidates[prev] += 0   # touch, weight below
            lo, hi = max(0, i - related_window), min(len(names), i + related_window + 1)
            for nb in dict.fromkeys(names[lo:hi]):
                if nb != site.func:
                    ev.related_candidates[nb] += 0

        # Weight once per tutorial so a verbose notebook cannot outvote a corpus.
        for func in dict.fromkeys(names):
            ev = evidence[func]
            idx = names.index(func)
            for prev in dict.fromkeys(names[:idx]):
                if prev != func:
                    ev.prereq_candidates[prev] += 1
            lo, hi = max(0, idx - related_window), min(len(names), idx + related_window + 1)
            for nb in dict.fromkeys(names[lo:hi]):
                if nb != func:
                    ev.related_candidates[nb] += 1

    for func, tuts in seen_in_tutorial.items():
        evidence[func].n_tutorials = len(tuts)
    return dict(evidence)


def summarize(evidence: dict[str, FunctionEvidence], min_support: int = 2) -> dict:
    """Shape the evidence for the synthesizer, with support attached.

    ``min_support`` is a floor on independent tutorials, not on call count. A
    dependency seen in one notebook is an anecdote; the synthesizer may still
    propose it, but it is flagged so the prover knows to ablate it first.
    """
    out = {}
    for func, ev in evidence.items():
        out[func] = {
            "n_tutorials": ev.n_tutorials,
            "examples": ev.examples[:3],
            "prereq_candidates": [
                {"func": f, "support": c, "weak": c < min_support}
                for f, c in ev.prereq_candidates.most_common(6)
            ],
            "related_candidates": [
                f for f, c in ev.related_candidates.most_common(5) if c >= min_support
            ],
            "alias_phrases": [
                p for p, c in ev.alias_phrases.most_common(8) if c >= min_support
            ],
        }
    return out


__all__ = ["CallSite", "FunctionEvidence", "mine_tutorial", "mine_corpus", "summarize"]
