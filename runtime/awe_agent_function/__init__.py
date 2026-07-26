"""awe-agent-function: the Agent-Friendly Function Framework, packaged.

Public API:

  register_function     - the @decorator
  registry_lookup       - natural-language search over the registry
  registry_summary      - category-level overview
  auto_decorate         - synthesise registry entries from a foreign package
  compute_afs           - run the AFS audit
  get_registry          - access the singleton registry
"""

from .decorator import register_function
from .registry import FunctionRegistry, get_registry
from .lookup import registry_lookup, registry_summary
from .auto_decorate import auto_decorate
from .afs import compute_afs, AFSReport, Subscores, score_entry

__all__ = [
    "register_function",
    "registry_lookup",
    "registry_summary",
    "auto_decorate",
    "compute_afs",
    "AFSReport",
    "Subscores",
    "score_entry",
    "FunctionRegistry",
    "get_registry",
]

__version__ = "0.1.0"
