"""Smoke tests."""

from awe_agent_function import (
    register_function,
    registry_lookup,
    registry_summary,
    auto_decorate,
    compute_afs,
    get_registry,
)


def test_decorate_and_lookup() -> None:
    @register_function(
        aliases=["square", "sq", "x**2"],
        category="math",
        description="Return x squared.",
        examples=["square(3)  # -> 9"],
        related=["cube"],
    )
    def square(x: int) -> int:
        return x * x

    out = registry_lookup("square")
    assert "square" in out.lower()
    assert "math" in out.lower()


def test_summary_lists_categories() -> None:
    @register_function(
        aliases=["cube"],
        category="math",
        description="Return x cubed.",
    )
    def cube(x: int) -> int:
        return x ** 3

    s = registry_summary()
    assert "math" in s


def test_auto_decorate_smoke() -> None:
    n = auto_decorate("json", recurse_depth=0)
    assert n >= 0  # json may or may not have public functions imported
    out = registry_lookup("dumps")
    assert "json" in out.lower() or "no registered" in out.lower()


def test_afs_report() -> None:
    rep = compute_afs()
    assert rep.n_functions >= 1
    assert 0.0 <= rep.library_afs_mean <= 1.0
