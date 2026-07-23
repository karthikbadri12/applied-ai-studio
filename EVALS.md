# EVALS.md: the evaluation framework

*"Does it work?"* is only answerable if you decided what "work" means before you
measured. This is the doctrine the `eval` agent follows, the `poc-gate` agent cites,
and the `code-reviewer` enforces at merge. Reference implementation:
`exemplar/claims-idp/build/evals/`.

**The one rule everything else serves:** the bar comes from the business need, set
*before* measurement. A bar chosen after seeing the score doesn't measure anything. It just
rationalises whatever you got.

---

## 1. The three-set doctrine

| Set | Answers | Built from | Sizing |
|---|---|---|---|
| **Golden** | "Does it work on the real distribution?" | Stratified sample of actual production cases, labelled by humans | Enough per stratum to make the metric stable — report per-stratum, not just the aggregate |
| **Adversarial** | "How does it break?" | Deliberately hostile cases, designed to fail | Small but vicious. **An adversarial set that finds nothing is too weak**: say so and strengthen it |
| **Regression** | "Did we break it again?" | Every past incident, bug, and human correction | Grows forever. Never shrinks |

**Golden-set sampling** must be stratified and the strata declared, by case type,
difficulty, channel, or segment (the exemplar uses 60% clean / 25% messy / 15%
edge). An unstratified random sample flatters the model on the easy majority and
hides the tail where the business actually loses money.

**Adversarial taxonomy**: cover every row that applies:

| Attack class | Examples |
|---|---|
| Prompt injection | Instructions embedded in retrieved documents, user content, tool output, filenames |
| Edge cases | Missing/contradictory fields, extreme values, empty and oversized inputs, wrong language |
| Quality degradation | Poor scans, handwriting, transcription noise, truncation |
| Distribution shift | Cases from a segment or period the golden set under-represents |
| Jailbreak / scope escape | Attempts to make the agent act outside its charter or skip a guardrail |
| Ambiguity traps | Cases where the correct answer is "escalate to a human", not an answer |

That last row matters most: **a system that never abstains is not safe.** Escalation
must be a scored, expected outcome, not a failure.

## 2. Metric taxonomy

Four families. They are not interchangeable, and they are never averaged together.

| Family | Examples | Gate behaviour |
|---|---|---|
| **Quality** | Accuracy, F1 (precision/recall reported separately), exact match, groundedness | Threshold: must meet the bar |
| **Safety** | Hallucination rate, harmful output, PII leakage, injection-execution rate | **Pass/fail. Never averaged, never traded off against quality.** One breach fails the gate |
| **Operational** | p95/p99 latency, cost per unit, throughput, error rate | Threshold: bars from the SLA in `01-prd.md` |
| **Business** | The PRD success metric (STP rate, handle time, misroute rate) | The one the sponsor cares about; `09-poc-gate.md` cites it directly |

**Precision and recall are reported separately, always.** A single F1 hides which
side the system fails on; and in most enterprise workflows a false accept costs
far more than a false reject (or the reverse). The business decides which; the
metric must expose it.

## 3. Setting bars

1. Derive from the business need in `01-prd.md` and the economics in
   `04-business-case.md`, *"at 90% extraction accuracy the review cost eats the
   savings, so 90% is the floor."*
2. Write them to `evals/bars.yaml`, machine-readable, one source of truth, read by
   both the harness and CI. The AI Spec (`06-ai-spec.md`) and `bars.yaml` must
   agree; a parity check is part of the eval gate.
3. Bars change only by explicit, audited human decision, never silently to make a
   run pass. A bar change is a `gate_decision` audit event.

## 4. LLM-as-judge

Useful where exact match is impossible (summaries, reasoning, tone). Dangerous
when unvalidated.

- **Rubric**: concrete and criterion-referenced. "Rate 1–5 for quality" is
  unusable; "does the output cite a source that actually contains the claim
  (yes/no)" is scoreable.
- **Judge validation is mandatory.** Score a human-labelled sample (~100 cases) with
  the judge and report agreement and Cohen's κ. The exemplar reports 94% agreement,
  κ 0.87. **An unvalidated judge is not evidence.**
- **Independence**: never let a model judge its own output with the same prompt
  and context. Different model or different framing, at minimum.
- **Where judges are not acceptable:** safety gates. Hallucination, PII leakage and
  harmful output are verified deterministically or by human review; a probabilistic
  judge cannot be the last line of defence on a pass/fail safety control.

## 5. CI integration: the eval gate

The gate is what makes evals real rather than decorative:

- `evals/run_evals.py` runs all three sets, computes every metric in `bars.yaml`,
  prints a bar-vs-measured table with PASS/FAIL per row, writes `results.json`,
  and **exits nonzero if any bar misses**.
- `.github/workflows/eval-gate.yml` runs tests + evals on every PR. **Red means no
  merge**, `code-reviewer` will not issue MERGE on a red gate, and `production`
  treats it as a launch blocker.
- Everything must run **keyless in mock mode**. An eval suite that needs credentials
  before it can prove anything can't run in CI, won't run on a laptop, and won't be
  run at all.

## 6. Online evaluation

Offline evals prove it worked on yesterday's data. Production is where it stops.

- **Shadow sampling**: score a percentage of live traffic (exemplar: 5%) against
  the same rubric; alert when the online score diverges from the offline score.
  Divergence means the golden set no longer represents reality.
- **HITL override rate** as a first-class quality signal. When humans start
  overturning the system more often, quality has moved before any metric does.
- **Drift triggers**: input distribution shift, confidence-score drift, upstream
  model version change, seasonal shift. Each trigger fires a re-evaluation, not a
  quiet continuation.
- **The feedback loop**: every human correction becomes a labelled case. Corrections
  enter the golden set; incidents enter the regression set (see
  `DISASTER_COMMAND.md`). The sets are living assets, and their growth is a health
  metric in `11-observability.md`.

## 7. Anti-patterns

| Anti-pattern | Why it fails | The fix |
|---|---|---|
| Demo as evidence | Cherry-picked, unrepeatable, N≈5 | Only eval sets count at the POC gate |
| Bar set after measuring | Guarantees a pass, proves nothing | Bars in `bars.yaml` before the run |
| Averaged safety metrics | "99.2% safe" means 8 breaches per 1,000 | Safety is pass/fail, never a mean |
| Static golden set | Rots as the business shifts; scores stay green while quality falls | Refresh cadence + drift triggers + corrections feed back |
| Judge judging itself | Same blind spots on both sides | Different model/framing; validate against humans |
| Leaderboard chasing | Optimises a benchmark, not the business metric | Optimise the AI Spec threshold; cost and latency are first-class |
| Aggregate-only reporting | Hides the failing stratum | Report per-stratum + a failure taxonomy with counts |
| No abstention cases | System confidently answers when it should escalate | Score "escalate" as a correct outcome |

---

**See also:** `QUALITY_BAR.md` (what `08-evals.md` must contain) · `HARNESS.md`
(guardrail severities, `eval_result` audit events) · `GOVERNANCE.md` (evals as the
NIST **MEASURE** function and MRM outcome analysis) · `exemplar/claims-idp/build/evals/`
(a working harness: 48 cases, 7 bars, green in mock mode).
