# Domain frame — Manufacturing & Industrial

> Loaded by `domain-advisor`. Practitioner guidance, not legal advice. Safety-related
> uncertainty routes to the safety/engineering authority as a HITL gate.

## Hard regulatory / safety constraints
- **Functional safety** — an AI must **never** be able to bypass a safety interlock
  (SIS / e-stop / PLC safety logic). AI advises; safety systems remain authoritative.
- **OSHA** workplace safety; **ISO 9001** quality management; product-safety and
  recall obligations.
- **Export controls / IP** — process data and designs are often proprietary or
  export-controlled; on-prem or sovereign handling is common (favor `cloud-onprem`).

## Regulated data classes present
Proprietary/IP and operational data (usually not PII — but protect the IP).

## Typical systems & data sources
**MES**, **SCADA / PLC**, process **historian** (OSIsoft PI), **ERP** (SAP), **CMMS**
(maintenance), vision/sensor streams, quality (LIMS). Data is high-volume time-series
+ images; often air-gapped OT networks.

## Mandatory human-in-the-loop points
- **Operator confirmation** before any AI-suggested actuation on the line.
- Safety interlocks are out of scope for AI control — full stop.
- Maintenance work orders reviewed before execution.

## Proven patterns (and pitfalls)
- **Predictive maintenance** — classical ML on historian/sensor data; strong ROI.
  Pitfall: false alarms erode trust — tune precision, show the evidence.
- **Visual QC / defect detection** — computer vision; strong fit. Pitfall: drift as
  product/lighting changes — online eval + retrain trigger required.
- **Root-cause analysis** — GenAI over historian + maintenance logs to speed RCA.
- **Yield / process optimization** — ML with a human-approved control loop, never
  autonomous on safety-relevant setpoints.

## Failure cost (sets eval-bar severity)
Safety incident, line-down cost per hour, scrap, recall. Anything safety-adjacent is
a pass/fail gate with human authority retained.
