# PROTOCOL

One function at a time. Not a batch pass over the package.

This is the same shape `omicverse-rebuildr` uses for a port: a target is
worked through by an agent that reads the sources, forms a hypothesis, builds
an executable check, and iterates against it until a pre-registered gate
clears. The unit there is an R package; the unit here is a **public callable**.

## Why per-function rather than batch

A batch pipeline can only probe a function with the example the library
already ships. Measured on `omicverse`, that constraint is what binds: of 219
public callables in scope, a batch pass could probe **55**, and of those it
confirmed a contract for **27**. The 164 it could not touch were lost to
causes a per-function agent removes rather than records:

| Batch outcome | n | What a per-function agent does instead |
|---|---:|---|
| declares no contract at all | 128 | reads the source and *derives* the contract, then probes it |
| example references undefined objects (`adata_ref`, `tfs`, …) | 22 | **writes a call that runs**, constructing the objects it needs |
| contract is prose placeholders (`"cell type labels"`) | 8 | resolves the placeholder to a real key by execution |
| needs an external file or service | 6 | stubs, or records an explicit unprobeable reason |

The batch run also had to invent three heuristic starting states
(strict / staged / enriched) and try all of them, because nothing in it could
decide *per function* what preconditions to establish. An agent reading the
source knows that `pca` wants a scaled layer and builds exactly that.

So the batch numbers are a **floor**, not an estimate. Treat them as the
baseline this protocol has to beat.

## Phase 0 — Pre-register (once per package)

`runs/<target>/manifest.yaml`, committed before any function is touched, then
read-only. Fixes the interpreter, the state adapter, the fixture (SHA-256
pinned), the tutorial corpus, and the gates. See `manifest.template.yaml`.

Also once per package: `python -m engine.smoke_test`, and a **worklist** —
every public callable, each marked `pending` / `done` / `skipped(reason)`.
The worklist is the checklist the run ticks through.

## Phase 1 — Discovery (per function, cheap, do not skip)

Before reading anything else, check whether the work already exists:

1. Is this function already decorated upstream? If so, the existing entry is a
   **hypothesis to test**, not a result to copy — Phase 3 probes it like any
   other. (On `omicverse` this matters: 32.6 % of hand `produces` claims and
   21.6 % of hand `requires` claims are refuted by the oracle.)
2. Has a **sibling** already been completed in this run? `ov.pp.umap` after
   `ov.pp.pca` inherits the fixture staging, the call skeleton and most of the
   prerequisite chain. Reuse compounds; this is the analogue of rebuildr's
   seed-template reuse and it is where the per-function cost comes down.

## Phase 2 — Read (per function)

Four sources, read in this order, because later ones are only interpretable in
light of earlier ones:

1. **Source** — what it actually mutates. The ground truth for the contract.
2. **Signature + type hints** — dispatch parameters, keyword-only defaults.
3. **Tutorial call sites** — `engine/tutorial_miner.py` for this function:
   real calls, what ran before them, what prose named the operation.
4. **Prose docs** — naming, category, multilingual aliases.

Output: a written hypothesis (one paragraph in `ITERATION_LOG.md`) of what the
function does, what state it needs, and what it leaves behind. Committing the
hypothesis *before* probing is what makes the probe a test rather than a
description.

## Phase 3 — Build a runnable call

**The step batch automation does not have, and the reason it stalls.**

Write `make_subject()` and `call(subject)` such that the call succeeds on the
fixture. This may require staging: read the source, see that `pca` needs
`layers["scaled"]`, and have `make_subject` run `scale` first. Construct any
auxiliary objects the call needs (a reference AnnData, a gene list, a marker
dict) rather than abandoning the function because its shipped example
referenced one.

Gate 3: the call runs on the fixture without raising. If it cannot be made to
run — GPU-only, licensed binary, network service — mark the function
`skipped(unprobeable: <reason>)` in the worklist and move on. **Skipping is a
recorded outcome, not a silent gap**; the audit reports the skip rate, and a
protocol that quietly drops hard functions would report a flattering
verified-rate over an easy subset.

## Phase 4 — Probe and iterate

Run the probes from `engine/state_probe.py` against the hypothesis:

| Claim | Probe | Promoted when |
|---|---|---|
| `produces` | `probe_produces` | key appears after the call |
| `requires` | `probe_requires` | deleting the key makes the call fail |
| `prerequisites` | `probe_prerequisites` | dropping the predecessor makes the call fail |
| `examples` | execute the call written in Phase 3 | returns without raising |
| `aliases` | `retrieval_check` | the alias retrieves this function at rank 1 |

Three outcomes, kept strictly separate:

- **confirmed** → `verified: true`.
- **refuted** → dropped. Not softened, not demoted to a comment. A wrong
  contract is worse than a missing one: it makes an agent compose confidently
  and incorrectly.
- **inconclusive** → dropped from the contract, reason logged. Never quietly
  read as confirmed.

`probe_produces` also returns keys that appeared but were **not** claimed. On
`omicverse` the hand registry under-declares **1.33 keys for every one it
declares correctly**, so this feedback is not an edge case — it is the main
defect the loop exists to catch. Add them to the hypothesis and re-probe.

**At most three rounds per function.** The cap is protocol. An unbounded loop
lets the agent search for a phrasing that passes rather than a claim that is
true.

Each round appends one YAML block:

```yaml
- function: "ov.pp.pca"
  round: 2
  hypothesis_change: "add produces varm['PCs'] (under-declared in round 1)"
  probe: "probe_produces"
  verdict: "confirmed"
  contract_verified: 3
  contract_refuted: 0
```

## Phase 5 — Emit the entry

Fields carry their provenance. `verified: true` only where a probe confirmed;
`derived` for values computed from confirmed ones (`auto_fix` follows from the
confirmed prerequisite chain: `auto` for chains ≤ 2, `escalate` where a
workflow-level function exists, else `none`); `unverified` for the
irreducibly judgemental (`category`, `description`).

The three tiers must stay visible in the emitted entry. A pipeline that
laundered `derived` and `unverified` into `verified` would score better on any
presence-counting audit — including AFS — while being worth less. Note the
tension frankly: **AFS rewards fields this protocol declines to certify.**

Tick the worklist. Next function.

## Phase 6 — Package audit (once, after the worklist is clear)

`REGISTRY_REPORT.md`: AFS with sub-scores, **contract-verified rate**,
example-runnable rate, coverage (`done` / `skipped` with reasons), and a
proposed-vs-survived table per field.

Gates, from the manifest:

```yaml
gates:
  coverage_min: 0.95
  contract_verified_min: 0.60
  example_runnable_min: 0.80
  afs_min: 0.55
  refuted_survivors: 0      # the only non-negotiable one
```

## Phase 7 — Behavioural evaluation

Static audit is a proxy. The claim "synthesis reaches hand quality" is settled
only by Pass@1 on an agent benchmark with the synthesised registry swapped in
for the hand one, agent and prompt and ranking and formatter held fixed
(`ovagent_bench/scripts/auto_lookup.py` does the swap).

AFS parity is not the target and would be the wrong one: hand's contract
sub-score is inflated by claims that are false, so matching it means matching
its errors. The target is Pass@1 at a materially higher verified rate.

For a library the decorating party does not maintain, the benchmark must also
be one they did not write.

## Cost

Per function: one discovery check, one read, one call to author, ≤ 3 probe
rounds. Sibling reuse (Phase 1.2) collapses most of Phases 2–3 within a
family, so a module of twenty related functions costs far less than twenty
independent functions. Budget the worklist by family, not by count.

## Invocation

```
Decorate <package>. Follow awe-decoratr/PROTOCOL.md.
Work the worklist one function at a time; do not batch.
```

A run whose `ITERATION_LOG.md` contains no Phase 4 blocks did no probing and
fails Gate `refuted_survivors: 0` by construction — there is nothing to have
refuted.
