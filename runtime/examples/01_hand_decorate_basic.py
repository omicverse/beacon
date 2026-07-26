"""Example 1 — Hand-decorate your own functions.

The canonical A3F usage: a library author adds @register_function at
each public-API call site so an LLM agent can find the function by
natural-language query rather than by `grep`. Run with:

  python examples/01_hand_decorate_basic.py
"""

from awe_agent_function import (
    register_function,
    registry_lookup,
    registry_summary,
    compute_afs,
)


# ---------------------------------------------------------------------------
# Two functions on a toy "stats" library, decorated to A3F-friendly depth.
# ---------------------------------------------------------------------------


@register_function(
    aliases=["zscore", "standard score", "z-score", "标准化"],
    category="preprocessing",
    description=("Convert a 1-D numeric array to its z-score "
                 "(zero mean, unit variance)."),
    requires={"shape": ["1d_array"]},
    produces={"shape": ["1d_array"], "metrics": ["mean=0", "std=1"]},
    examples=[
        "zscore([1, 2, 3, 4, 5])  # array([-1.41, -0.71, 0.0, 0.71, 1.41])",
        "zscore(np.random.randn(100))",
    ],
    related=["minmax_scale", "robust_scale"],
    auto_fix="none",
)
def zscore(x):
    """Compute the z-score of *x*."""
    import numpy as np
    x = np.asarray(x, dtype=float)
    mu = x.mean()
    sd = x.std(ddof=0)
    return (x - mu) / (sd if sd else 1.0)


@register_function(
    aliases=["welch_ttest", "welch t-test", "two-sample t-test (unequal var)",
             "ttest_ind"],
    category="statistics",
    description="Two-sample Welch's t-test (does not assume equal variance).",
    requires={"shape": ["1d_array", "1d_array"]},
    produces={"fields": ["t_stat", "p_value", "df"]},
    prerequisites={"optional_functions": ["zscore"]},
    examples=[
        "welch_ttest(group_a, group_b)  # → {'t_stat': 2.31, 'p_value': 0.022, …}",
    ],
    related=["mannwhitneyu", "permutation_test"],
    auto_fix="none",
)
def welch_ttest(a, b):
    """Welch's t-test for two independent samples with unequal variance."""
    import numpy as np
    from math import sqrt
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1), b.var(ddof=1)
    se = sqrt(va / na + vb / nb)
    t = (a.mean() - b.mean()) / se
    df = (va / na + vb / nb) ** 2 / (
        (va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1)
    )
    return {"t_stat": t, "df": df}


# ---------------------------------------------------------------------------
# What an LLM agent would do at plan time
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 72)
    print("registry_summary():")
    print("=" * 72)
    print(registry_summary())

    print()
    print("=" * 72)
    print("registry_lookup('z-score'):")
    print("=" * 72)
    print(registry_lookup("z-score"))

    print()
    print("=" * 72)
    print("registry_lookup('two-sample test for unequal variance'):")
    print("=" * 72)
    print(registry_lookup("two-sample test for unequal variance"))

    print()
    print("=" * 72)
    print("compute_afs() — audit:")
    print("=" * 72)
    print(compute_afs().summary())


if __name__ == "__main__":
    main()
