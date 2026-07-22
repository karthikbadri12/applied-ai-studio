# Applied AI Studio — Architecture

A domain-agnostic, IDE-native **agent system** that takes an executive problem
statement and drives it through the full **AI Development Life Cycle (ADLC)** —
from a one-line VP ticket to a funded, governed, production-ready delivery plan,
and then hands a spec to a downstream coding pipeline.

It is not a chatbot. It is an org chart of specialist agents governed by a shared
constitution and a single orchestrator.

---

## The three layers

```
┌──────────────────────────────────────────────────────────────────────────┐
│  LAYER 1 — SETTINGS / REGISTRY   (registry/agents.json, registry/stages.json)│
│  The catalog: which agents exist, their type, their stage, their artifact.   │
│  This is what an IDE reads to "install" the agents.                          │
└──────────────────────────────────────────────────────────────────────────┘
                                   │
┌──────────────────────────────────────────────────────────────────────────┐
│  LAYER 2 — GOVERNANCE & ORCHESTRATION                                        │
│  CONSTITUTION.md   →  rules every agent obeys (safety, HITL, evidence)       │
│  orchestrator      →  routes the problem, sequences stages, enforces gates   │
│  advisors ─────────→  advise the ADMINISTRATOR (orchestrator + human owner)  │
└──────────────────────────────────────────────────────────────────────────┘
                                   │
┌──────────────────────────────────────────────────────────────────────────┐
│  LAYER 3 — EXECUTION                                                          │
│  Each agent knows one job: its inputs, its output artifact, its HITL gate.   │
│  Pipeline agents run in sequence; advisory agents are consulted on demand.   │
└──────────────────────────────────────────────────────────────────────────┘
```

**Administrator model.** The *administrator* is the pairing of the orchestrator
agent and the human owner (the FDE / delivery lead). Advisory agents never act on
the world; they produce recommendations **to the administrator**. The
administrator decides. Some decisions are reserved for the human — those are the
**human-in-the-loop (HITL) gates** (see `CONSTITUTION.md`).

---

## The agents

### Pipeline agents — the ADLC spine (run in order)

| # | Agent | Consumes | Produces (artifact) | HITL gate |
|---|-------|----------|---------------------|-----------|
| 1 | `intake` | VP problem statement | **Signed PRD** | Sponsor signs PRD |
| 2 | `process-map` | PRD + SOP | Step table tagged Human/Machine | — |
| 3 | `assess` | Machine steps | Solution verdict (ML/GenAI/Hybrid/Agentic) + model shortlist | — |
| 4 | `value-prop` | Verdict + VP numbers | Quantified business case (ROI, payback) | Finance signs case |
| 5 | `architecture` | Verdict + data class + funded case | Reference architecture + model strategy | — |
| 6 | `dev-spec` | Verdict + arch | AI Spec + RAG blueprint + agent toolchain + CI eval gate | — |
| 7 | `data-science` | AI Spec | Prompts/features + experiment log + retraining plan | — |
| 8 | `eval` | Eval threshold | Golden + adversarial + regression sets + metric bars | — |
| 9 | `poc-gate` | Metric bars + PRD metric | **GO / CONDITIONAL / NO-GO** verdict | Sponsor approves gate |
| 10 | `production` | Passing POC + guardrails | Production + responsible-AI checklists | Security/Compliance sign-off |
| 11 | `observability` | SLOs + controls | Golden signals, dashboards, alerts, cost attribution | — |
| 12 | `brief` | Everything above | End-to-end delivery brief (capstone) | Owner approves brief |

### Advisory agents — consulted by the orchestrator, advise the administrator

| Agent | Advises on |
|-------|-----------|
| `model-selector` | Task → tier → managed vs open model pick, routing/fallback cascade |
| `cloud-gcp` | Vertex AI, Gemini, BigQuery ML, Agent Builder, GKE |
| `cloud-aws` | Bedrock, SageMaker, Kendra, Step Functions, ECS/EKS |
| `cloud-azure` | Azure AI Foundry, Azure OpenAI, AI Search, ML Studio |
| `cloud-onprem` | Open-source stack: vLLM/Ollama, Airflow, Milvus/pgvector, Ray |
| `connector-advisor` | How to connect Snowflake, Databricks, BigQuery, Bedrock, etc. |
| `domain-advisor` | Industry regulations, data sources, sensitivities (15 domains) |

### Downstream dev pipeline — a separate, packaged pipeline (see `pipelines/dev-pipeline.md`)

| Agent | Job |
|-------|-----|
| `discovery` | Ingest the AI Spec + brief, map the target codebase, produce a build backlog |
| `coder` | Implement stories against the AI Spec |
| `code-reviewer` | Review against the spec, guardrails, and eval gate before merge |

The dev pipeline is deliberately decoupled: the ADLC spine produces an **AI Spec**
artifact; the dev pipeline **consumes** it. You can run the planning spine without
ever touching code, then hand the spec to the coding agents when funded.

---

## How a request flows

```
VP: "Our claims team is drowning — 40k FNOL calls/month, 6-min handle time."
        │
        ▼
  orchestrator  ── loads CONSTITUTION, picks domain-advisor(insurance)
        │
        ▼
  intake ──► asks the clarifying questions ──► Signed PRD  ◀── HITL: sponsor
        │
        ▼
  process-map ──► assess ──► (consults model-selector + cloud-* + domain-advisor)
        │                     ──► solution verdict + model shortlist
        ▼
  value-prop  ◀── HITL: finance   ──► architecture ──► dev-spec
        │
        ▼
  data-science ──► eval ──► poc-gate  ◀── HITL: sponsor GO/NO-GO
        │
        ▼
  production ◀── HITL: security ──► observability ──► brief ◀── HITL: owner
        │
        ▼
  [ AI Spec ] ──────────────► dev-pipeline: discovery ──► coder ──► code-reviewer
```

Every stage writes a file into `artifacts/` using the matching template in
`artifacts/templates/`. The artifact of stage N is the input contract of stage N+1.

---

## Portability across IDEs

The **canonical** agent definitions live in `.claude/agents/*.md` (Claude Code /
Anthropic subagent format: YAML frontmatter + a system prompt body).

- **Claude Code** (VS Code, JetBrains, terminal): reads `.claude/agents/` natively.
- **Cursor**: reads `AGENTS.md` and `.cursor/rules/*.mdc` (thin pointers to the packs).
- **Antigravity / VS Code agents / Codex**: read the `AGENTS.md` standard.
- **Connectors**: `connectors/mcp.example.json` is a Model Context Protocol config
  that Claude Code, Cursor, and Antigravity all consume to reach live data systems.

One source of truth, four IDEs. See `README.md` for install steps per IDE.
