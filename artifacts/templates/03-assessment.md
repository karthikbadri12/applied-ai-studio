# Technical Assessment — <initiative name>

> Stage 3 · Owner: assess agent · Input: 02-process-map.md · Consulted: model-selector, domain-advisor, cloud-*

## Verdict: should this be AI?
<Yes/No + one line. If "no — use rules/integration/process change," say why and stop.>

## Solution type
- **Primary:** ☐ Classical ML ☐ GenAI ☐ Hybrid ☐ Agentic
- **Why this, not simpler:** <the reason the cheaper options were rejected>

## Model shortlist (from model-selector)
| Tier | Managed candidate | Open candidate | Note |
|------|-------------------|----------------|------|
| <mid> | <…> | <…> | <…> |

## Data & ground truth
| Candidate step | Source system (connector) | Labelled? | How "correct" is measured |
|----------------|---------------------------|-----------|----------------------------|
| <…> | <Snowflake / …> | <y/n> | <…> |

## Regulated-data flags (from domain-advisor) — carried downstream
- ☐ PII ☐ PHI ☐ PCI ☐ MNPI ☐ other: <…>

## Cloud realizability (quick check; full comparison in stage 5)
- Realizable on GCP / AWS / Azure / on-prem? <y/y/y/y + caveats>

## Top risks
1. <…>
