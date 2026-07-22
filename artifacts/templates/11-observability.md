# Observability — <initiative name>

> Stage 11 · Owner: observability agent · Input: 10-production.md (SLOs), 08-evals.md (metrics)

## Golden signals
| Signal | Threshold | Owner |
|--------|-----------|-------|
| Latency p50/p95/p99 | <…> | <…> |
| Traffic / errors / saturation | <…> | <…> |
| Quality score | <…> | <…> |
| Groundedness / hallucination rate | <…> | <…> |
| Guardrail trips · HITL override rate | <…> | <…> |
| Token / cost per call | <…> | <…> |

## Online eval
- Cadence: <…>  ·  Method: ☐ scheduled eval-set ☐ live-shadow sample
- Regression loop back to eval's regression set: <how new prod failures are captured>

## Drift detection
- Input / output / embedding drift → trigger the retraining pipeline: <…>

## Dashboards
- **Exec view:** working? cost? saving vs business case?
- **Operator view:** health · queues · incidents.

## Alerts (each → a runbook step)
| Alert | Threshold | Severity | Owner | Runbook |
|-------|-----------|----------|-------|---------|
| <…> | <…> | <…> | <…> | <link> |

## CI/CD with eval gate
<deploy pipeline runs eval CI gate · blocks on regression · canary + rollback>

## Cost attribution (vs the business case)
| Unit (feature/team/tenant) | Cost | vs ROI promise |
|----------------------------|------|----------------|
| <…> | <…> | <…> |
