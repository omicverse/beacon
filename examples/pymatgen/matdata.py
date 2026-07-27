"""MatData prototype — the materials convention over AnnData.

Not a new container. AnnData is the substrate; this module supplies the slot
convention and the deposit-style operations that make materials workflows
observable to a probe. ~200 lines, written to be falsified cheaply: if the
probes in ``engine/state_probe.py`` still cannot confirm a contract under this
convention, the container was never the problem.

Slot convention
---------------
``obs``    one row per material: formula, nsites, energy, e_above_hull
``var``    one row per feature: the featurizer that produced it, units
``X``      M x K feature matrix
``obsm``   descriptors and embeddings
``layers`` the same M x K quantities at a different level of theory
``uns['structures']``  the raw objects, keyed by variant name
``uns['calc']``        per-layer calculator parameters

``structures`` sits in ``uns`` rather than as a new top-level attribute so this
stays *AnnData* — readable by anything that speaks h5ad, and probeable by the
adapter Beacon already has.

The one rule that matters
-------------------------
Operations **deposit**; they do not return. ``primitive(md)`` writes
``uns['structures']['primitive']`` and returns nothing useful. This is the move
scanpy made with ``adata.layers['scaled']``, and it is the entire reason
single-cell contracts are checkable: a key that did not exist now does.
"""

from __future__ import annotations

from typing import Any, Iterable

import numpy as np
import pandas as pd
from anndata import AnnData

try:
    from pymatgen.core import Composition, Structure
except Exception:                                     # probe env without pymatgen
    Structure = Composition = None                    # type: ignore


# --------------------------------------------------------------------------
# Construction
# --------------------------------------------------------------------------

def from_matminer_df(
    df: pd.DataFrame,
    structure_col: str = "structure",
    feature_cols: Iterable[str] | None = None,
) -> AnnData:
    """Adopt an existing matminer-style DataFrame.

    matminer's convention — a DataFrame with a ``structure`` column of pymatgen
    objects, feature columns appended by ``featurize_dataframe`` — is already
    "rows are materials, columns are features". This reads it as-is, so the
    convention costs its first user nothing. Round-tripping via
    ``to_matminer_df`` is what keeps that true; a one-way adapter is an
    adoption dead end.
    """
    if structure_col not in df.columns:
        raise KeyError(f"no {structure_col!r} column; matminer's convention is a "
                       f"DataFrame with pymatgen Structures in {structure_col!r}")
    structures = list(df[structure_col])
    meta_cols = [c for c in df.columns if c != structure_col]
    if feature_cols is None:
        feature_cols = [c for c in meta_cols
                        if pd.api.types.is_numeric_dtype(df[c])]
    feature_cols = list(feature_cols)
    obs_cols = [c for c in meta_cols if c not in feature_cols]

    X = df[feature_cols].to_numpy(dtype=float) if feature_cols else np.zeros((len(df), 0))
    md = AnnData(
        X=X,
        obs=df[obs_cols].reset_index(drop=True) if obs_cols else pd.DataFrame(index=range(len(df))),
        var=pd.DataFrame(index=pd.Index(feature_cols, name="feature")),
    )
    md.obs_names = [str(i) for i in range(len(df))]
    md.uns["structures"] = {"input": structures}
    md.uns["calc"] = {}
    md.uns["provenance"] = ["from_matminer_df"]
    return md


def to_matminer_df(md: AnnData, variant: str = "input") -> pd.DataFrame:
    """Round-trip back to the convention the ecosystem already reads."""
    df = md.obs.copy().reset_index(drop=True)
    df.insert(0, "structure", list(md.uns["structures"][variant]))
    feat = md.uns.get("features", {}).get("X_composition")
    if feat is not None:
        for i, name in enumerate(feat["names"]):
            df[name] = md.obsm["X_composition"][:, i]
    return df


def from_structures(structures: list, obs: pd.DataFrame | None = None) -> AnnData:
    """Build from bare pymatgen Structures — the MP-query entry point."""
    obs = obs if obs is not None else pd.DataFrame(index=range(len(structures)))
    md = AnnData(X=np.zeros((len(structures), 0)), obs=obs.reset_index(drop=True))
    md.obs_names = [str(i) for i in range(len(structures))]
    md.uns["structures"] = {"input": list(structures)}
    md.uns["calc"] = {}
    md.uns["provenance"] = ["from_structures"]
    return md


# --------------------------------------------------------------------------
# Deposit-style operations
# --------------------------------------------------------------------------

def describe(md: AnnData, variant: str = "input") -> None:
    """Per-material scalars. Deposits into ``obs``.

    produces: obs['formula'], obs['nsites'], obs['volume'], obs['density']
    """
    S = md.uns["structures"][variant]
    md.obs["formula"] = [s.composition.reduced_formula for s in S]
    md.obs["nsites"] = [len(s) for s in S]
    md.obs["volume"] = [float(s.volume) for s in S]
    md.obs["density"] = [float(s.density) for s in S]
    md.uns["provenance"].append(f"describe({variant})")


def featurize(md: AnnData, variant: str = "input") -> None:
    """Composition descriptors. Deposits into ``X`` / ``var`` / ``obsm``.

    Features go to ``obsm``, not ``X``. Discovered by testing rather than
    assumed: AnnData ties ``X``'s width to ``var``, so ``md.X = Xf`` on a
    container built with zero features raises ``Data matrix has wrong shape``.
    A deposit-style convention must therefore write features somewhere whose
    width is free, and ``obsm`` is exactly that. ``X`` stays empty; the feature
    names live in ``uns['features']``.

    requires: uns['structures'][variant]
    produces: obsm['X_composition'], uns['features']
    """
    S = md.uns["structures"][variant]
    rows, names = [], ["mean_atomic_mass", "mean_electronegativity",
                       "n_elements", "volume_per_atom"]
    for s in S:
        comp: Any = s.composition
        els = list(comp.elements)
        en = [e.X for e in els if e.X is not None]
        rows.append([
            float(comp.weight / comp.num_atoms),
            float(np.mean(en)) if en else np.nan,
            float(len(els)),
            float(s.volume / len(s)),
        ])
    Xf = np.asarray(rows, dtype=float)
    md.obsm["X_composition"] = Xf
    md.uns["features"] = {"X_composition": {"names": names,
                                            "featurizer": "matdata.featurize"}}
    md.uns["provenance"].append(f"featurize({variant})")


def primitive(md: AnnData, source: str = "input") -> None:
    """Reduce each structure. Deposits a new structure variant.

    This is the operation the bare-pymatgen probe could not see at all:
    ``get_primitive_structure`` returns a new object and changes no attribute
    name, so nothing appears. Depositing it under a name makes it appear.

    requires: uns['structures'][source]
    produces: uns['structures']['primitive'], obs['nsites_primitive']
    """
    S = md.uns["structures"][source]
    prim = [s.get_primitive_structure() for s in S]
    md.uns["structures"]["primitive"] = prim
    md.obs["nsites_primitive"] = [len(s) for s in prim]
    md.uns["provenance"].append(f"primitive({source})")


def energy_model(md: AnnData, layer: str = "toy", **params) -> None:
    """Stand-in for an ML potential or a DFT run, at a named level of theory.

    The point of the ``layer`` argument is provenance: a formation energy is
    meaningless without its functional, pseudopotential, cutoff and k-points.
    Putting the level of theory in the *slot name* and its parameters in
    ``uns['calc'][layer]`` makes that structural rather than conventional — an
    agent that writes ``layers['mace']`` and reads ``layers['pbe']`` has made a
    category error the container can catch.

    requires: obsm['X_composition']
    produces: obsm[f'energy_{layer}'], obs[f'energy_{layer}'], uns['calc'][layer]
    """
    if "X_composition" not in md.obsm:
        raise ValueError("energy_model requires obsm['X_composition']; run featurize() first")
    Z = np.nan_to_num(md.obsm["X_composition"], nan=0.0)
    w = np.linspace(1.0, 0.1, Z.shape[1])
    e = Z @ w
    md.obsm[f"energy_{layer}"] = Z * w
    md.obs[f"energy_{layer}"] = e
    md.uns["calc"][layer] = {"model": "toy-linear", **params}
    md.uns["provenance"].append(f"energy_model(layer={layer})")


def convex_hull(md: AnnData, layer: str = "toy") -> None:
    """Stability relative to the lowest-energy structure per composition.

    requires: obs[f'energy_{layer}']
    produces: obs['e_above_hull'], uns['phase_diagram']
    """
    key = f"energy_{layer}"
    if key not in md.obs:
        raise ValueError(f"convex_hull requires obs[{key!r}]; run energy_model first")
    if "formula" not in md.obs:
        describe(md)
    e = md.obs[key].to_numpy(dtype=float)
    per_formula = pd.Series(e).groupby(md.obs["formula"].values).min()
    md.obs["e_above_hull"] = e - md.obs["formula"].map(per_formula).to_numpy(dtype=float)
    md.uns["phase_diagram"] = {"layer": layer,
                               "minima": {k: float(v) for k, v in per_formula.items()}}
    md.uns["provenance"].append(f"convex_hull(layer={layer})")


def similarity(md: AnnData) -> None:
    """Pairwise structural similarity. Deposits into ``obsp``.

    requires: obsm['X_composition']
    produces: obsp['structure_similarity']
    """
    if "X_composition" not in md.obsm:
        raise ValueError("similarity requires obsm['X_composition']")
    Z = np.nan_to_num(md.obsm["X_composition"], nan=0.0)
    Z = Z / (np.linalg.norm(Z, axis=1, keepdims=True) + 1e-12)
    md.obsp["structure_similarity"] = Z @ Z.T
    md.uns["provenance"].append("similarity()")


__all__ = ["from_matminer_df", "to_matminer_df", "from_structures",
           "describe", "featurize", "primitive", "energy_model",
           "convex_hull", "similarity"]
