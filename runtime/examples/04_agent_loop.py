"""Example 4 — Drop A3F into a single-tool agent loop.

This is the minimal pattern an agent harness uses to surface the
registry to a chat-completion API. The harness prepares two prompts
that differ only in whether `registry_lookup` is mentioned, runs
the same task in both arms, and the registry tools are invoked from
inside the model's Python tool — no special tool-calling protocol
needed.

This file does NOT call any LLM (so it has no credentials, no API
key, no network dependency). It prints the *system prompts* and the
single-line invocation an agent would actually make. Drop these
prompts into any chat-completion harness (DeepSeek, OpenAI,
Anthropic, …) to reproduce the §7.3 sklearn ablation.

Run with:
  python examples/04_agent_loop.py
"""

import warnings

warnings.filterwarnings("ignore")

from awe_agent_function import auto_decorate, registry_lookup, registry_summary


SYSTEM_BASELINE = """\
You are a coding assistant. You have one tool: a Python interpreter.
End each reply with a fenced ```python``` block to call it.
The interpreter keeps state across turns.
"""


SYSTEM_PLUS_REGISTRY = SYSTEM_BASELINE + """\

You also have access to a function registry over the public API of
the target package. Inside your Python tool you can call:

  from awe_agent_function import registry_lookup, registry_summary
  print(registry_lookup("classification with hyperparameter selection"))

The registry returns the function's full name, signature, an example
call, and a See-Also list. Budget 1–3 lookup calls before writing your
solution; this is much cheaper than guessing API names.
"""


def main() -> None:
    print("[*] auto-decorating sklearn …")
    n = auto_decorate("sklearn", recurse_depth=2)
    print(f"[*] registered {n} entries.")

    print()
    print("=" * 72)
    print("BASELINE system prompt (no registry exposed):")
    print("=" * 72)
    print(SYSTEM_BASELINE)

    print("=" * 72)
    print("+REGISTRY system prompt (registry exposed):")
    print("=" * 72)
    print(SYSTEM_PLUS_REGISTRY)

    print("=" * 72)
    print("Sample first agent turn ( + registry arm):")
    print("=" * 72)
    print(
        "> Train a classifier on the canonical Iris dataset with\n"
        "> hyperparameter selection; return final_model + final_acc.\n"
        "\n"
        "```python\n"
        "from awe_agent_function import registry_lookup\n"
        "print(registry_lookup('classification with hyperparameter selection'))\n"
        "```\n"
    )

    print("=" * 72)
    print("Live demo — what the +registry arm actually receives back:")
    print("=" * 72)
    print(registry_lookup("classification with hyperparameter selection",
                          max_results=2))


if __name__ == "__main__":
    main()