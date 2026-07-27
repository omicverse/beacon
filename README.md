# Beacon

Turn a package's tutorials, documentation, docstrings and source into a
**verified** agent-readable registry — a complete `@register_function`
decoration for every public callable, where each contract claim has been
checked by execution rather than asserted by a language model.

Companion to [`awe-agent-function`](../awe-agent-function) (the registry and
lookup runtime) and sibling in construction to
[`omicverse-rebuildr`](https://github.com/omicverse/omicverse-rebuildr)
(reference-driven R→Python translation). The protocol shape is deliberately
the same: markdown protocol the agent reads, a runnable engine that decides
pass/fail, gates pre-registered before any agent writes anything, automatic
rollback, and mandatory artefacts that make an unaudited release impossible.

## Why this exists

Runtime auto-decoration from docstrings alone has a measured ceiling. On a
six-library audit, every docstring-only synthesis landed at
`AFS ∈ [0.43, 0.53]` with **`C = 0.00`** — the contract sub-score is
structurally unreachable, because a docstring does not state which container
keys a function reads and writes. Hand-decorated `omicverse` reaches
`C = 0.27`, and even that is the library's largest remaining gap.

`C = 0` is not a tuning problem. The information is not in the docstring. It
is in two other places:

| Contract field | Where the information actually lives | How we recover it |
|---|---|---|
| `examples` | tutorials — real, working call sites | mine notebooks/scripts |
| `prerequisites` | tutorial **call order** | mine call sequences |
| `related` | tutorial **co-occurrence** | mine cell/section adjacency |
| `requires` | runtime — what breaks when absent | **execute and probe** |
| `produces` | runtime — what appears after the call | **execute and diff state** |
| `aliases` | docstring + prose docs + tutorial narration | synthesize, then verify by retrieval |

So the pipeline is not "ask an LLM to fill in fields." It is: harvest from
sources that carry the information, then **prove each claim against a running
interpreter**, and discard what cannot be proven.

## The core principle

> A contract field is admitted only if a probe can distinguish the world in
> which it is true from the world in which it is false.

`produces={"obsm": ["X_pca"]}` is admitted when running the function on a
fixture makes `X_pca` appear in `obsm` and not otherwise.
`prerequisites={"functions": ["scale"]}` is admitted when removing `scale`
from the call sequence makes the call fail. Fields that cannot be probed
(`category`, `description`) are synthesized and marked `unverified` in the
emitted entry — never silently mixed with proven ones.

This is what separates the output from "more metadata": every `verified: true`
field is a falsifiable claim that survived a falsification attempt.

## Architecture

```
   sources                harvesters            synthesis         proving
 ┌───────────┐         ┌──────────────┐
 │ docstrings├────────►│ DocstringH   ├──┐
 ├───────────┤         ├──────────────┤  │   ┌───────────┐   ┌──────────────┐
 │ source AST├────────►│ AstH         ├──┼──►│Synthesizer├──►│ Prover       │
 ├───────────┤         ├──────────────┤  │   │  (1/fn)   │   │ state_probe  │
 │ tutorials ├────────►│ TutorialH    ├──┤   └───────────┘   │ ablation     │
 ├───────────┤         ├──────────────┤  │         ▲         │ retrieval    │
 │ prose docs├────────►│ ProseH       ├──┘         │         └──────┬───────┘
 └───────────┘         └──────────────┘            │                │
                                                   │        refuted │
                                              ┌────┴─────┐◄─────────┘
                                              │ Repairer │  (bounded, ≤3)
                                              └──────────┘
                                                   │
                                             ┌─────▼──────┐
                                             │  Auditor   │ AFS + verified-rate
                                             └─────┬──────┘   + coverage
                                                   │
                                        emit: decorations.py
                                              REGISTRY_REPORT.md
                                              ITERATION_LOG.md
```

Five agent roles, one bounded repair loop. Harvesters run in parallel and are
deliberately **blind to each other** — a claim supported by two independent
harvesters is stronger evidence than one harvester asserting it twice.

## What makes a claim survive

| Probe | Field it decides | Refutation condition |
|---|---|---|
| `state_probe.diff` | `produces` | key does not appear after the call |
| `state_probe.strip` | `requires` | call still succeeds with the key removed |
| `sequence_ablation` | `prerequisites` | call still succeeds without the predecessor |
| `example_exec` | `examples` | example raises |
| `retrieval_check` | `aliases` | alias fails to retrieve its own function top-1 |
| — | `category`, `description` | not probeable → emitted as `unverified` |

`requires` uses *removal*, not observation: a function may touch a key
incidentally without depending on it. Only deleting the key and observing the
failure establishes dependence.

## State models are pluggable

`requires`/`produces` are meaningless without a notion of "the state a call
reads and writes." AnnData has one central mutable container; `pymatgen` and
`RDKit` do not. A state model adapter declares how to snapshot and diff, so
the same protocol applies to libraries with a different shape:

| Adapter | State snapshot | Used by |
|---|---|---|
| `anndata` | the seven containers (`layers/obsm/obsp/uns/var/obs/varm`) | omicverse, scanpy |
| `attrs` | public attributes + their types on the returned object | pymatgen, RDKit, ASE |
| `filesystem` | files created/modified under the working dir | atomate2, VASP wrappers |
| `namespace` | new bindings in the exec namespace | sklearn, scipy |

Adding a library means writing an adapter, not changing the protocol. See
`STATE_MODELS.md`.

## What the agent actually sees

The point of a registry is what arrives in the agent's context when it asks a
question in its own words. Below is a real, unedited `registry_lookup` call
against the decorated `omicverse` — reproduce it with
`python -c "import omicverse as ov; print(ov.utils.registry_lookup('leiden clustering'))"`.

**Agent turn 1 — the agent does not know the API name and searches by intent:**

```python
print(ov.utils.registry_lookup("leiden clustering"))
```

**What comes back:**

```
Found 10 matching functions:
  ────────────────────────────────────────────────────────────────────
  [match 1/10]
  ov.pp.leiden((adata, resolution=1.0, random_state=<ov.seed-default>,
                key_added='leiden', local_iterations=100, max_levels=10,
                device=None, symmetrize=None, **kwargs))
    Perform Leiden community detection clustering
    Docstring:
      leiden clustering
    Must run first: neighbors
    Requires: uns['neighbors'], obsp['connectivities']
    Produces: obs['leiden']
    Example: ov.pp.leiden(adata, resolution=1.0)
  ────────────────────────────────────────────────────────────────────
  [match 2/10]
  ov.utils.cluster[method=leiden]((adata, method='leiden',
                                   use_rep='X_pca', random_state=1024, ...))
    Variant of `omicverse.utils._cluster.cluster` when `method='leiden'`.
    ...
```

**Agent turn 2 — the code it now writes:**

```python
ov.pp.neighbors(adata, use_rep="X_pca")   # ← because of "Must run first"
ov.pp.leiden(adata, resolution=1.0)
labels = adata.obs["leiden"]              # ← because of "Produces"
```

Four things in that block are not in the docstring, and each maps to a
component of the entry:

| Line in the output | Field | What it prevents |
|---|---|---|
| `Must run first: neighbors` | `prerequisites` | calling `leiden` on an `adata` with no graph — the single most common failure mode we measure (`wrong_workflow_order`) |
| `Requires: uns['neighbors'], obsp['connectivities']` | `requires` | passing the wrong representation, or assuming `X_pca` is enough |
| `Produces: obs['leiden']` | `produces` | inventing a result key — `adata.obs['clusters']`, `adata.obs['leiden_labels']` |
| `ov.utils.cluster[method=leiden]` | dispatch entry | missing the second, parameterised way to reach the same algorithm |

The unaided agent has to guess all four. The docstring for this function is
the two words *"leiden clustering"*.

Every one of those claims was admitted by a probe, not asserted: `produces` by
observing `obs['leiden']` appear after a real call on a fixture, `requires` by
deleting the key and confirming the call fails, `prerequisites` by removing
`neighbors` from the sequence and confirming the same.

## Quick start

```bash
export DECORATR_TARGET=pymatgen
export DECORATR_ENV=/path/to/env          # interpreter with the target installed
python -m engine.smoke_test               # 30 s readiness check

# Phase 0: pre-register gates (edit, then commit — read-only afterwards)
cp manifest.template.yaml runs/pymatgen/manifest.yaml

# Phases 1-5, driven by the agent
#   "Decorate pymatgen. Follow PROTOCOL.md."
```

Read `PROTOCOL.md` before starting a run. `manifest.yaml` is committed before
the first agent turn and is never widened afterwards — the same read-only gate
discipline `omicverse-rebuildr` uses, for the same reason: a threshold that
can be relaxed measures nothing.

## Layout

```
beacon/
├── README.md                 this file
├── PROTOCOL.md               five phases, agent roles, gates, rollback
├── STATE_MODELS.md           adapter contract + writing a new one
├── HARVESTERS.md             per-source extraction rules and their limits
├── manifest.template.yaml    pre-registered gate spec
├── engine/
│   ├── state_probe.py        the oracle: snapshot / diff / strip
│   ├── tutorial_miner.py     call sequences + co-occurrence from notebooks
│   ├── contract_verify.py    adjudicates a candidate against the probes
│   ├── afs_audit.py          AFS + verified-rate + coverage report
│   ├── emit.py               candidates -> decorations.py
│   └── smoke_test.py
└── runs/<target>/            per-target working dir (manifest, log, output)
```

## Relationship to the benchmark

The output is evaluated the same way the hand-decorated registry was: a
Pass@1 contrast on an agent benchmark, plus the static audit. Two questions
the framework is built to answer, both open in the literature:

1. **Does synthesized decoration recover hand-authored performance?** If yes,
   adoption cost collapses and the "you are injecting expert knowledge"
   objection dissolves. If partly, the gap is a measurement of how much of
   the gain is expertise rather than structure.
2. **Does it transfer to a library with a different state model?** The
   `attrs` adapter plus a third-party materials benchmark tests exactly this,
   on a library nobody here maintains and tasks nobody here wrote.
