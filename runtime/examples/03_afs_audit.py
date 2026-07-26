"""Example 3 — Audit your library against the AFS rubric.

Run the audit on whatever you have decorated in the current
process. The report tells you (a) the library-level
Agent-Friendliness Score, (b) the per-component breakdown
(D / C / S / B), and (c) the per-function rows so you can
sort and find the entries that most need more metadata.

Run with:
  python examples/03_afs_audit.py
"""

from awe_agent_function import (
    register_function,
    compute_afs,
)


# A bigger toy library so the per-component breakdown is meaningful.

@register_function(aliases=["pca", "PCA", "principal component analysis"],
                   category="dim_reduction",
                   description="Principal component analysis on a "
                               "feature matrix; returns the projected "
                               "matrix and the explained-variance ratio.",
                   requires={"shape": ["2d_array"]},
                   produces={"attributes": ["components_",
                                            "explained_variance_"]},
                   examples=["fit_pca(X, n_components=10)"],
                   related=["TruncatedSVD", "ICA"],
                   auto_fix="none")
def fit_pca(X, n_components=10):
    """Fit PCA on X."""

@register_function(aliases=["normalize", "L2-normalize", "row-normalize"],
                   category="preprocessing",
                   description="L2-normalize the rows of X.",
                   requires={"shape": ["2d_array"]},
                   produces={"shape": ["2d_array"]},
                   examples=["normalize(X)"],
                   related=["StandardScaler"])
def normalize(X):
    """L2-normalize each row of X."""

@register_function(aliases=["foo"], category="misc",
                   description="A poorly-documented function.")
def foo():                          # no examples, no related, no contract
    """todo"""

@register_function(aliases=["bar", "bar method", "条形"],   # multilingual
                   category="misc",
                   description="Another minimal entry, but with a longer "
                               "description so the discoverability check "
                               "passes the 40-char threshold.",
                   examples=["bar()"],
                   related=["foo"])
def bar():
    """A second toy function."""


def main() -> None:
    rep = compute_afs()
    print(rep.summary())

    print()
    print("=" * 72)
    print("Per-function table (sorted by AFS, lowest first):")
    print("=" * 72)
    rows = sorted(rep.rows, key=lambda r: r["AFS"])
    print(f"{'AFS':>5}  {'D':>5} {'C':>5} {'S':>5} {'B':>5}   {'function'}")
    for r in rows:
        print(f"{r['AFS']:>5.2f}  "
              f"{r['D']:>5.2f} {r['C']:>5.2f} {r['S']:>5.2f} {r['B']:>5.2f}   "
              f"{r['full_name']}")
    print()
    print("Lowest-AFS entries are the next candidates for richer metadata.")


if __name__ == "__main__":
    main()
