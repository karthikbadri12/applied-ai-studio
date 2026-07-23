# QUALITY_BAR.md: the artifact quality floor

An artifact that merely fills the template's headings is **incomplete**. The bar is:
*a Google Cloud delivery lead could walk into a C-suite review with this file alone
and survive hostile questions.* Every agent is bound to this bar by Constitution
Art. 6.4. The reference implementation is `exemplar/claims-idp/`, when in doubt,
match its depth.

## Universal requirements (every artifact, every stage)

1. **Quantify everything.** Every claim carries a number, and every number carries a
   label (`[stated]` / `[estimated]` / `[measured]` / `[assumption, confirm]`) and
   its arithmetic. "High labor cost" is banned; "$1.9M/yr = 2,400 packets/wk × 27min
   avg × $34/hr loaded [estimated]" is the floor.
2. **Metrics block.** Baseline → target → measured (when available), with the
   measurement method and owner. Same table schema across all 12 artifacts so
   metrics are traceable stage-to-stage.
3. **A diagram when there is topology.** Process flows, architectures, data flows,
   rollout plans: mermaid, not paragraphs.
4. **Decision trail.** Chosen / rejected / why / approved-by. A recommendation with
   no named rejected alternative is not a decision, it's a guess.
5. **Risk register.** ≥ 5 risks scored severity × likelihood, each with a named
   mitigation and owner. Generic risks ("model may hallucinate") only count when
   tied to this use case's failure mode and cost.
6. **Eval linkage.** Which eval set + metric bar proves this artifact's claims.
   From stage 8 onward: actual results tables, not promises.
7. **Assumptions & open questions** as a numbered list. An empty list is a claim —
   and almost always a false one.
8. **Handoff contract.** The final section addresses stage N+1 by name: here is
   what you consume, here is what is still open.

## Stage-specific floors (beyond the template)

| Artifact | Not done until it has |
|---|---|
| 01 PRD | Stakeholder map (RACI), volumetrics table, current-cost model with arithmetic, SLA/latency envelope, explicit out-of-scope list, sign-off block |
| 02 Process map | As-is AND to-be mermaid flows; per-step table: actor, system, duration, error rate, Human/Machine tag, automation rationale |
| 03 Assessment | Verdict matrix (ML/GenAI/Hybrid/Agentic scored against ≥5 criteria), model shortlist with context/cost/latency columns, data-readiness scorecard, ground-truth inventory |
| 04 Business case | 3-scenario model (conservative/expected/optimistic), payback month, 3-yr NPV, sensitivity: the 2 assumptions that swing the case, cost of doing nothing |
| 05 Architecture | Component diagram + sequence diagram, 4-cloud comparison table with a winner and named losers, PII/PHI controls matrix (data class × control × verified-by), FinOps unit-cost estimate, **dependency & readiness matrix** (component × version × READY/NEEDS-SETUP/BLOCKED/MISSING × owner × exact setup steps — reuse `00-stack-review.md`'s matrix where it exists, extend it with the new components this architecture adds) |
| 06 AI Spec | Testable acceptance criteria per capability, full I/O JSON schemas, prompt/tool inventory, CI eval-gate thresholds, delivery mode, **the build file-tree the dev pipeline must produce**, **build-dependency checklist** (every install/provision/credential step the build needs, in order, each marked ready/pending, synced to `aidlc.config.json`) |
| 07 Data science | Actual prompts (system + few-shot), experiment log table (≥5 rows: change, metric, cost, keep/kill), retraining/refresh triggers |
| 08 Evals | Golden/adversarial/regression set sizes + sampling method, results table per metric bar (target vs measured), failure taxonomy with counts, judge rubric + judge-validation numbers |
| 09 POC gate | Verdict + evidence table citing stage-8 results row-by-row against the PRD metric, conditions with owners and dates if CONDITIONAL |
| 10 Production | Launch-blocker checklist with owner + status per item, incident severity matrix + escalation path, rollback trigger + tested-rollback note, responsible-AI checklist mapped to the domain's regulations |
| 11 Observability | Dashboard spec (per panel: metric, source, threshold), alert → runbook table, online-eval sampling plan, cost-attribution model per call |
| 12 Brief | One-page executive summary (readable standalone), full metrics rollup from metrics.json, complete decision log, dev-pipeline handoff packet |

## The build contract (what "pipeline ready" means)

When `/appliedai` runs in build mode, "done" is a **working repository**, not a plan:

```
<project>/
  src/<pkg>/            the pipeline stages as code (typed, docstringed)
  src/<pkg>/llm.py      provider-agnostic client, env-selected (Vertex/Bedrock/Azure/
                        Anthropic/OpenAI) + LLM_MODE=mock so everything runs keyless
  evals/golden.jsonl    real cases, ≥25 rows to start
  evals/adversarial.jsonl  designed-to-break cases
  evals/run_evals.py    measures every metric bar from the AI Spec; nonzero exit on miss
  evals/bars.yaml       the thresholds, machine-readable; single source of truth
  tests/                unit tests, runnable offline
  .github/workflows/eval-gate.yml   CI: tests + evals on every PR; red = no merge
  infra/                IaC skeleton for the chosen cloud (Terraform), plan-safe
  .env.example          every credential as an env-var name; never a value
  Makefile              make test · make eval · make run
  README.md             quickstart in ≤ 10 lines, incl. mock mode
```

The eval harness MUST run green in mock mode out of the box, a demo that needs
credentials before it proves anything has proved nothing. The code-reviewer verdict
gates completion, per the dev pipeline.
