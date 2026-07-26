"""30-second readiness check: adapters, probes and miner all work.

Runs the probes against a synthetic subject whose behaviour is known, so a
green smoke test means the oracle can actually distinguish true from false
claims — not merely that the imports resolved.
"""
from __future__ import annotations
import sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from state_probe import (NamespaceAdapter, probe_produces, probe_requires,  # noqa: E402
                         probe_prerequisites, get_adapter, ADAPTERS)
from tutorial_miner import mine_tutorial, mine_corpus, summarize  # noqa: E402

ok = True
def check(label, cond, detail=""):
    global ok
    ok &= bool(cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}{'  ' + detail if detail else ''}")

print("adapters")
check("registry has 4 adapters", set(ADAPTERS) == {"anndata","attrs","namespace","filesystem"})
check("get_adapter('namespace')", get_adapter("namespace").name == "namespace")

print("probe_produces distinguishes true from false claims")
ad = NamespaceAdapter()
mk = lambda: {"seed": 1}
call = lambda ns: ns.__setitem__("result", 42)
v = probe_produces(call, mk, ad, claimed={"names": ["result"]})
check("true claim confirmed", v.confirmed == [("names", "result")])
v2 = probe_produces(call, mk, ad, claimed={"names": ["nope"]})
check("false claim refuted", v2.refuted == [("names", "nope")], f"observed={v2.observed}")
check("under-declaration surfaced", ("names","result") in v2.unclaimed)

print("probe_requires uses removal, not observation")
def needs_seed(ns):
    return ns["seed"] * 2                      # raises KeyError without 'seed'
r = probe_requires(needs_seed, lambda: {"seed": 1, "extra": 9}, ad,
                   claimed={"names": ["seed", "extra"]})
check("genuine dependency confirmed", ("names","seed") in r.confirmed)
check("incidental key refuted", ("names","extra") in r.refuted,
      "a key present but unused must NOT be admitted")

print("probe_prerequisites ablates rather than observes")
steps = [("prep", lambda ns: ns.__setitem__("x", 1)),
         ("decor", lambda ns: ns.__setitem__("unused", 0)),
         ("target", lambda ns: ns.__setitem__("y", ns["x"] + 1))]
p = probe_prerequisites(steps, lambda: {}, "target")
check("real predecessor confirmed", p.get("prep") is True)
check("habitual predecessor rejected", p.get("decor") is False,
      "order alone must not imply dependency")

print("tutorial miner")
with tempfile.TemporaryDirectory() as d:
    nb = Path(d) / "t.py"
    nb.write_text("import ov\nov.pp.scale(a)\nov.pp.pca(a, n_pcs=50)\n")
    sites = mine_tutorial(nb, "ov")
    check("call sites found", [s.func for s in sites] == ["ov.pp.scale", "ov.pp.pca"])
    s = summarize(mine_corpus([Path(d)], "ov"))
    check("prereq candidate proposed", any(
        c["func"] == "ov.pp.scale" for c in s["ov.pp.pca"]["prereq_candidates"]))
    check("examples captured real call", "n_pcs=50" in " ".join(s["ov.pp.pca"]["examples"]))

print("\n" + ("SMOKE OK — the oracle can refute" if ok else "SMOKE FAILED"))
sys.exit(0 if ok else 1)
