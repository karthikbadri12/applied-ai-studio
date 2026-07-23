# AIDLC — Component Diagrams

Each component individually, then the complete connection map. (Mermaid — renders
on GitHub and in most IDEs.) Machine-readable phase map: `registry/phases.json`.

---

## P1 · Intent & Discovery

```mermaid
flowchart LR
    VP(["VP problem statement"]) --> ORCH["orchestrator\n(classifies domain, applies harness)"]
    ORCH -.consult.-> DA["domain-advisor\nregs · data classes · HITL points"]
    ORCH --> INTAKE["intake\nSocratic question loop"]
    INTAKE --> PRD[["01-prd.md\nSigned PRD"]]
    PRD --> GATE1{{"⛔ Sponsor signs PRD"}}
    GATE1 --> PMAP["process-map\nas-is → to-be steps"]
    PMAP --> A2[["02-process-map.md\nHuman/Machine step table"]]
```

## P2 · Assess & Architecture

```mermaid
flowchart LR
    A2[["02-process-map.md"]] --> ASSESS["assess\nML / GenAI / Hybrid / Agentic verdict"]
    ASSESS -.consult.-> MS["model-selector"]
    ASSESS -.consult.-> DA["domain-advisor"]
    ASSESS --> A3[["03-assessment.md"]]
    A3 --> VPROP["value-prop\nROI · payback · NPV"]
    VPROP --> A4[["04-business-case.md"]]
    A4 --> GATE2{{"⛔ Finance approves"}}
    GATE2 --> ARCH["architecture"]
    ARCH -.same question to all four.-> GCP["cloud-gcp"] & AWS["cloud-aws"] & AZ["cloud-azure"] & ONP["cloud-onprem"]
    ARCH -.consult.-> CONN["connector-advisor"]
    ARCH --> A5[["05-architecture.md\nwinner + named losers + controls matrix"]]
    A5 --> DSPEC["dev-spec"]
    DSPEC --> A6[["06-ai-spec.md\nbars · schemas · build file-tree"]]
```

## P3 · Build, Test & Execute

```mermaid
flowchart LR
    A6[["06-ai-spec.md"]] --> DS["data-science\nprompts · experiments"]
    DS --> A7[["07-data-science.md"]]
    A6 --> DISC["discovery\nbacklog → ≤2-min micro-tasks"]
    DISC --> TASKS[["dev/tasks.json\nwaves · checkpoints"]]
    TASKS --> CODER["coder\nparallel waves, checkpoint per task"]
    CODER --> BUILD[["build/ repo\nsrc · evals · tests · CI · infra"]]
    A7 --> EVAL["eval\ngolden · adversarial · regression"]
    BUILD --> EVAL
    EVAL --> A8[["08-evals.md + bars.yaml results"]]
    A8 --> POC["poc-gate\nevidence vs PRD metric"]
    POC --> A9[["09-poc-gate.md"]]
    A9 --> GATE3{{"⛔ Sponsor GO / NO-GO"}}
```

## P4 · Review & Observability

```mermaid
flowchart LR
    BUILD[["build/ repo"]] --> CR["code-reviewer\nspec + guardrails + eval gate"]
    CR -->|CHANGES REQUESTED| CODER["back to coder"]
    CR -->|MERGE| PROD["production\nlaunch blockers · responsible AI"]
    PROD --> A10[["10-production.md"]]
    A10 --> GATE4{{"⛔ Security & Compliance"}}
    GATE4 --> OBS["observability\nsignals · alerts · cost attribution"]
    OBS --> A11[["11-observability.md"]]
    A11 --> BRIEF["brief\nassembles everything · reconciles audit"]
    BRIEF --> A12[["12-delivery-brief.md"]]
    A12 --> GATE5{{"⛔ Owner approves brief"}}
```

## The harness (wraps every invocation above)

```mermaid
flowchart LR
    PRE["pre-flight\nartifact? gate? skills?\ndata-class approved?"] --> EXEC["execute\nhard/soft guardrails live"]
    EXEC --> POST["post-flight\nQUALITY_BAR check\nno secrets · evidence"]
    POST --> AUD[("audit.jsonl\nappend-only ledger")]
    AUD --> G{"HITL gate?"}
    G -->|yes| H["⛔ administrator decides\n(decision → audit event)"]
    G -->|no| NXT["next stage"]
    EXEC -->|hard violation| BLOCK["BLOCK → surface to administrator"] --> AUD
```

## The micro-task engine (inside P3)

```mermaid
flowchart LR
    STORY["story"] --> SPLIT["split: atomic tasks ≤ 2 min\n(one file / one function / one test)"]
    SPLIT --> W1["wave 1\n(no deps — run in parallel)"]
    W1 --> CK1[("tasks.json\nstatus: done ✓")]
    CK1 --> W2["wave 2\n(deps satisfied)"]
    W2 --> CK2[("checkpoint")]
    CK2 --> MORE["…wave N"]
    MORE --> VERIFY["make test · make eval\ngreen before review"]
    CK1 -.crash? resume from last checkpoint.-> W2
```

## Complete connection map

```mermaid
flowchart TB
    subgraph GOV["Governance (cross-cutting)"]
        CONST["CONSTITUTION.md"] --- QB["QUALITY_BAR.md"] --- HARN["HARNESS.md"]
        ORCH["orchestrator"]
        AUDIT[("audit.jsonl + metrics.json")]
    end
    subgraph ADV["Advisors (recommend only → administrator)"]
        MS["model-selector"]; DA["domain-advisor"]; CONN["connector-advisor"]
        GCP["cloud-gcp"]; AWS["cloud-aws"]; AZ["cloud-azure"]; ONP["cloud-onprem"]
    end
    subgraph P1["P1 · Intent & Discovery"]
        INTAKE["intake"] --> PMAP["process-map"]
    end
    subgraph P2["P2 · Assess & Architecture"]
        ASSESS["assess"] --> VPROP["value-prop"] --> ARCH["architecture"] --> DSPEC["dev-spec"]
    end
    subgraph P3["P3 · Build, Test & Execute"]
        DS["data-science"] --> DISC["discovery"] --> CODER["coder"] --> EVAL["eval"] --> POC["poc-gate"]
    end
    subgraph P4["P4 · Review & Observability"]
        CR["code-reviewer"] --> PROD["production"] --> OBS["observability"] --> BRIEF["brief"]
    end
    USER(["administrator\n(human)"])
    VPIN(["VP problem statement"]) --> ORCH
    ORCH --> P1 --> P2 --> P3 --> P4
    ADV -.recommendations.-> ORCH
    ORCH -.delegates + harness.-> P1 & P2 & P3 & P4
    P1 & P2 & P3 & P4 -.every event.-> AUDIT
    ORCH <-->|"⛔ 5 HITL gates"| USER
    BRIEF --> OUT(["delivery brief + working repo"])
```
