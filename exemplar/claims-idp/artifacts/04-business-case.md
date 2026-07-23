# Business Case — FNOL Claims Intake IDP (claims-idp)

> Stage 4 · Owner: value-prop agent · Input: 03-assessment.md, 01-prd.md
> Every figure labelled `[stated]` / `[estimated]` / `[assumption — confirm]`. All arithmetic shown.

## Baseline cost of the status quo (from PRD, restated)

| Driver | Math | Annual cost | Label |
|--------|------|-------------|-------|
| Intake labor | 124,800 packets × 0.45 hr × $34/hr | $1,909,440 | time/volume `[stated]`, rate `[estimated]` |
| Misroute rework | 124,800 × 9% = 11,232 × 0.583 hr × $34 | $222,768 | `[estimated]` |
| CAT-season overtime | ~2,100 OT hr × $51/hr | $107,100 | `[estimated]` |
| **Status quo total** | — | **$2,239,308/yr** | — |

## Impact model (tied to the PRD metrics)

Savings decompose into three levers, each traceable to a PRD bar:

1. **STP lever** — every straight-through packet saves the full 27 min:
   `STP packets × 0.45 hr × $34 = STP packets × $15.30`.
2. **Assist lever** — every exception packet drops from 27 min to the assisted
   handle time: `(1−STP) × 124,800 × (27 − assisted min)/60 × $34`.
3. **Rework lever** — misroute 9% → target: `Δpts × 124,800 × 0.583 hr × $34`.

HITL QA-sample labor is charged in **run cost** (not netted from savings) to
avoid double counting.

## Three scenarios

| Scenario | STP | Assisted time | Misroute | Lever math | Gross savings/yr |
|----------|-----|---------------|----------|-----------|------------------|
| Conservative | 20% | 18 min | 9%→6% | STP: 24,960 × $15.30 = $381,888 · Assist: 99,840 × 0.15 hr × $34 = $509,184 · Rework: 3,744 × $19.83 = $74,256 | **$965,328** `[estimated]` |
| Expected | 35% `[PRD target]` | 12 min `[PRD target]` | 9%→4% `[PRD target]` | STP: 43,680 × $15.30 = $668,304 · Assist: 81,120 × 0.25 hr × $34 = $689,520 · Rework: 6,240 × $19.83 = $123,760 | **$1,481,584** `[estimated]` |
| Optimistic | 45% | 10 min | 9%→3% | STP: 56,160 × $15.30 = $859,248 · Assist: 68,640 × 0.283 hr × $34 = $661,232 · Rework: 7,488 × $19.83 = $148,512 | **$1,668,992** `[estimated]` |

Note: savings are capacity released, realized as CAT-surge absorption without
overtime, backlog elimination, and staged redeployment — not day-one layoffs
(risk R4 in the PRD; workforce plan owned by R. Vance).

## Cost to build (one-time)

| Item | Math | Cost | Label |
|------|------|------|-------|
| Delivery squad | 5 people (TL, 2 eng, 1 ML/prompt, 1 BA/QA) × 14 wk × 40 hr × $92/hr blended loaded | $257,600 | `[estimated]` |
| Integrations (claims platform API, Snowflake connector, GCS eventing) | fixed-scope estimate | $32,000 | `[estimated]` |
| Ground-truth build (from 03-assessment §inventory) | $11.2K golden + $2.7K adversarial + $1.5K routing truth | $15,400 | `[estimated]` |
| Security review + pen test (PII/PHI scope) | vendor quote range midpoint | $18,000 | `[estimated]` |
| Contingency | 15% × above ≈ | $48,000 | `[estimated]` |
| **Total build** | — | **$371,000** | `[estimated]` |

## Cost to run (annual, expected scenario)

| Item | Math | Annual | Label |
|------|------|--------|-------|
| Inference + OCR | 124,800 × $0.048/packet (cost bar $0.09 ⇒ ceiling $11,232) | $5,990 | `[estimated]`; unit build-up in 05-architecture §FinOps |
| GCP infra (Cloud Run, GCS, BigQuery, VPC-SC, logging) | ~$2,400/mo × 12 | $28,800 | `[estimated]` |
| HITL QA-sample labor | 43,680 STP × 10% = 4,368 packets × 5 min × $34 | $12,376 | `[estimated]` |
| Eval maintenance & golden-set refresh | 0.25 FTE ML eng ($48K) + annotation refresh ($6K) | $54,000 | `[estimated]` |
| Platform ops / on-call | 0.4 FTE SRE | $64,000 | `[estimated]` |
| **Total run** | — | **$165,166/yr** | `[estimated]` |

(Conservative run: $159,862 — QA line falls to $7,072. Optimistic: $168,702 — QA rises to $15,912.)

## The case

| Scenario | Gross savings | Run cost | **Net/yr** | Payback (build ÷ net/12) | 3-yr NPV @10% |
|----------|--------------|----------|-----------|--------------------------|----------------|
| Conservative | $965,328 | $159,862 | $805,466 | $371,000 ÷ $67,122 = **5.5 mo** | −371K + 805.5K × 2.4869 = **$1.63M** |
| Expected | $1,481,584 | $165,166 | $1,316,418 | $371,000 ÷ $109,701 = **3.4 mo** | −371K + 1,316.4K × 2.4869 = **$2.90M** |
| Optimistic | $1,668,992 | $168,702 | $1,500,290 | $371,000 ÷ $125,024 = **3.0 mo** | −371K + 1,500.3K × 2.4869 = **$3.36M** |

(2.4869 = 3-yr annuity factor at 10%: 0.9091 + 0.8264 + 0.7513. Flat savings
assumed across yrs 1–3 `[assumption — confirm]` — conservative, since volume grows.)

- **Verdict: ☑ Fund.** Even the conservative case pays back in under 6 months
  and clears $1.6M 3-yr NPV against a $371K build.

## Cost of doing nothing

Status quo runs $2,239,308/yr and claims volume is growing ~6%/yr
`[assumption — confirm]` (ops trend 2023–25). 3-yr do-nothing cost:
$2.24M × (1 + 1.06 + 1.1236) = **$7.13M**, plus unquantified cycle-time damage
to retention during CAT events — the 2025 hail-season backlog peaked at 11 days
`[stated]`, and every one of those days is a policyholder deciding whether to
renew. Hiring to the peak instead (≈ +9 FTEs `[estimated]`) adds ~$640K/yr and
still doesn't fix misroutes.

## Sensitivity — the two assumptions that swing the case

| Swing variable | Expected value | Break-even point | Case impact |
|----------------|----------------|------------------|-------------|
| **STP rate** | 35% | ~15%: annual cost to cover = run $165K + build/3 $124K = $289K ⇒ $289K ÷ $15.30/packet ≈ 18,900 packets ≈ 15% of volume — with zero assist-lever credit | Every −5 pts of STP ≈ −$95.5K net/yr (6,240 × $15.30); case survives to 15% STP even if assist lever fails entirely |
| **Assisted handle time** | 12 min | 22.9 min: assist lever alone breaks even at $289K ÷ 124,800 = $2.32/packet = 4.1 min saved (27 → 22.9), with zero STP credit | Every +1 min on assisted time ≈ −$46K net/yr at 35% STP (81,120 × 1/60 × $34) |

Secondary sensitivities: Pro-fallback rate 18% → 30% moves inference from
$5,990 to ~$8,400/yr `[estimated]` — immaterial (<0.2% of net). The case lives
and dies on the two operational levers, not on token prices.

## Metrics block (finance-facing; measured post-launch)

| Metric | Baseline | Target | Measured | Method | Owner |
|--------|----------|--------|----------|--------|-------|
| Net annual benefit | $0 | ≥$1.32M (expected) | — (Q1 2027 review) | Realized-savings model: actual STP/handle-time/misroute × lever math above | Finance BP (K. Doyle) |
| Cost per packet (all-in run ÷ volume) | n/a | ≤$1.32 ($165,166 ÷ 124,800) | — | Monthly billing + labor roll-up | K. Doyle |
| Payback | n/a | ≤6 mo conservative | — | Cumulative net vs $371K | K. Doyle |

## Decision trail

| Decision | Chosen | Rejected | Why | Approved by |
|----------|--------|----------|-----|-------------|
| Savings accounting | Capacity-released model, QA labor in run cost | Netting QA from gross savings | Avoids double counting; makes HITL labor visible per QUALITY_BAR | Value-prop agent; K. Doyle concurred |
| Benefit horizon | 3-yr NPV, flat savings | 5-yr with growth credit | Conservatism: shorter horizon + no growth credit; case still clears | K. Doyle, 2026-07-18 |
| Alternative considered | Fund claims-idp | Hire +9 FTEs to peak | $640K/yr recurring vs $371K one-time + $165K run; hiring fixes neither misroutes nor audit coverage | R. Vance, 2026-07-18 |
| Alternative considered | Build on HYBRID verdict | Buy vertical IDP SaaS | Vendor quotes $0.35–0.60/packet `[estimated]` = $44–75K/yr + per-seat fees, weak Snowflake validation story, audit exhaust not ours; revisit if build slips >8 wks | R. Vance, 2026-07-18 |

## Risk register (financial)

| # | Risk | Sev | Lik | S×L | Mitigation | Owner |
|---|------|-----|-----|-----|------------|-------|
| R1 | STP lands <15% break-even floor | 4 | 2 | 8 | Stage-9 POC gate blocks scale spend until measured STP ≥ conservative 20% on pilot traffic | POC-gate agent |
| R2 | Savings booked as "capacity" never materialize into budget relief | 4 | 3 | 12 | Quarterly realized-savings review vs lever math; redeployment plan with named moves by Q1 2027 | K. Doyle + R. Vance |
| R3 | Build overruns 14 wk (integration surprises) | 3 | 3 | 9 | 15% contingency held; claims-platform API spike in wk 1–2 before squad ramps | Delivery TL |
| R4 | Run cost creep: eval maintenance quietly grows past 0.25 FTE | 2 | 3 | 6 | Eval-maintenance hours tracked in observability cost panel (stage 11) | J. Iyer |
| R5 | Volume growth assumption (6%) wrong in either direction distorts the do-nothing comparison | 2 | 2 | 4 | Sensitivity uses flat volume for the funded case — growth only strengthens it | K. Doyle |

## Assumptions & open questions

1. `[assumption — confirm]` $92/hr blended squad rate (internal + partner mix); procurement to confirm by kickoff.
2. `[assumption — confirm]` Flat savings across yrs 1–3; no credit for volume growth or phase-2 lines.
3. `[assumption — confirm]` 6% volume growth for the do-nothing model only.
4. **Open (inherited):** Pro-fallback rate (18% vs up to 30%) — immaterial to the case but bounds the FinOps model in stage 5.
5. `[assumption — confirm]` Redeployment (not backfill-freeze) is the realization mechanism; workforce plan due before launch.

## Sign-off (HITL gate) — Finance

- **K. Doyle, Finance Business Partner** — signed 2026-07-18 → unlocks stage 5 spend.
- Conditions: (a) POC gate must show measured STP ≥20% before scale rollout;
  (b) realized-savings review quarterly.

## Handoff to stage 5 (architecture)

**You consume:** the funded envelope ($371K build / $165K run), the $0.09/packet
unit-cost bar with $0.048 expected, and the fallback-rate open question.
**Your job:** pick the cloud with a like-for-like 4-way comparison, produce the
PII/PHI controls matrix compliance signed up for, and verify the two feasibility
unknowns that carry financial risk: Snowflake lookup p95 and claims-platform API
write path. **Still open for you:** CAT-surge SLA policy (PRD Q5) — it sizes
your serving tier.
