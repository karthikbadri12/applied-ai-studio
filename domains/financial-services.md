# Domain frame — Financial Services & Banking

> Loaded by `domain-advisor`. Practitioner guidance, not legal advice. Uncertain
> points route to compliance/legal as a HITL gate.

## Hard regulatory constraints
- **SR 11-7 (model risk management)** — models need documentation, validation, and
  ongoing monitoring by an independent function. Your `eval` + `observability`
  artifacts are the backbone of this.
- **ECOA / Reg-B + FCRA** — any credit decision requires an **adverse-action notice**
  with specific reasons → the model must be explainable; black-box declines are illegal.
- **Fair-lending** — disparate-impact testing is mandatory for lending decisions.
- **GLBA** (privacy/safeguards), **SOX** (controls), **AML/BSA/KYC**, **PCI-DSS** for card data.

## Regulated data classes present
**PII**, **MNPI** (material non-public info — strict information barriers), **PCI**.

## Typical systems & data sources
Core banking (FIS/Fiserv/Temenos), card networks, market-data feeds, credit bureaus,
CRM (Salesforce Financial Services Cloud), transaction stores.

## Mandatory human-in-the-loop points
- **Adverse-action review** on any automated credit decline (with reasons).
- **Human disposition of AML/fraud alerts** before account action (SAR filing is human).
- Trader / advisor sign-off on anything client-facing or trade-affecting.

## Proven patterns (and pitfalls)
- **Fraud / AML alert triage** — strong ML fit; GenAI to summarize the case for the
  investigator. Pitfall: unexplained scores fail model-risk review — keep features
  interpretable.
- **Loan underwriting assist** — assist only; explainability + fair-lending tests are
  gates, not nice-to-haves.
- **Research / document summarization** — good GenAI fit; enforce MNPI barriers so
  context from one desk never leaks to another.

## Failure cost (sets eval-bar severity)
Regulatory fines, discriminatory-lending liability, market loss, consent orders.
Explainability and fairness are **gates**.
