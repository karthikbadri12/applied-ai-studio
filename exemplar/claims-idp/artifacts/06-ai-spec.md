# AI Spec — FNOL Claims Intake IDP (claims-idp)

> Stage 6 · Owner: dev-spec agent · Input: 03-assessment.md, 05-architecture.md
> **This is the contract the dev pipeline builds against and the stage-8 evals measure.**
> Every field is testable. Approved 2026-07-22 (R. Vance, T. Okafor concur) · funded (stage 4).

## 1. Objective

Given a claim packet (mixed-media attachments) landing in GCS, produce within
p95 ≤60 s and ≤$0.09 a validated, confidence-gated `RoutingDecision` — auto-queued
when every gate is green (target ≥35% of packets), exception-queued otherwise —
with a complete `AuditRecord` for 100% of invocations and **zero** coverage-
consequential action taken by the system.

## 2. Capabilities & testable acceptance criteria

| # | Capability | Acceptance criterion (measured on stage-8 sets) | Metric bar |
|---|-----------|--------------------------------------------------|-----------|
| C1 | Document classification (claim_form / damage_photo / police_report / medical_bill / other) | Label match vs golden set | **accuracy ≥95%** |
| C2 | Field extraction (per doc-type field lists §4) with per-field confidence + source spans | Per-field F1 vs adjudicated golden truth; abstain (null + reason) counts correct when source lacks the field | **F1 ≥90%** |
| C3 | No fabricated fields | Field asserted with no supporting source span, golden + adversarial sets | **hallucinated-field rate <1% — pass/fail safety gate** |
| C4 | Policy validation (deterministic vs Snowflake) | Exact match of validation verdicts vs truth table | **exact-match ≥98%** |
| C5 | Confidence-gated routing | Share of golden-mix packets eligible for STP with all gates green AND zero critical errors inside the STP subset | **STP-eligible ≥35%** |
| C6 | Latency | End-to-end span per packet on full golden mix (incl. fallback share) | **p95 ≤60 s** |
| C7 | Unit cost | Metered OCR+token+infra-variable cost per packet on golden mix | **≤$0.09/packet** (expect $0.048 `[estimated]`) |
| C8 | Audit completeness | AuditRecords ÷ invocations on every eval run | **= 100%** (any miss fails the run) |
| C9 | Advisory-only guardrail | Adversarial prompts/documents attempting to trigger coverage language: output schema cannot express a coverage action; text fields screened | **0 coverage-consequential outputs — pass/fail** |

Bars C1–C9 are machine-readable in `evals/bars.yaml` — single source of truth;
this table and that file must never disagree (CI check).

## 3. Inputs

| Field | Shape | Source connector | Volume | Preprocessing |
|-------|-------|------------------|--------|---------------|
| Claim packet | `ClaimPacket` (§4) via GCS `packet.created` event | GCS bucket `claims-packets-prod` | 2,400/wk, 3.9× CAT surge `[stated]` | split, hash-dedup, DLP tag |
| Attachments | PDF/JPEG/TIFF, avg 6.2 docs · 10.4 pages `[estimated]` | same | ~1.3M pages/yr | Document AI OCR → text + layout + quality score |
| Policy record | 4 whitelisted columns | Snowflake `POLICY_DB` read-only SA | 1 lookup/packet, p95 340 ms `[measured]` | none — never sent to model |

## 4. I/O JSON Schemas (the contract; enforced by schema-constrained decoding + unit tests)

```json
{
  "ClaimPacket": {
    "packet_id": "string (uuid)",
    "received_at": "string (ISO-8601)",
    "channel": "mailbox | portal",
    "claimed_policy_number": "string | null",
    "line": "auto | property | unknown",
    "documents": ["Document"],
    "content_hash": "string (sha256)",
    "dlp_tags": ["PII", "PHI"]
  },
  "Document": {
    "doc_id": "string",
    "packet_id": "string",
    "mime_type": "application/pdf | image/jpeg | image/tiff",
    "page_count": "integer",
    "ocr_text": "string",
    "ocr_quality_score": "number 0..1",
    "doc_type": "claim_form | damage_photo | police_report | medical_bill | other",
    "doc_type_confidence": "number 0..1",
    "model_version": "string (e.g. gemini-2.5-flash@pinned)"
  },
  "ExtractedFields": {
    "packet_id": "string",
    "fields": [{
      "name": "string (from per-doc-type field list)",
      "value": "string | number | date | null",
      "confidence": "number 0..1",
      "source": {"doc_id": "string", "page": "integer", "span": "string | bbox"} ,
      "abstain_reason": "string | null  (required when value is null)"
    }],
    "extraction_path": "flash | flash+pro_fallback",
    "model_versions": ["string"]
  },
  "ValidationResult": {
    "packet_id": "string",
    "policy_found": "boolean",
    "checks": [{
      "check": "policy_active_on_loss_date | insured_name_match | coverage_line_match | vin_or_address_match",
      "verdict": "pass | fail | needs_human",
      "evidence": "string (deterministic rule id + values compared, PII-masked)"
    }],
    "overall": "clean | mismatch | needs_human"
  },
  "RoutingDecision": {
    "packet_id": "string",
    "decision": "stp_auto_queue | exception_review",
    "recommended_queue": "string (existing queue taxonomy id)",
    "reasons": ["string (gate id that passed/failed)"],
    "gates": {
      "classification_min_conf": "number (param, default 0.90 [assumption — confirm])",
      "required_field_min_conf": "number (param, default 0.85 [assumption — confirm])",
      "validation_overall": "clean required for STP",
      "ocr_quality_floor": "number (param, default 0.70 [assumption — confirm])"
    },
    "advisory_note": "string — NEVER contains coverage determination language (guardrail C9)"
  },
  "AuditRecord": {
    "audit_id": "string (uuid)",
    "packet_id": "string",
    "stage": "ingest | dlp | ocr | classify | extract | validate | gate | queue_write",
    "timestamp": "string (ISO-8601)",
    "model_version": "string | null",
    "prompt_hash": "string | null",
    "redacted_prompt": "string | null (PHI redacted, span offsets kept)",
    "redacted_output": "string | null",
    "outcome": "success | fallback_taken | exception | error",
    "latency_ms": "integer",
    "cost_usd": "number",
    "hitl_actor": "string | null (specialist/QA id when a human touched it)"
  }
}
```

Per-doc-type required field lists (extraction targets): claim_form: policy_no,
loss_date, loss_location, claimant_name, contact, description, claimed_amount;
police_report: report_no, agency, incident_date, parties, citations;
medical_bill: provider, service_date, billed_amount, treatment_codes;
damage_photo: damage_class, severity_hint (advisory).

## 5. Behavior & constraints

- **Cascade:** Flash on 100%; Pro re-extraction per-document when any required
  field confidence < `required_field_min_conf` OR `ocr_quality_score` < floor.
  Gate params live in config, not code (stage-5 handoff condition).
- **Abstain rule (from stage 3):** a null value with `abstain_reason` is correct
  behavior when the source lacks the field; evals score it as such.
- **Guardrails:** DLP screen pre-model; schema-constrained decoding (no free
  text except bounded `advisory_note`); C3 span-check post-extraction; C9
  coverage-language screen on `advisory_note`; Snowflake data never enters a prompt.
- **HITL (from process map, immutable):** exception packets require specialist
  confirmation; 10% STP daily QA sample; adjusters own all consequential
  decisions; **no autonomous coverage denial — advisory only** `[stated]`.
- **Failure posture:** audit write failure = packet failure (no silent loss);
  any unhandled error routes the packet to exception, never drops it.
- Latency budget p95 ≤60 s (segment budgets in 05 §latency); cost ≤$0.09/packet.

## 6. Prompt & tool inventory

| ID | Type | Purpose | Model | Constrained output | Side-effects | Auto/HITL |
|----|------|---------|-------|--------------------|--------------|-----------|
| P1 `classify_docs` | prompt (system + 6 few-shots) | DocType per document | Flash | enum + confidence JSON | none | Auto |
| P2 `extract_claim_form` | prompt (system + 4 few-shots) | Field list §4 | Flash → Pro | ExtractedFields JSON | none | Auto |
| P3 `extract_police_report` | prompt (system + 4 few-shots incl. handwriting) | Field list §4 | Flash → Pro | ExtractedFields JSON | none | Auto |
| P4 `extract_medical_bill` | prompt (system + 4 few-shots, PHI-aware) | Field list §4 | Flash → Pro | ExtractedFields JSON | none | Auto |
| P5 `assess_damage_photo` | prompt (system + 3 few-shots) | damage_class, severity_hint | Flash | JSON | none | Auto (advisory) |
| T1 `ocr_document` | tool (Document AI) | text+layout+quality | n/a | vendor JSON | none | Auto |
| T2 `lookup_policy` | tool (Snowflake, read-only, 4 columns) | ValidationResult inputs | n/a | typed row | none | Auto |
| T3 `write_audit` | tool (BigQuery append) | AuditRecord | n/a | insert ack | append-only write | Auto (mandatory) |
| T4 `assign_queue` | tool (claims platform API) | queue assignment | n/a | ack | **the only world-changing write** | Auto for STP routing only; HITL otherwise |

No agentic tool selection: the pipeline calls tools in fixed order (stage-3
verdict: agentic rejected). Actual prompt texts are stage-7 deliverables and
live in `src/claims_idp/prompts/` with pinned versions.

## 7. Acceptance / eval thresholds (hands to stage 8)

> Ship when, on the stage-8 golden set (500 packets) + adversarial set (120):
> C1 ≥95% ∧ C2 F1 ≥90% ∧ C4 ≥98% ∧ C5 ≥35% ∧ C6 p95 ≤60 s ∧ C7 ≤$0.09
> ∧ C3 <1% ∧ C8 =100% ∧ C9 =0 — where C3, C8, C9 are **pass/fail safety gates**:
> a single miss fails the release regardless of other scores.

## 8. CI eval gate

- Every PR: `make test` (offline unit tests) + `make eval` in `LLM_MODE=mock`
  against `evals/golden.jsonl` (≥25-row keyless seed) — **red = no merge**.
- Nightly + on any model/prompt version change: full eval vs live endpoints on
  the complete golden + adversarial sets; regression vs last green run blocks.
- `evals/run_evals.py` reads `evals/bars.yaml`, prints target-vs-measured per
  bar, exits nonzero on any miss; `.github/workflows/eval-gate.yml` wires both.
- Drift consistency check: §2 table ↔ `bars.yaml` parity test in CI.

## 9. Delivery mode

☑ **Workflow step** (Eventarc-triggered Cloud Run pipeline) + ☑ embedded
exception-review panel in the claims platform. ☐ API ☐ Batch ☐ Copilot ☐ MCP tool.

## 10. Build file-tree (per QUALITY_BAR build contract — the dev pipeline must produce exactly this)

```
claims-idp/
  src/claims_idp/
    __init__.py
    ingest.py            split, sha256 dedup, DLP tagging
    ocr.py               Document AI adapter (mocked in LLM_MODE=mock)
    classify.py          C1 — P1
    extract.py           C2/C3 — P2–P5, Flash→Pro cascade, span checks
    validate.py          C4 — deterministic checks vs T2
    gate.py              C5 — confidence gates + RoutingDecision
    audit.py             C8 — AuditRecord writer (BQ; jsonl sink in mock)
    schemas.py           §4 schemas as typed dataclasses + validators
    llm.py               provider-agnostic client — env-selected (Vertex/Bedrock/
                         Azure/Anthropic/OpenAI) + LLM_MODE=mock, fully keyless
    prompts/             P1–P5, versioned
  evals/
    golden.jsonl         ≥25 seed rows (stage-3 regression seed), keyless
    adversarial.jsonl    designed-to-break: wrong-policy, dup, near-miss names,
                         blank/rotated pages, coverage-bait (C9)
    run_evals.py         measures every bar; nonzero exit on miss
    bars.yaml            C1–C9 thresholds — single source of truth
  tests/                 unit tests per module, offline, no network
  .github/workflows/eval-gate.yml    tests + evals on every PR; red = no merge
  infra/                 Terraform, plan-safe: GCS+CMEK, Cloud Run, Eventarc,
                         BQ dataset (append-only), VPC-SC, DLP templates, IAM
  .env.example           GCP_PROJECT, VERTEX_LOCATION, SNOWFLAKE_*, LLM_MODE …
                         names only, never values
  Makefile               make test · make eval · make run
  README.md              quickstart ≤10 lines incl. mock mode
```

Constraints: package `claims_idp`; **stdlib-only Python** (no third-party deps —
cloud adapters isolated behind interfaces and inert in mock mode); everything
runs green keyless out of the box via `LLM_MODE=mock`.

## Metrics block (the contract rollup)

| Metric | Baseline | Target (bar) | Measured | Method | Owner |
|--------|----------|--------------|----------|--------|-------|
| C1 classification accuracy | n/a | ≥95% | — stage 8 | golden label match | Eval agent |
| C2 extraction F1 | n/a | ≥90% | — stage 8 | per-field F1, abstain-aware | Eval agent |
| C3 hallucinated fields | n/a | <1% pass/fail | — stage 8 | span-support check | Eval agent |
| C4 validation exact-match | n/a | ≥98% | — stage 8 | truth table | Eval agent |
| C5 STP-eligible | 0% `[stated]` | ≥35% | — stage 8 | gate sim on golden mix | Eval agent |
| C6 p95 latency | proto 41–60 s `[measured]` | ≤60 s | — stage 8 | trace spans | J. Iyer |
| C7 cost/packet | est. $0.048 | ≤$0.09 | — stage 8 | metered run | J. Iyer |
| C8 audit coverage | 0% | 100% | — stage 8 | records ÷ invocations | T. Okafor |
| C9 coverage-action outputs | n/a | 0 pass/fail | — stage 8 | adversarial screen | T. Okafor |

## Decision trail

| Decision | Chosen | Rejected | Why | Approved by |
|----------|--------|----------|-----|-------------|
| Schema enforcement | Constrained decoding + dataclass validators | Post-hoc regex repair | Repair hides model failure from evals; constrained decoding makes C3 measurable | Dev-spec agent, 2026-07-22 |
| Gate params | Config-driven with `[assumption — confirm]` defaults (0.90/0.85/0.70) | Hard-coded thresholds | Stage-7 tunes from eval curves; stage-5 handoff condition | Data-science agent concurred |
| C9 mechanism | Schema cannot express coverage actions + advisory_note screen | Prompt-only instruction "don't decide coverage" | Structural impossibility beats behavioral request; auditable | T. Okafor, 2026-07-22 |
| Mock strategy | Deterministic fixture responses keyed by doc hash | Recorded live responses | Fixtures are stable, PHI-free, and keyless in CI | Dev-spec agent |
| Eval seed size | 25-row keyless seed + full 500/120 live sets | Full sets in CI on every PR | PR loop stays <5 min and keyless; full rigor nightly | Eval agent concurred |

## Risk register

| # | Risk | Sev | Lik | S×L | Mitigation | Owner |
|---|------|-----|-----|-----|------------|-------|
| R1 | Default gate params (0.90/0.85/0.70) are guesses — mis-set gates sink C5 or poison STP | 4 | 4 | 16 | Stage-7 sweeps gates against golden curves before bars lock; params in config | Data-science agent |
| R2 | bars.yaml and this spec drift apart | 3 | 3 | 9 | CI parity check (§8) fails the build on mismatch | Delivery TL |
| R3 | Mock fixtures diverge from live model behavior → green CI, red reality | 4 | 3 | 12 | Nightly live eval is the arbiter; fixture refresh on every model pin bump | Eval agent |
| R4 | stdlib-only constraint makes cloud adapters awkward → temptation to add deps | 2 | 3 | 6 | Adapters use REST via urllib behind `llm.py` interface; code-reviewer enforces | Code-reviewer agent |
| R5 | Per-doc-type F1 masked by aggregate: police-report handwriting could sit at 80% inside a ≥90% average | 4 | 3 | 12 | Stage 8 must report per-doc-type F1; release notes flag any type <85% `[assumption — confirm]` for gate tightening | Eval agent |
| R6 | `assign_queue` (T4) is the one world-changing write — a bug auto-queues bad packets at scale | 5 | 2 | 10 | T4 dry-run mode in canary; rollback = flip STP gate to 0% (all packets → exception) in config, no deploy needed | J. Iyer |

## Assumptions & open questions

1. `[assumption — confirm]` Gate defaults 0.90 / 0.85 / 0.70 — stage 7 replaces with tuned values.
2. `[assumption — confirm]` Fallback rate ~18% (inherited); parameterized, not hard-coded.
3. `[assumption — confirm]` Per-doc-type F1 floor 85% as the sub-bar under the 90% aggregate.
4. **Open:** claims-platform queue API contract (wk-1 spike, stage-5 risk R4) — T4 adapter blocked until confirmed.
5. `[assumption — confirm]` 25-row keyless seed is representative enough for PR-loop smoke; nightly full run is the true gate.

## Handoff to stage 7 (data-science) and the dev pipeline

- **Target repo:** `claims-idp/` per §10 tree · **first build slice:** ingest →
  classify → mock eval loop green in `LLM_MODE=mock` (C1 path end-to-end).
- **Stage 7 consumes:** P1–P5 prompt slots (write the actual prompts + few-shots),
  gate-param sweep task (risk R1), fallback-rate measurement, ≥5-row experiment
  log per QUALITY_BAR.
- **Guardrails the code-reviewer enforces:** stdlib-only; schema-constrained
  outputs; audit write transactional; no secrets in code (`.env.example` names
  only); C3/C8/C9 wired as pass/fail in `run_evals.py`; T4 dry-run default off
  in non-prod.
- **Trigger:** this spec is approved **and** funded (stage 4 signed 2026-07-18) — build may start.
