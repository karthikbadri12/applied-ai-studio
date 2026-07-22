# Data Science / Modeling — <initiative name>

> Stage 7 · Owner: data-science agent · Input: 06-ai-spec.md (target = the eval threshold)

## Approach (branch on solution type)
☐ GenAI / Agentic ☐ Classical ML

### GenAI path
- **System prompt (v_):** <…>
- **Few-shot / exemplars:** <…>
- **Output-schema enforcement:** <…>
- **Retrieval / context strategy:** <…>
- **Guardrail prompts:** <…>

### Classical ML path
- **Features:** <list + source + transform + leakage check>
- **Model & training:** <algorithm · split · HPO · imbalance handling>
- **Baseline vs candidate:** <…>

## Experiment log
| Run | What changed | Dev-set score | Cost / latency | Decision |
|-----|--------------|---------------|----------------|----------|
| 1 | <…> | <…> | <…> | keep / kill |

## Retraining / refresh pipeline
- Trigger: <drift / cadence / new labels>  ·  Re-eval before promote: <yes>
- Promotion approver (HITL if regulated): <…>
