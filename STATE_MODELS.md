# State models

`requires` and `produces` are claims about what a call reads and writes. That
sentence has no meaning until "state" is defined, and state is the one thing
scientific libraries do *not* agree on. An adapter supplies that definition for
one library shape; the protocol and the probes are written against the adapter,
so a new library needs a new adapter, not a new protocol.

This is also the honest answer to the generality question. A framework whose
contract vocabulary is the seven AnnData containers is a framework for AnnData.
Naming the state model as a pluggable component is what makes the claim
"library-side contracts help agents" separable from "AnnData has a convenient
shape."

## The four shapes

| Shape | The state is | Removal means | Examples |
|---|---|---|---|
| **central container** | keys inside one mutable object threaded through every call | `del container[key]` | AnnData: `omicverse`, `scanpy`, `muon` |
| **object-centric** | the public attribute surface of the subject and of the returned object | `delattr` | `pymatgen.Structure`, `rdkit.Mol`, `ase.Atoms` |
| **namespace** | bindings created in an execution scope | `del ns[name]` | `sklearn`, `scipy`, `numpy` |
| **side-effecting** | files written under a working directory | `os.remove` | `atomate2`, `quacc`, VASP/QE wrappers |

`anndata` is the easy case and the one the paper's evidence comes from. The
other three are where the design is actually tested.

## The adapter contract

Two methods. Both are deliberately minimal, because everything else the probes
need is already in `state_probe.py`.

```python
class StateAdapter(Protocol):
    name: str

    def snapshot(self, subject) -> dict[str, set[str]]:
        """Container -> set of keys present right now."""

    def strip(self, subject, container: str, key: str) -> bool:
        """Remove key. Return False if it was not there to remove."""
```

`snapshot` must be **cheap and total** — probes call it twice per trial, and a
partial snapshot silently converts "produced" into "not observed."

`strip` must return `False` rather than raise when a key cannot be removed.
That distinction carries real information: a read-only property that cannot be
deleted is *unremovable*, which the prover records as inconclusive. Reporting
it as "removal did not break the call" would silently admit the opposite claim.

## Why object-centric libraries are the hard case

For AnnData, the subject before and after a call is the same object, so
`snapshot(subject)` twice is well defined. For `pymatgen` it usually is not:

```python
structure = Structure.from_file("Si.cif")
primitive = structure.get_primitive_structure()   # new object, input untouched
```

Nothing was written *into* `structure`. The produced state is the returned
object's attribute surface, and the meaningful diff is between the input's
surface and the output's — not before/after on one object.

`AttrsAdapter` therefore expects the caller's `call` to hand the returned
object back as the post-state subject. Concretely, in the manifest's
`make_subject` / call wiring:

```python
def call(subject):
    out = subject.get_primitive_structure()
    subject.__dict__.update(               # fold the result back in so the
        {k: getattr(out, k) for k in dir(out) if not k.startswith("_")}
    )
```

This is a wrapper concern, not an adapter concern, and it is the single most
common way to get a wrong `produces` on an object-centric library: probe the
input, see nothing change, and conclude the function produces nothing.

## Writing a new adapter

1. Decide what a *key* is. It must be a string an agent could plausibly write
   in code — `obsm['X_pca']`, a `Structure.lattice` attribute, an output
   filename. If the key is not addressable by the agent, it does not belong in
   a contract.
2. Implement `snapshot`. Prefer over-collecting: a key that appears in the
   snapshot but is never claimed shows up as an *under-declaration* report,
   which is useful. A key missing from the snapshot silently refutes true
   claims, which is not.
3. Implement `strip`, returning `False` for unremovable keys.
4. Add it to `ADAPTERS` in `state_probe.py`.
5. Extend `engine/smoke_test.py` with a case where a claim is **true** and one
   where it is **false**, and check the probes separate them. An adapter that
   cannot refute is worse than no adapter: it manufactures confirmations.

Step 5 is the acceptance test. The smoke test already does this for
`namespace`; copy the pattern.

## Known limits

- **Lazy / deferred computation.** Dask-backed or lazily-evaluated results may
  not materialise inside the probe window, so `produces` under-reports. Force
  computation inside the `call` wrapper.
- **Global side effects.** Libraries that mutate module-level configuration
  (`scanpy.settings`, matplotlib rcParams) hold state no adapter above sees.
  Such functions come back with empty contracts, which is honest but
  incomplete.
- **Randomness.** A probe result that depends on a seed is not a contract.
  Pin the seed in the fixture; if a `produces` key appears only sometimes, it
  is inconclusive, not confirmed.
- **Cost.** `probe_requires` is `O(number of claimed keys)` full re-runs. On
  expensive functions (DFT wrappers, deep-learning inference) budget the probe
  or restrict the claim set. This is the main scaling obstacle for the
  `filesystem` shape, where a single trial can be a compute job.
