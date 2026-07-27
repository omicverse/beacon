"""Feasibility probe: does the oracle work on an object-centric library?

The omicverse evidence was collected on AnnData, where one mutable container
is threaded through every call, so ``snapshot(subject)`` before and after is
well defined. ``pymatgen`` is not shaped that way:

    primitive = structure.get_primitive_structure()   # new object; input untouched

Probing the *input* therefore observes no change and refutes every ``produces``
claim — not because the claims are wrong but because the probe is looking at
the wrong object. If that cannot be fixed, the contract sub-score collapses to
zero on this library and the whole migration is pointless. So this is the
question to answer before investing in a full decoration run, not after.

Three probe strategies are compared per function:

``in_place``    snapshot the subject before and after. Correct for methods that
                mutate (``Structure.make_supercell``), blind to those that return.
``fold_back``   run the call, then copy the returned object's public attribute
                surface onto the subject so the diff sees it. What
                ``STATE_MODELS.md`` prescribes.
``return_diff`` snapshot the input, snapshot the *returned object*, diff those
                two directly — no mutation of the subject at all.

The interesting column is not "did a probe succeed" but **which strategy each
kind of function needs**, because that determines what the framework has to
generate per call site rather than once per library.
"""

from __future__ import annotations

import sys
from pathlib import Path

BEACON = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BEACON / "engine"))

from state_probe import AttrsAdapter, probe_produces, probe_requires  # noqa: E402

from pymatgen.core import Lattice, Structure  # noqa: E402


def make_si() -> Structure:
    """Conventional cubic Si. Fresh per trial — probes mutate."""
    return Structure(
        Lattice.cubic(5.43),
        ["Si"] * 8,
        [[0, 0, 0], [0.25, 0.25, 0.25], [0, 0.5, 0.5], [0.25, 0.75, 0.75],
         [0.5, 0, 0.5], [0.75, 0.25, 0.75], [0.5, 0.5, 0], [0.75, 0.75, 0.25]],
    )


def _public_attrs(obj) -> dict:
    out = {}
    for n in dir(obj):
        if n.startswith("_"):
            continue
        try:
            v = getattr(obj, n)
        except Exception:
            continue
        if not callable(v):
            out[n] = v
    return out


def fold_back(fn):
    """Run ``fn`` and graft the returned object's attribute surface onto the subject.

    ``Structure`` rejects unknown attributes on some builds, so the graft is
    written into ``__dict__`` directly and failures per attribute are ignored:
    the adapter reads through ``dir()``/``getattr``, which sees ``__dict__``.
    """
    def call(subject):
        out = fn(subject)
        if out is None or out is subject:
            return
        for k, v in _public_attrs(out).items():
            try:
                subject.__dict__[k] = v
            except Exception:
                pass
    return call


# (name, callable, mutates-in-place?, what a decorator would plausibly claim)
CASES = [
    ("get_primitive_structure",
     lambda s: s.get_primitive_structure(), False, "a reduced cell"),
    ("get_reduced_structure",
     lambda s: s.get_reduced_structure(), False, "a niggli-reduced cell"),
    ("make_supercell",
     lambda s: s.make_supercell([2, 1, 1]), True, "an enlarged cell"),
    ("add_oxidation_state_by_guess",
     lambda s: s.add_oxidation_state_by_guess(), True, "oxidation states on species"),
    ("add_site_property",
     lambda s: s.add_site_property("selective_dynamics", [[True] * 3] * len(s)),
     True, "a per-site property"),
    ("copy", lambda s: s.copy(), False, "an identical structure"),
    ("get_sorted_structure",
     lambda s: s.get_sorted_structure(), False, "a sorted structure"),
    ("perturb", lambda s: s.perturb(0.01), True, "displaced sites"),
]


def strategy_report():
    ad = AttrsAdapter()
    print(f"{'function':32s} {'in_place':>9s} {'fold_back':>10s} {'return_diff':>12s}  note")
    print("-" * 88)
    rows = []
    for name, fn, mutates, note in CASES:
        # in_place
        v_ip = probe_produces(lambda s: fn(s), make_si, ad, timeout_s=120)
        n_ip = sum(len(v) for v in v_ip.observed.values())
        # fold_back
        v_fb = probe_produces(fold_back(fn), make_si, ad, timeout_s=120)
        n_fb = sum(len(v) for v in v_fb.observed.values())
        # return_diff: compare input surface to returned surface, no probe needed
        try:
            s = make_si()
            before = set(_public_attrs(s))
            out = fn(s)
            after = set(_public_attrs(out if out is not None else s))
            n_rd = len(after - before)
        except Exception:
            n_rd = -1
        rows.append((name, n_ip, n_fb, n_rd, mutates))
        print(f"{name:32s} {n_ip:9d} {n_fb:10d} {n_rd:12d}  {note}")
    return rows


def summarise(rows):
    print("\n" + "=" * 88)
    mut = [r for r in rows if r[4]]
    ret = [r for r in rows if not r[4]]
    print(f"in-place 函数 {len(mut)} 个, 返回新对象 {len(ret)} 个")
    print(f"  in_place 策略能观察到变化的:   "
          f"{sum(1 for r in mut if r[1] > 0)}/{len(mut)} (mutating)  "
          f"{sum(1 for r in ret if r[1] > 0)}/{len(ret)} (returning)")
    print(f"  fold_back 策略能观察到变化的:  "
          f"{sum(1 for r in mut if r[2] > 0)}/{len(mut)} (mutating)  "
          f"{sum(1 for r in ret if r[2] > 0)}/{len(ret)} (returning)")
    print("\n判读:")
    blind = [r[0] for r in ret if r[1] == 0]
    if blind:
        print(f"  in_place 对这些返回型函数完全失明: {blind}")
    fixed = [r[0] for r in ret if r[1] == 0 and r[2] > 0]
    print(f"  fold_back 救回来的: {fixed if fixed else '无 —— 这是坏消息'}")
    still = [r[0] for r in ret if r[2] == 0]
    if still:
        print(f"  两种策略都测不到: {still}")
        print("  → 这些函数的 produces 无法用属性面来表达，"
              "说明 pymatgen 的状态模型需要的不是属性 diff，而是别的粒度")


if __name__ == "__main__":
    rows = strategy_report()
    summarise(rows)
