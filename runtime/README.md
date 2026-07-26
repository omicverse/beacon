# awe-agent-function

A library-agnostic implementation of the **Agent-Friendly Function
Framework (A3F)**: a single decorator that promotes any Python
function to an LLM-discoverable artifact carrying aliases, data-shape
contracts, and dispatch alternatives, plus two natural-language
lookup APIs that surface the registry to an agent at planning time.

This package extracts the core machinery from `omicverse._registry`
and `omicverse.utils.ovagent.registry_scanner` and ships it without
the AnnData / scverse dependencies — it works on *any* Python
package, whether the package adopts the decorator at the call site
or whether you auto-decorate a foreign package at runtime.

## Two ways to use it

**1. Direct decoration** (your library):

```python
from awe_agent_function import register_function, registry_lookup

@register_function(
    aliases=["pca", "PCA", "principal component analysis"],
    category="preprocessing",
    description="Principal component analysis on a feature matrix.",
    requires={"shape": ["2d_array"]},
    produces={"attributes": ["components_", "explained_variance_"]},
    examples=["PCA(n_components=10).fit_transform(X)"],
    auto_fix="none",
)
def pca(X, n_components=10): ...

# At plan time, an agent (or you) queries:
print(registry_lookup("pca"))           # which API + signature
print(registry_lookup("dimensionality reduction"))
```

**2. Auto-decoration** (foreign library, no source mod):

```python
from awe_agent_function import auto_decorate, registry_lookup

# Walks the public API of a foreign package and synthesises a
# registry entry for every public function / class.
auto_decorate("sklearn", recurse_depth=2)

print(registry_lookup("classification"))
print(registry_lookup("ensemble"))
```

The auto-decorator inspects each public callable, extracts a
description from the docstring's first sentence, an `Examples`
section if present, a `See Also` list as `related`, and tokenizes
the dotted module path and the camelCase / snake_case name into
synthetic aliases. The resulting registry is queryable by exactly
the same API — `registry_lookup`, `registry_summary` — as a
hand-decorated library.

## Quantitative audit (AFS)

```python
from awe_agent_function import compute_afs

afs = compute_afs("my_library")        # mean Agent-Friendliness Score
print(afs.summary())                   # per-component sub-scores
```

## License

MIT.
