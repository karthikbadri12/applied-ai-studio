# Evaluation Harness — <initiative name>

> Stage 8 · Owner: eval agent · Input: 06-ai-spec.md (threshold), 07-data-science.md
> No eval, no ship.

## Golden set
- Size: <N>  ·  Sourced from: <…>  ·  Labelled by: <…>
- Correctness judged by: ☐ exact match ☐ rubric ☐ LLM-as-judge ☐ human

## Adversarial set
- Edge cases: <…>  ·  Ambiguous: <…>  ·  Injection/jailbreak: <…>  ·  OOD: <…>
- Exceptions from process-map: <…>

## Regression set
- Cases that must never break again (grows with each bug): <…>

## Metrics & bars (the ship gate)
| Metric | Bar | Type |
|--------|-----|------|
| Quality (<accuracy/F1/faithfulness>) | ≥ <X> | gate |
| Safety (harmful-output rate) | = 0 | pass/fail |
| Latency p95 | < <Y>s | gate |
| Cost / call | ≤ <$Z> | gate |

## CI gate
<how it runs in CI · score that blocks merge · human override + sign-off>

## Judge design (if LLM-as-judge)
- Rubric: <…>  ·  Judge model: <…>  ·  Validated against human labels: <agreement %>
