# AI Spec — <initiative name>

> Stage 6 · Owner: dev-spec agent · Input: 03-assessment.md, 05-architecture.md
> **This is the contract the dev pipeline builds against.** Every field must be testable.

## 1. Objective
<One testable sentence: what the system does.>

## 2. Inputs
| Field | Shape | Source connector | Volume | Preprocessing |
|-------|-------|------------------|--------|---------------|
| <…> | <…> | <…> | <…> | <…> |

## 3. Outputs
- **Schema:** <exact shape>
- **Definition of a correct output:** <…>

## 4. Behavior & constraints
- Tone / refusals: <…>  ·  Latency budget: <p95 …>  ·  Cost ceiling: <$/call>
- Guardrails: <…>  ·  HITL points (from process-map): <…>

## 5. Acceptance / eval threshold (hands to stage 8)
> Ship when <metric ≥ X on the golden set> AND <p95 < Ys> AND <safety = pass>.

---

## RAG blueprint (if applicable)
Corpus · chunking · embedding model · store · retrieval k · rerank · grounding/citation rules · refresh cadence.

## Agent toolchain (if applicable)
| Tool | Purpose | Inputs | Side-effects | Auto / HITL | 
|------|---------|--------|--------------|-------------|
| <…> | <…> | <…> | <…> | <…> |
- Stop conditions · max steps: <…>

## CI eval gate
<how the eval set runs in CI; what score blocks a merge>

## Delivery mode
☐ API ☐ Batch ☐ Embedded copilot ☐ Workflow step ☐ MCP tool

## Handoff to dev pipeline
- Target repo: <…>  ·  First build slice: <…>  ·  Guardrails code-reviewer enforces: <…>
- Trigger: spec approved **and** funded.
