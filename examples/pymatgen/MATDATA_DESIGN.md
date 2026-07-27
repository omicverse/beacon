# MatData — annotated data for materials workflows

## Why this exists

The feasibility probe in `feasibility.py` failed, and how it failed is the
argument for this design. Eight `pymatgen` operations, three probe strategies,
**zero observable state changes** — including operations that mutate in place:

```
function                          in_place  fold_back  return_diff
make_supercell                           0          0            0
get_primitive_structure                  0          0            0
add_site_property                        0          0            0
```

The cause is not "returns a new object". A `Structure` always has the same
attributes. `make_supercell` takes 8 sites to 16 and doubles the volume, but
`lattice`, `sites`, `volume` and `composition` were all there before and are
all there after. **Nothing appears.**

Beacon's contract vocabulary — `requires` / `produces` as sets of container
keys — is built on keys appearing. AnnData supplies that: `obsm['X_pca']`
genuinely does not exist until `pp.pca` runs, which is why the oracle confirms
27 contracts on `omicverse` and none here. The blocker is not the adapter and
not the library; materials Python has no container whose slots are named,
addressable and observably filled.

## Revised recommendation: do not write a new class

The first draft of this document proposed a new `MatData` container. Checking
the ecosystem first changed that conclusion, and the reason is worth stating
plainly: **the axis choice this design needs is already the community's de
facto convention, and AnnData has meanwhile grown out of its biology-shaped
assumptions.**

- `matminer`, the standard featurization toolkit, works on a **pandas
  DataFrame with a `structure` column** of pymatgen objects; `featurize_dataframe`
  appends feature columns. Rows are materials, columns are features — exactly
  the axis assignment argued for below, already in use.
- AnnData now accepts **xarray Datasets for `obs`/`var`/`obsm`/`varm`**
  (experimental `Dataset2D`), so its slots are no longer tied to the
  cells × genes shape.

So the proposal becomes a **convention plus adapters over AnnData itself**, not
a new format. That matters for three practical reasons: Beacon's existing
`AnnDataAdapter` works unchanged, `h5ad`/`zarr` on-disk comes free, and a
convention that reads existing matminer DataFrames has a chance of being
adopted, whereas a new container competing with `pymatgen`, ASE and OPTIMADE
does not.

## Slot assignment

```
AnnData, under the materials convention
├── X            (M × K)   feature matrix; often empty at load
├── obs          (M)       formula, spacegroup, e_above_hull, band_gap, mp_id
├── var          (K)       units, source, featurizer that produced the column
├── obsm         (M × d)   X_soap, X_matminer, X_pca
├── obsp         (M × M)   structure_similarity, hull_adjacency
├── layers       (M × K)   the same quantities at a different level of theory
└── uns
    ├── structures         M serialised structures (OPTIMADE-shaped)
    ├── sites              ragged per-site frames: forces, magmoms, charges
    ├── calc               per-layer calculator parameters
    └── phase_diagram, bandstructure, provenance
```

`structures` and `sites` live in `uns` rather than as new top-level slots
precisely so this stays *AnnData*, readable by any tool that speaks h5ad.

## `layers` carries the level of theory

The slot that earns its keep here and has no single-cell equivalent worth the
name. The same M × K quantities computed differently:

```python
md.layers["pbe"]         # DFT, PBE functional
md.layers["hse06"]       # hybrid
md.layers["mace"]        # ML interatomic potential — a surrogate
md.layers["experiment"]  # measured
```

A formation energy is meaningless without its functional, pseudopotential,
cutoff and k-point mesh. Putting the level of theory in the *slot name* and its
parameters in `uns["calc"][layer]` makes provenance structural rather than
conventional. An agent that writes into `layers["mace"]` and reads from
`layers["pbe"]` has made a category error the container can catch — which is
the "surrogate ≠ DFT" discipline, enforced rather than documented.

## Compatibility with what already exists

| Source | Shape it already has | Maps to |
|---|---|---|
| **matminer** | DataFrame, `structure` column + appended feature columns | `uns['structures']` + `X`/`var`; `featurize_dataframe` becomes a deposit |
| **ASE `db`** | rows; `key_value_pairs` (scalars only), `data` (blobs), `Atoms.arrays` (per-atom), `Atoms.info` | `obs` ← key_value_pairs (the scalar restriction matches a DataFrame exactly); `uns['sites']` ← arrays; `uns` ← data |
| **OPTIMADE** | `cartesian_site_positions` (nsites × 3), `species_at_sites`, `species`, entry properties | `uns['structures']` serialisation format; entry properties (`nsites`, `chemical_formula_*`, `elements`) become `obs` columns with standard names |
| **pymatgen `ComputedEntry`** | energy + calculation parameters | `obs['energy']` + `uns['calc']` |

Two things fall out of this table that were not obvious before checking:

**ASE's scalar restriction on `key_value_pairs` is the same restriction a
DataFrame column has**, and ASE's own answer to "too many ML features" is to
move them to a separate table — which is what `obsm` is. The two designs
converged independently.

**OPTIMADE should be the serialisation for `uns['structures']`**, not a
pymatgen pickle. It is the interchange standard, it is already the format MP
and the other providers emit, and it keeps the container readable without
pymatgen installed.

Adapters to write, in priority order:

```python
from_matminer_df(df, structure_col="structure")   # the highest-value one
from_ase_db(path)
from_optimade(response)
to_matminer_df(md)                                 # round-trip, or adoption is a dead end
```

`from_matminer_df` matters most: it means an existing matminer workflow becomes
a `MatData` for free, and the convention costs its first user nothing.

## Structure transforms must deposit, not return

The probe failure says `get_primitive_structure` produces nothing observable.
Under this convention it does, provided transforms **deposit**:

```python
mt.primitive(md)           # produces: uns['structures_primitive']
mt.relax(md, calc='mace')  # produces: uns['structures_relaxed_mace'],
                           #           layers['mace'], uns['sites']['forces_mace']
```

This is the move `scanpy` made with `adata.layers['scaled']` instead of
returning a scaled matrix, and it is the entire reason single-cell contracts
are checkable. Adopting it is not cosmetic — it is the difference between a
probe that can refute and one that cannot.

## What becomes observable

Each of these is then a falsifiable `produces` claim, checkable by the probes
already in `engine/state_probe.py` with the existing `anndata` adapter:

| operation | produces |
|---|---|
| MP / OPTIMADE query | `uns['structures']`, `obs['mp_id','formula','e_above_hull']` |
| matminer featurize | `X`, `var['featurizer']` |
| SOAP descriptor | `obsm['X_soap']` |
| convex hull | `obs['e_above_hull']`, `uns['phase_diagram']` |
| ML relaxation | `uns['structures_relaxed_mace']`, `layers['mace']` |
| band structure | `uns['bandstructure']`, `obs['band_gap']` |
| similarity graph | `obsp['structure_similarity']` |

And `requires` becomes checkable by removal: delete `obsm['X_soap']` and the
prediction step must fail — the test the current pymatgen surface cannot
support at all.

## Honest costs

**Ragged per-site data is where the analogy strains.** Materials have different
atom counts, so `uns['sites']` is a list of frames and loses vectorisation.
AnnData sidesteps this by never having the problem. ASE solves it by keeping
per-atom data on the `Atoms` object rather than in the table, which is the same
compromise.

**A convention nobody writes into is worth nothing.** The adoption path runs
through `from_matminer_df` and round-tripping, not through asking anyone to
switch containers.

**It does not rescue the general claim.** Beacon working on materials *because
we supplied the container it needs* is weaker than Beacon working on materials
as they are. The honest framing: the contract abstraction requires a state
model with named, addressable slots; where a domain lacks one, the abstraction
does not transfer until the domain grows one. That is a real boundary, and more
useful stated than hidden.

## Cheapest next step

Not the container. The **smallest thing that tests the claim**: `from_matminer_df`
plus three deposit-style operations (featurize, hull, relax), then re-run
`feasibility.py` against them. If the probes confirm contracts they currently
cannot see, the design is validated cheaply and the rest is engineering. If
they still cannot, the problem was never the container.

## Sources

- [matminer documentation](https://hackingmaterials.lbl.gov/matminer/) —
  DataFrame + `structure` column convention, `featurize_dataframe`
- [ASE database](https://wiki.fysik.dtu.dk/~askhl/ase-doc/ase/db/db.html) —
  `key_value_pairs` scalar restriction, `data`, external feature tables
- [OPTIMADE structures schema](https://www.optimade.org/optimade-python-tools/0.12.6/api_reference/models/structures/)
  — `cartesian_site_positions`, `species_at_sites`, `species`
- [anndata](https://anndata.readthedocs.io/) — slot semantics; xarray
  `Dataset2D` support for `obs`/`var`/`obsm`/`varm`
