"""Natural-language lookup APIs for the agent.

`registry_lookup(query)` returns a Markdown-style string designed to
land directly in an agent's bash tool result. `registry_summary()`
returns a category-level overview.
"""

from __future__ import annotations

from typing import Optional

from .registry import get_registry


def registry_lookup(query: str, max_results: int = 8, verbose: bool = True) -> str:
    """Search the registry and return a formatted result string."""

    registry = get_registry()
    matches = registry.find(query)
    if not matches:
        return f"No registered functions found for query {query!r}."

    matches = matches[:max_results]
    out: list[str] = [f"Found {len(matches)} matching function(s) for {query!r}:"]
    for i, e in enumerate(matches, 1):
        out.append("")
        out.append(f"[{i}] {e['full_name']}")
        out.append(f"    desc:      {e['description']}")
        if e.get("aliases"):
            out.append(f"    aliases:   {', '.join(e['aliases'])}")
        out.append(f"    category:  {e['category']}")
        out.append(f"    signature: {e.get('signature', '(...)')}")
        if verbose:
            if e.get("examples"):
                out.append("    examples:")
                for ex in e["examples"][:3]:
                    out.append(f"       {ex}")
            if e.get("related"):
                out.append(f"    related:   {', '.join(e['related'][:6])}")
            req = e.get("requires") or {}
            prod = e.get("produces") or {}
            if req:
                req_pairs = []
                for k, vs in req.items():
                    for v in vs:
                        req_pairs.append(f"{k}:{v}")
                out.append(f"    requires:  {', '.join(req_pairs)}")
            if prod:
                prod_pairs = []
                for k, vs in prod.items():
                    for v in vs:
                        prod_pairs.append(f"{k}:{v}")
                out.append(f"    produces:  {', '.join(prod_pairs)}")
    return "\n".join(out)


def registry_summary() -> str:
    """Category-level overview of the registry."""

    registry = get_registry()
    lines: list[str] = []
    for cat in sorted(registry.list_categories()):
        items = registry.get_by_category(cat)
        names = [e.get("short_name", "") for e in items]
        sample = ", ".join(n for n in names[:5] if n)
        suffix = f" (+{len(names) - 5} more)" if len(names) > 5 else ""
        lines.append(f"- {cat} ({len(names)} functions): {sample}{suffix}")
    return "\n".join(lines) if lines else "Registry is empty."
