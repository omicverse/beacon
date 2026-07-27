"""Re-run the feasibility question under the MatData convention.

``feasibility.py`` probed bare ``pymatgen`` and found zero observable state
changes across eight operations and three strategies. This asks the same
question of the same operations wrapped in the convention, using the *same*
probes and the ``anndata`` adapter Beacon already ships.

The comparison that matters is per operation, not in aggregate: an operation
that was invisible before and is confirmed now is evidence the container was
the blocker. One that is still invisible is evidence it was not.
"""

from __future__ import annotations

import sys
from pathlib import Path

BEACON = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BEACON / "engine"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from pymatgen.core import Lattice, Structure  # noqa: E402

import matdata as mt  # noqa: E402
from state_probe import AnnDataAdapter, probe_produces, probe_requires  # noqa: E402


def _si(a: float = 5.43) -> Structure:
    return Structure(
        Lattice.cubic(a), ["Si"] * 8,
        [[0, 0, 0], [0.25, 0.25, 0.25], [0, 0.5, 0.5], [0.25, 0.75, 0.75],
         [0.5, 0, 0.5], [0.75, 0.25, 0.75], [0.5, 0.5, 0], [0.75, 0.75, 0.25]])


def _nacl(a: float = 5.64) -> Structure:
    return Structure(Lattice.cubic(a), ["Na", "Cl"], [[0, 0, 0], [0.5, 0.5, 0.5]])


def make_df() -> pd.DataFrame:
    """A matminer-shaped input: a `structure` column plus metadata."""
    return pd.DataFrame({
        "structure": [_si(5.43), _si(5.50), _nacl(5.64), _nacl(5.70)],
        "mp_id": ["mp-149", "mp-149s", "mp-22862", "mp-22862s"],
    })


def fresh():
    """A MatData at the state each probe needs, built from the DataFrame."""
    return mt.from_matminer_df(make_df())


def staged(*steps):
    """Fresh MatData with the given deposits already applied."""
    def make():
        md = fresh()
        for s in steps:
            s(md)
        return md
    return make


# (label, subject factory, call, claimed produces, claimed requires)
CASES = [
    ("describe", fresh, mt.describe,
     {"obs": ["formula", "nsites", "volume", "density"]}, {}),
    ("featurize", fresh, mt.featurize,
     {"obsm": ["X_composition"], "uns": ["features"]}, {}),
    ("primitive", fresh, mt.primitive,
     {"obs": ["nsites_primitive"]}, {}),
    ("energy_model", staged(mt.featurize), lambda md: mt.energy_model(md, layer="toy"),
     {"obsm": ["energy_toy"], "obs": ["energy_toy"]}, {"obsm": ["X_composition"]}),
    ("convex_hull", staged(mt.featurize, mt.describe,
                           lambda md: mt.energy_model(md, layer="toy")),
     lambda md: mt.convex_hull(md, layer="toy"),
     {"obs": ["e_above_hull"]}, {"obs": ["energy_toy"]}),
    ("similarity", staged(mt.featurize), mt.similarity,
     {"obsp": ["structure_similarity"]}, {"obsm": ["X_composition"]}),
]


def main() -> int:
    ad = AnnDataAdapter()
    print(f"{'operation':14s} {'produces 声称':>12s} {'确认':>5s} {'证伪':>5s} "
          f"{'漏报':>5s} | {'requires 声称':>13s} {'确认':>5s} {'证伪':>5s}")
    print("-" * 88)
    tot = {"c": 0, "r": 0, "u": 0, "rc": 0, "rr": 0, "n": 0, "nr": 0}
    for label, subject, call, claim_p, claim_r in CASES:
        vp = probe_produces(call, subject, ad, claimed=claim_p, timeout_s=120)
        np_ = sum(len(v) for v in claim_p.values())
        nr = sum(len(v) for v in claim_r.values())
        if claim_r:
            vr = probe_requires(call, subject, ad, claimed=claim_r, timeout_s=120)
            rc, rr = len(vr.confirmed), len(vr.refuted)
        else:
            rc = rr = 0
        tot["n"] += np_; tot["c"] += len(vp.confirmed); tot["r"] += len(vp.refuted)
        tot["u"] += len(vp.unclaimed); tot["nr"] += nr; tot["rc"] += rc; tot["rr"] += rr
        err = f"  BASELINE FAILED: {vp.baseline_error}" if vp.baseline_error else ""
        print(f"{label:14s} {np_:12d} {len(vp.confirmed):5d} {len(vp.refuted):5d} "
              f"{len(vp.unclaimed):5d} | {nr:13d} {rc:5d} {rr:5d}{err}")
    print("-" * 88)
    print(f"{'合计':14s} {tot['n']:12d} {tot['c']:5d} {tot['r']:5d} {tot['u']:5d} "
          f"| {tot['nr']:13d} {tot['rc']:5d} {tot['rr']:5d}")

    print("\n对照 feasibility.py（裸 pymatgen）: 8 个操作 x 3 策略, 可观察变化 0")
    print(f"本次（MatData 约定）: produces 确认 {tot['c']}/{tot['n']}, "
          f"requires 确认 {tot['rc']}/{tot['nr']}")
    if tot["c"] == 0:
        print("\n判读: 容器没有解决问题 —— 阻碍从来不在容器。")
    else:
        print(f"\n判读: 之前完全不可见的操作现在有 {tot['c']} 条 produces 被探针确认，"
              f"{tot['rc']} 条 requires 被删除法确认。容器就是阻碍。")
    if tot["r"]:
        print(f"警告: {tot['r']} 条声称被证伪 —— 约定写错了，不是探针的问题。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
