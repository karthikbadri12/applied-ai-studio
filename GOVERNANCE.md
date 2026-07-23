# GOVERNANCE.md: the AI governance framework

`CONSTITUTION.md` states the rules. `HARNESS.md` enforces them at runtime.
**This document maps both onto the external frameworks your risk, compliance, and
audit functions already use**, so an AIDLC initiative arrives at a governance
review with the evidence already assembled, not scrambling to reconstruct it.

Nothing here is new process. It is a crosswalk: every control below is already
produced by a stage, an artifact, or a gate.

---

## 1. Risk tiering (EU AI Act-aligned)

The `domain-advisor` and `assess` stages jointly assign a tier at stage 3. The tier
determines which controls become **mandatory** downstream.

| Tier | Meaning | AIDLC consequence |
|---|---|---|
| **Prohibited** | Social scoring, manipulative systems, most biometric categorisation | `assess` returns a NO-GO verdict and the initiative stops. Not a design problem — a legality problem. |
| **High-risk** | Credit, insurance underwriting, employment, essential services, medical, critical infrastructure | All five HITL gates mandatory and non-waivable · human oversight documented per decision point · bias/fairness testing required in `08-evals.md` · full technical documentation via the 12 artifacts · post-market monitoring in `11-observability.md` |
| **Limited** | Chatbots, content generation with human review | Disclosure requirement (users told they're interacting with AI) recorded in `10-production.md` · standard gates apply |
| **Minimal** | Internal productivity, spam filtering, no consequential decisions | Standard AIDLC discipline; gates may be waived only by explicit, audited human waiver (Art. 5 soft-guardrail protocol) |

**Rule:** the tier is recorded in `03-assessment.md`, carried in every downstream
artifact, and re-checked at `10-production.md`. Tier changes are audit events.

## 2. NIST AI RMF crosswalk

| RMF function | What it asks | Where AIDLC answers it |
|---|---|---|
| **GOVERN** | Are policies, roles, and accountability defined? | `CONSTITUTION.md` (the policy) · `HARNESS.md` (enforcement) · this file (risk tiering + RACI §5) · `audit.jsonl` (accountability record) |
| **MAP** | Is the context, purpose, and risk understood? | P1: `01-prd.md` (problem, metric, scope), `02-process-map.md` (where humans vs machines act) · P2: `03-assessment.md` (solution verdict, data classes, regulated flags), `05-architecture.md` (controls matrix) |
| **MEASURE** | Is performance and trustworthiness quantified? | P3: `08-evals.md` (golden/adversarial/regression, metric bars, failure taxonomy), `09-poc-gate.md` (evidence table vs the PRD metric) — see `EVALS.md` |
| **MANAGE** | Are risks prioritised, monitored, and responded to? | P4: `10-production.md` (launch blockers, responsible-AI checklist), `11-observability.md` (golden signals, drift triggers, cost) · `DISASTER_COMMAND.md` (incident response) |

Every artifact's risk register (a `QUALITY_BAR.md` requirement: ≥5 risks, scored
severity × likelihood, named mitigation and owner) is the MANAGE evidence.

## 3. Model risk management (SR 11-7-style)

For banking, insurance, and other regulated estates where models require formal
validation:

| MRM element | AIDLC evidence |
|---|---|
| **Model inventory** | `12-delivery-brief.md` + `metrics.json` — purpose, owner, tier, data classes, models used incl. versions and fallback cascade |
| **Conceptual soundness** | `03-assessment.md` — the scored verdict matrix showing why this approach, and which simpler approaches were rejected and why |
| **Data quality & lineage** | `00-stack-review.md` (readiness matrix) + `03-assessment.md` (data-readiness scorecard, ground-truth inventory) |
| **Outcome analysis / back-testing** | `08-evals.md` — measured results per metric bar with sampling method, plus `11-observability.md` online eval |
| **Independent validation** | The `code-reviewer` and `poc-gate` agents are structurally independent of `coder` and `data-science` — they cannot approve their own work (Constitution Art. 1, 6) |
| **Ongoing monitoring** | `11-observability.md` — drift triggers, HITL-override rate, quality signals, and the ROI promise monitored against the `04-business-case.md` baseline |
| **Periodic review** | `10-production.md` sets the review cadence; drift triggers force an off-cycle review |
| **Change management** | The CI eval gate: no change merges on a red bar; every change re-measured against the same sets |

## 4. Data governance

**Data-class taxonomy.** Assigned at `03-assessment.md`, controlled at
`05-architecture.md`, verified at `10-production.md`:

`PUBLIC` · `INTERNAL` · `CONFIDENTIAL` · `PII` · `PHI` · `PCI` · `CPNI` · `REGULATED-OTHER`

**Approval matrix.** The `05-architecture.md` controls matrix must state, for every
data class the solution touches: which model/service may process it, under which
control (masking, tokenisation, redaction-at-source, CMEK, VPC boundary), in which
region, retained how long, and **verified by whom**. Constitution Art. 4 makes an
uncontrolled regulated-data path an automatic launch blocker, the harness treats
an unapproved data-class → model pairing as a *hard* guardrail violation and blocks.

**Residency & retention.** Named per class in the controls matrix. Cross-border
transfer requires an explicit entry, not silence.

**Data-subject rights.** Where GDPR/CCPA apply, `10-production.md` must record how
access, deletion, and objection requests are honoured, including in vector stores
and cached model outputs, the two places teams routinely forget.

## 5. Roles and the gate RACI

| Gate | Sponsor | Finance | Security/Compliance | Delivery owner | Administrator |
|---|---|---|---|---|---|
| PRD sign-off | **A** | C | I | R | R |
| Business case | C | **A** | I | R | R |
| POC GO/NO-GO | **A** | C | C | R | R |
| Production launch | C | I | **A** | R | R |
| Delivery brief | C | I | C | **A** | R |

*A = accountable (owns the decision) · R = responsible (does the work) · C = consulted · I = informed.*
The **administrator** is the orchestrator plus the human owner; advisors are
consulted throughout and are accountable for nothing; they recommend only
(Constitution Art. 1.2).

## 6. The evidence pack

When an auditor, regulator, or model-risk committee asks *"show me"*, the answer is
a directory, not a slide deck:

```
artifacts/
  00–12 *.md        the decision trail, each with metrics, risks, rejected
                    alternatives, assumptions, and the approver of record
  metrics.json      machine-readable rollup: stage timings, gate outcomes +
                    approvers, eval scores, model/cloud decisions
  audit.jsonl       append-only ledger: every stage, consult, guardrail trip,
                    waiver, and gate decision, timestamped and phase-tagged
  incidents/        post-incident reviews (see DISASTER_COMMAND.md)
build/evals/        the sets, the bars, the measured results, the CI gate
```

Three properties make this defensible: it is **contemporaneous** (written as the
work happened, not reconstructed), **append-only** (Art. 7, a BLOCKED event may
never be omitted; omission is itself a violation), and **reconciled** (the `brief`
agent cross-checks `audit.jsonl` against `metrics.json` and reports mismatches as
findings).

## 7. Responsible-AI control checklist

Verified at `10-production.md`; scope varies by tier (§1) and domain (`domains/`).

- **Fairness**: for high-risk tiers, disaggregated eval performance across the
  protected groups the domain defines; a single aggregate score is insufficient.
- **Explainability**: proportional to tier: high-risk decisions need a
  human-readable reason, source citations for retrieval, and confidence surfaced
  to the reviewer.
- **Human oversight**: every consequential decision routes to a named human role;
  the reviewer must have the information and authority to actually overturn it
  (oversight that can't say no isn't oversight).
- **Robustness**: adversarial eval set, prompt-injection quarantine (a universal
  hard guardrail), graceful degradation and fallback paths.
- **Transparency**: AI disclosure where required; model, version, and prompt
  version recorded per decision in the audit trail.
- **Accountability**: a named owner per launch blocker and per open risk.

---

**See also:** `CONSTITUTION.md` (the articles) · `HARNESS.md` (runtime enforcement,
guardrail severities, the gate protocol) · `QUALITY_BAR.md` (per-artifact floors) ·
`EVALS.md` (how MEASURE is actually done) · `DISASTER_COMMAND.md` (when it goes
wrong in production).
