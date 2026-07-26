# Examples

Four runnable demos, ordered from simplest to most realistic.

| File | Demonstrates |
|------|-------------|
| `01_hand_decorate_basic.py` | Author-side usage: `@register_function` on two toy `stats` functions, then `registry_lookup` and a one-paragraph AFS audit. |
| `02_auto_decorate_sklearn.py` | Library-agnostic usage: walk `sklearn`'s public surface at runtime (no source mod), register 540+ entries, query several natural-language prompts. |
| `03_afs_audit.py` | The AFS audit on a deliberately heterogeneous toy library — including a poorly-documented function `foo` so the per-function table shows the gradient the audit is meant to surface. |
| `04_agent_loop.py` | Drop-in pattern for an LLM agent harness: the two system prompts that differ only in whether `registry_lookup` is exposed, plus a live demo of what the agent reads back. No API key required — paste the prompts into any chat-completion harness to reproduce §7.3. |

Run any of them with the project's venv:

```
cd awe-agent-function
pip install -e .
python examples/01_hand_decorate_basic.py
python examples/02_auto_decorate_sklearn.py
python examples/03_afs_audit.py
python examples/04_agent_loop.py
```

The §7.3 cross-library validation (DeepSeek API ablation against the
sklearn mini-bench) lives at
`../../sklearn_bench/run_ablation.py` — that script is the
end-to-end runner; the examples here cover the standalone components
of the package.
