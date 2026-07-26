"""@register_function decorator (library-agnostic)."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, Dict, List, Optional

from .registry import get_registry


def register_function(
    aliases: List[str],
    category: str,
    description: str,
    examples: Optional[List[str]] = None,
    related: Optional[List[str]] = None,
    prerequisites: Optional[Dict[str, List[str]]] = None,
    requires: Optional[Dict[str, List[str]]] = None,
    produces: Optional[Dict[str, List[str]]] = None,
    auto_fix: str = "none",
    contract_keys: Optional[set] = None,
):
    """Decorator that promotes a function to a first-class registry entry.

    See README.md for usage and the AFS audit semantics.
    """

    def decorator(func: Callable) -> Callable:
        get_registry().register(
            func,
            aliases=aliases,
            category=category,
            description=description,
            examples=examples,
            related=related,
            prerequisites=prerequisites,
            requires=requires,
            produces=produces,
            auto_fix=auto_fix,
            contract_keys=contract_keys,
        )

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        wrapper._registry_info = {
            "aliases":     aliases,
            "category":    category,
            "description": description,
        }
        return wrapper

    return decorator
