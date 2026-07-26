# omicverse — worked example and the evidence behind it

`decorations_auto.py` (330 entries) and `auto_entries.json` are the output of
running this framework against `omicverse`, and the input to the head-to-head
benchmark below. Nothing here was hand-written.

## What the probes established

| | n |
|---|---:|
| entries | 330 |
| probe-verified `requires` / `produces` | 27 |
| ablation-confirmed `prerequisites` | 11 |
| derived `auto_fix` (policy, marked `derived` not `verified`) | 10 |
| real tutorial examples | 215 |
| **refuted claims surviving into the output** | **0** |

## Behavioural result

`deepseek-v4-flash`, 38 tasks x 3 seeds, 101 paired cells. Agent, prompt,
ranking function and output formatter held fixed; only the entry source
varies.

| registry | Pass@1 | vs baseline |
|---|---:|---:|
| none (baseline) | 73.2 % | — |
| **auto (this framework)** | **80.7 %** | **+7.5** |
| hand (445 author-written entries) | 86.8 % | +13.6 |

Auto recovers 55 % of the hand-written registry's uplift. The `hand - auto`
gap is **not** statistically resolved at this sample size: 95 % bootstrap CI
`[-1.3, +14.0]`, McNemar 13 vs 6, p = 0.167. Neither is `auto - baseline`
(`[-3.1, +18.9]`). Treat the point estimates as the result and the intervals
as the honest uncertainty.

Per layer, against the same baseline:

| layer | auto | hand | baseline | auto - baseline |
|---|---:|---:|---:|---:|
| C spatial | 67 % | 67 % | 42 % | **+25** |
| E bulk | 100 % | 100 % | 72 % | **+28** |
| L foundation-model | 50 % | 42 % | 33 % | **+17** |
| B workflow | 73 % | 87 % | 70 % | +3 |
| A preprocessing | 93 % | 100 % | 100 % | **-7** |
| G microbiome | 80 % | 100 % | 90 % | **-10** |

The shape matters more than the mean: **auto helps most where the baseline is
weakest, and hurts where the baseline is already strong.** On A and G the
synthesised registry misroutes a model that was doing fine unaided.

## Known defects, both diagnosed

1. **Alias collisions** — 46 of 1,162 alias keys are ambiguous
   (`principal component analysis` resolves to both `pca` and `scale`; last
   registration wins). Matches the failure counts: `wrong_tool_choice` 9 for
   auto vs 7 for hand. Fix is deduplication.
2. **Thin prerequisite coverage** — 11 confirmed chains, against
   `wrong_workflow_order` 8 for auto vs 4 for hand. Not a code defect: the
   probe fixture (a 500x2024 PBMC subsample) cannot supply the state most
   remaining functions need. Fix is a fixture ladder, not more oracle work.

## What auditing the hand registry found

The same probes were run against the 445 hand-written entries. Of the
contract claims they assert:

- `produces`: 58 confirmed / **43 refuted** / 31 inconclusive
- `requires`: 16 confirmed / **8 refuted** / 13 inconclusive
- 25.4 % of declared contract keys are prose placeholders, not keys
  (`"cell type labels"`, `"{cluster_col}"`)
- under-declaration: 1.33 observed keys per correctly declared one

So the two registries are not the same kind of object. Hand buys broader
coverage, a third of which is wrong; auto buys narrower coverage that
survived a falsification attempt. Comparing their AFS numbers directly
rewards the errors.
