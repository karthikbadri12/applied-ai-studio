# Domain frame — Healthcare & Life Sciences

> Loaded by `domain-advisor`. Practitioner guidance, not legal advice. Anything
> uncertain routes to compliance/legal counsel as a HITL gate.

## Hard regulatory constraints
- **HIPAA / HITECH** — PHI must be encrypted in transit & at rest; minimum-necessary
  access; BAAs with every processor (including the model provider); breach notification.
- **FDA** — if the output influences diagnosis/treatment, it may be **Software as a
  Medical Device (SaMD)**; clinical validation and possible clearance apply. Flag early.
- **21 CFR Part 11** — e-records/e-signatures in regulated workflows.
- State privacy laws (e.g. CMIA in CA) may exceed HIPAA.

## Regulated data classes present
**PHI** (the big one), **PII**. Tag at `assess`; control at `architecture`/`production`.

## Typical systems & data sources
EHR (Epic, Cerner/Oracle Health), **HL7 v2 / FHIR** interfaces, PACS (imaging),
claims (837/835), lab (LIS). Expect FHIR APIs and a lot of unstructured clinical text.

## Mandatory human-in-the-loop points
- **A clinician signs off** on any output that informs diagnosis, treatment, or
  triage. AI assists; it does not decide care.
- Physician-in-the-loop for anything patient-facing with clinical content.

## Proven patterns (and pitfalls)
- **Prior-authorization triage / RAG** — strong fit; ground answers in payer policy
  docs. Pitfall: hallucinated policy criteria → deny/approve errors. Hard eval needed.
- **Clinical documentation (ambient scribe)** — high value; pitfall: fabricated
  findings in the note. Adversarial evals on omission/hallucination are non-negotiable.
- **Medical coding assist** — good ROI; keep a human coder in the loop for billing.
- Graveyard: autonomous diagnosis without clinician sign-off — regulatory + safety wall.

## Failure cost (sets eval-bar severity)
Patient harm, OCR fines (per-record), loss of accreditation/license. Safety metrics
are pass/fail gates, never averaged away.
