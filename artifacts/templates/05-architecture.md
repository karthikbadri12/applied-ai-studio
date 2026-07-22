# Reference Architecture — <initiative name>

> Stage 5 · Owner: architecture agent · Input: 03-assessment.md, 04-business-case.md
> Consulted: cloud-gcp, cloud-aws, cloud-azure, cloud-onprem, model-selector, connector-advisor

## Diagram
```
<ASCII / mermaid reference architecture>
```

## Layer-by-layer choices
| Layer | Choice | Why |
|-------|--------|-----|
| Serving / compute | <…> | <…> |
| Model + routing | <primary → fallback cascade> | <…> |
| Retrieval (RAG) | <chunking / embed / store / rerank> | <…> |
| Data plane | <sources + connectors> | <…> |
| Orchestration | <pattern + runtime> | <…> |
| MLOps / LLMOps | <registry / eval gate / rollout> | <…> |

## Cloud comparison (same question, four answers)
| Layer | GCP | AWS | Azure | On-prem |
|-------|-----|-----|-------|---------|
| Model | <…> | <…> | <…> | <…> |
| Vector | <…> | <…> | <…> | <…> |
| Orchestration | <…> | <…> | <…> | <…> |

**Recommended path:** <cloud> — because <cost / residency / estate / skills / lock-in>.
Runners-up rejected because: <…>.

## Controls matrix (per regulated-data class)
| Data class | Masking | Encryption | Region | Retention | Access | Approved models |
|------------|---------|-----------|--------|-----------|--------|-----------------|
| <PHI> | <…> | <…> | <…> | <…> | <…> | <…> |

## Decision trail
- Chose <…>; rejected <…> because <…>.
