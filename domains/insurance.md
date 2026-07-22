# Domain frame — Insurance

> Loaded by `domain-advisor`. Practitioner guidance, not legal advice. Uncertain
> points route to compliance/legal as a HITL gate.

## Hard regulatory constraints
- **State insurance codes** — regulation is state-by-state; a model touching rating,
  underwriting, or claims may need filed/approved methodology.
- **NAIC Model Bulletin on AI** — governance, testing for unfair discrimination, and
  documentation of AI systems used in insurance decisions.
- **Unfair Claims Settlement Practices Acts** — claims handling must be fair and
  timely; a bad automated denial is bad-faith exposure.
- **GLBA** privacy; **PHI** rules apply on health/disability/workers-comp lines.

## Regulated data classes present
**PII**, and **PHI** on health-adjacent lines.

## Typical systems & data sources
Policy admin (Guidewire PolicyCenter), claims (ClaimCenter), FNOL intake, billing,
actuarial/rating engines, third-party data (telematics, medical, weather).

## Mandatory human-in-the-loop points
- **Adjuster decision** on claim approval/denial/payout — AI triages and drafts; a
  licensed adjuster decides.
- **Underwriter sign-off** on risk selection and pricing.

## Proven patterns (and pitfalls)
- **FNOL intake** — GenAI to structure the first-notice call/form; strong fit.
  Pitfall: mis-captured facts flow downstream — validate extraction hard.
- **Claims triage / severity routing** — Hybrid (ML score + GenAI summary); route,
  don't decide.
- **Fraud detection** — ML scoring + investigator review; keep it explainable for
  regulatory defensibility.
- **Underwriting assist** — assist only; unfair-discrimination testing is a gate.

## Failure cost (sets eval-bar severity)
Bad-faith claims liability, regulatory action, mispriced risk / reserve error.
Fairness and accuracy on denials are pass/fail gates.
