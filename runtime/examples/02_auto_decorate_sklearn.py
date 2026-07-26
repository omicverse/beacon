"""Example 2 — Auto-decorate a foreign package (sklearn) at runtime.

This is the headline of §7.3 in the paper: A3F applies to any
Python package without modifying its source. We walk sklearn's
public surface, AST-extract each callable's signature + docstring,
and synthesise registry entries. The result is queryable by
exactly the same `registry_lookup` API that a hand-decorated
library exposes.

Run with:
  python examples/02_auto_decorate_sklearn.py
"""

import warnings

warnings.filterwarnings("ignore")

from awe_agent_function import (
    auto_decorate,
    registry_lookup,
    registry_summary,
    compute_afs,
)


def main() -> None:
    print("[*] auto-decorating sklearn (this takes ~10 s) …")
    n = auto_decorate("sklearn", recurse_depth=2)
    print(f"[*] registered {n} sklearn entries.")

    print()
    print("[*] AFS audit:")
    rep = compute_afs(library_name="sklearn")
    print(rep.summary())

    print()
    queries = [
        "random forest classifier",
        "feature selection wrapper",
        "principal component analysis",
        "stratified k-fold cross validation",
        "silhouette score for clustering",
    ]
    for q in queries:
        print()
        print("=" * 72)
        print(f"registry_lookup({q!r}):")
        print("=" * 72)
        print(registry_lookup(q, max_results=2))


if __name__ == "__main__":
    main()
