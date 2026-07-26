"""Agent-Friendliness Score (AFS) audit over the registry.

See §3.7 of the paper for the formal definition. Default weights
(W_D, W_C, W_S, W_B) = (0.30, 0.35, 0.15, 0.20). Reweight to taste.
"""

from __future__ import annotations

import re
import statistics as stats
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .registry import get_registry


W_D = 0.30
W_C = 0.35
W_S = 0.15
W_B = 0.20


_DISPATCH_PARAM = re.compile(
    r"\b(method|backend|mode|provider|task|classifier|organism|"
    r"correction_method|doublets_method|prediction_mode|api_type)\b",
    re.IGNORECASE,
)


def _multilingual(aliases: List[str]) -> bool:
    for a in aliases or []:
        s = str(a)
        if not s.isascii():
            return True
        if " " in s.strip():
            return True
    return False


def _kw_with_default(signature: str, parameters: list) -> bool:
    if signature and "=" in signature:
        return True
    return bool(parameters) and len([p for p in parameters
                                     if not str(p).startswith("self")]) >= 3


def _dispatch_hint(signature: str, description: str, docstring: str) -> bool:
    if signature and re.search(
            r"\b(method|backend|mode|provider|task|classifier|organism)\b",
            signature):
        return True
    txt = (description or "") + " " + (docstring or "")
    return bool(txt and _DISPATCH_PARAM.search(txt))


@dataclass
class Subscores:
    D: float = 0.0
    C: float = 0.0
    S: float = 0.0
    B: float = 0.0
    afs: float = 0.0


def score_entry(entry: dict) -> Subscores:
    aliases = entry.get("aliases") or []
    category = str(entry.get("category", "") or "").strip()
    description = str(entry.get("description", "") or "").strip()
    requires = entry.get("requires") or {}
    produces = entry.get("produces") or {}
    auto_fix = str(entry.get("auto_fix", "none") or "none")
    prereqs = entry.get("prerequisites") or {}
    examples = entry.get("examples") or []
    related = entry.get("related") or []
    signature = str(entry.get("signature", "") or "")
    parameters = entry.get("parameters") or []
    docstring = str(entry.get("docstring", "") or "")

    n_alias = sum(1 for a in aliases if str(a).strip())
    d = ((1 if n_alias >= 3 else 0)
         + (1 if _multilingual(aliases) else 0)
         + (1 if category else 0)
         + (1 if len(description) >= 40 else 0)) / 4.0

    c = ((1 if (requires or produces) else 0)
         + (1 if auto_fix in ("auto", "escalate") else 0)
         + (1 if (prereqs.get("functions")
                  or prereqs.get("optional_functions")) else 0)) / 3.0

    s = ((1 if _kw_with_default(signature, parameters) else 0)
         + (1 if _dispatch_hint(signature, description, docstring) else 0)) / 2.0

    b = ((1 if len(examples) >= 1 else 0)
         + (1 if len(related) >= 1 else 0)) / 2.0

    afs = W_D * d + W_C * c + W_S * s + W_B * b
    return Subscores(D=round(d, 3), C=round(c, 3), S=round(s, 3),
                     B=round(b, 3), afs=round(afs, 3))


@dataclass
class AFSReport:
    library: str
    n_functions: int
    library_afs_mean: float
    library_afs_median: float
    library_afs_p10: float
    library_afs_p90: float
    subscore_means: Dict[str, float]
    weights: Dict[str, float]
    rows: List[dict] = field(default_factory=list)

    def summary(self) -> str:
        ss = self.subscore_means
        out = [
            f"Library: {self.library}",
            f"  n_functions:    {self.n_functions}",
            f"  AFS (mean):     {self.library_afs_mean:.3f}",
            f"  AFS (median):   {self.library_afs_median:.3f}",
            f"  AFS [p10, p90]: [{self.library_afs_p10:.3f}, {self.library_afs_p90:.3f}]",
            "  Sub-scores (means):",
            f"    D (discoverability): {ss['D']:.3f}  (w={self.weights['D']})",
            f"    C (contract):        {ss['C']:.3f}  (w={self.weights['C']})",
            f"    S (signature):       {ss['S']:.3f}  (w={self.weights['S']})",
            f"    B (behavioural):     {ss['B']:.3f}  (w={self.weights['B']})",
        ]
        return "\n".join(out)


def compute_afs(library_name: Optional[str] = None) -> AFSReport:
    """Audit the global registry; optionally restrict to entries whose
    full_name starts with `library_name.`."""

    registry = get_registry()
    parents = registry.all_parents()
    if library_name:
        prefix = library_name + "."
        parents = [p for p in parents
                   if str(p.get("full_name", "")).startswith(prefix)]

    rows = []
    for p in parents:
        ss = score_entry(p)
        rows.append({
            "full_name": p.get("full_name"),
            "category":  p.get("category"),
            "D": ss.D, "C": ss.C, "S": ss.S, "B": ss.B, "AFS": ss.afs,
        })

    afs_vals = [r["AFS"] for r in rows] or [0.0]
    pcts = sorted(afs_vals)
    p10 = pcts[max(0, int(0.10 * (len(pcts) - 1)))]
    p90 = pcts[min(len(pcts) - 1, int(0.90 * (len(pcts) - 1)))]
    sub_means = {
        "D": round(stats.fmean([r["D"] for r in rows]) if rows else 0.0, 3),
        "C": round(stats.fmean([r["C"] for r in rows]) if rows else 0.0, 3),
        "S": round(stats.fmean([r["S"] for r in rows]) if rows else 0.0, 3),
        "B": round(stats.fmean([r["B"] for r in rows]) if rows else 0.0, 3),
    }

    return AFSReport(
        library=library_name or "<global registry>",
        n_functions=len(rows),
        library_afs_mean=round(stats.fmean(afs_vals), 3) if rows else 0.0,
        library_afs_median=round(stats.median(afs_vals), 3) if rows else 0.0,
        library_afs_p10=round(p10, 3),
        library_afs_p90=round(p90, 3),
        subscore_means=sub_means,
        weights={"D": W_D, "C": W_C, "S": W_S, "B": W_B},
        rows=rows,
    )
