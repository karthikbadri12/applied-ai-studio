# Applied AI Enterprise

**A domain-agnostic Applied-AI agent system you install into your IDE.** Drop in an
executive problem statement — *"our claims team is drowning in 40k calls a month"* —
and a roster of specialist agents drives it through the full **AI Development Life
Cycle**: clarifying questions, a signed PRD, a solution verdict, a model + cloud
strategy, a business case, evals, a go/no-go gate, a production plan, and a buildable
spec — with a human in the loop at every decision that matters.

It runs natively in **Claude Code**, and via the `AGENTS.md` standard in **Cursor,
VS Code, and Antigravity**. Connectors (Snowflake, Databricks, BigQuery, Bedrock…)
plug in over **MCP**.

> Not a chatbot. An org chart of specialist agents governed by a shared constitution
> and a single orchestrator — the way a Forward Deployed team actually delivers.

---

## Why this exists

Most "AI initiatives" die the same three deaths: no one defined the problem, no one
could prove it worked, or no one thought about production until it broke. This pack
encodes the discipline that prevents all three — as agents you can run.

- **Executives** get a decision-grade brief, not a science project.
- **PMs / BAs** get the clarifying-question rigor and artifacts at every stage.
- **Engineers** get an unambiguous, testable AI Spec to build against.
- **Everyone** gets the human-in-the-loop gates and the audit trail regulators want.

## The architecture (three layers)

```
 SETTINGS   registry/agents.json · registry/stages.json   ← the catalog an IDE installs
 GOVERNANCE CONSTITUTION.md · orchestrator · advisors      ← rules + routing + advice
 EXECUTION  12 pipeline agents + dev pipeline              ← each knows one job + artifact
```

**The administrator = orchestrator + human.** Advisors advise; the administrator
decides; some decisions are reserved for the human (the HITL gates). Full picture in
[ARCHITECTURE.md](ARCHITECTURE.md).

## The agents (25)

| Group | Agents |
|-------|--------|
| **Orchestrator** | `orchestrator` — routes the problem, sequences stages, enforces gates |
| **ADLC pipeline (12)** | `intake` → `process-map` → `assess` → `value-prop` → `architecture` → `dev-spec` → `data-science` → `eval` → `poc-gate` → `production` → `observability` → `brief` |
| **Advisors (7)** | `model-selector` · `cloud-gcp` · `cloud-aws` · `cloud-azure` · `cloud-onprem` · `connector-advisor` · `domain-advisor` |
| **Dev pipeline (3)** | `discovery` → `coder` → `code-reviewer` (decoupled; consumes the AI Spec) |

Each stage produces a real artifact ([templates](artifacts/templates/)): Intake → a
**signed PRD**, Assess → a **solution verdict + model shortlist**, POC gate → a
**GO / NO-GO**, Brief → an **end-to-end delivery brief**. The artifact of stage N is
the input contract of stage N+1.

## The four cloud/technical agents (asked the same question)

`cloud-gcp`, `cloud-aws`, `cloud-azure`, and `cloud-onprem` each answer the *same*
architecture question so you compare **Vertex vs Bedrock vs Azure AI vs open-source
on-prem** like-for-like — then get one recommended path with the reason the other
three lost. On-prem covers the open-weight stack (vLLM, Llama/Mistral/Qwen, Airflow,
Milvus) for "must stay on-prem" mandates.

## Install

**With uv (recommended — works for every IDE):**
```bash
uvx --from aidlc-studio aidlc init --ide all
# per-IDE: --ide claude | cursor | copilot | antigravity
# then:    aidlc list · aidlc check
```
Full per-IDE guide: [docs/INSTALL.md](docs/INSTALL.md).

**Claude Code** (VS Code, JetBrains, terminal)
```bash
git clone <this-repo> && cd applied-ai-studio
claude   # the agents in .claude/agents/ are picked up automatically
```
Then: *"Act as the orchestrator. Here's my problem statement: …"*

**Cursor / Antigravity / VS Code agents**
- They read [AGENTS.md](AGENTS.md) and [.cursor/rules/](.cursor/rules/) automatically.
- Point the assistant at the repo and give it a problem statement; it adopts the
  orchestrator role and walks the pipeline.

**Connectors (optional, any IDE)**
- Copy the servers you need from [connectors/mcp.example.json](connectors/mcp.example.json)
  into your IDE's MCP config. Secrets go in a secret manager / gitignored `.env`.

## A 3-minute demo

1. Give the `orchestrator` a one-line problem statement.
2. Watch `intake` run the clarifying-question loop and produce `artifacts/01-prd.md`,
   then stop at the **sponsor sign-off** gate.
3. Approve it. Watch `assess` (consulting `model-selector` + the four cloud agents +
   `domain-advisor`) produce a solution verdict and a model + cloud comparison.
4. Continue to the **POC gate** — a GO / CONDITIONAL / NO-GO backed by evals — and the
   final **delivery brief** with the AI Spec handoff.

Everything lands as files in `artifacts/`, so the demo *shows its work*.

## 📄 Full documentation site

**[docs/index.html](docs/index.html)** — the professional overview: capabilities, the
complete end-to-end walkthrough, the agent roster, the 2026 cloud/framework matrix,
governance, and the proof. Open it in a browser (or serve `docs/` via GitHub Pages).

## Repo map

```
CONSTITUTION.md          the rules every agent obeys
HARNESS.md               runtime enforcement: guardrails, gates, audit ledger
QUALITY_BAR.md           per-artifact definition of done + the build contract
GOVERNANCE.md            EU AI Act tiers · NIST AI RMF · model risk management
EVALS.md                 evaluation doctrine: sets, bars, judges, CI gate
DISASTER_COMMAND.md      incident command for production AI
PRODUCT.md               vision, personas, OKRs, RICE roadmap
ARCHITECTURE.md          the three-layer design + request flow
AGENTS.md                cross-IDE entry (Cursor / Antigravity / VS Code)
registry/                agents · stages · phases · skills · frameworks (JSON)
.claude/agents/          all 25 agent definitions (canonical source)
.claude/skills/          14 skills + the /appliedai entry point
artifacts/templates/     the artifact each stage produces
exemplar/claims-idp/     gold-standard worked example + working eval-gated codebase
connectors/              catalog + MCP config + per-connector guides
domains/                 15-industry registry + deep packs (domain-agnostic core)
demo/RECORDING_SCRIPT.md scene-by-scene demo script
docs/                    index.html · architecture.html · INSTALL.md · diagrams.md
```

## What is AIDLC itself built with?

Deliberately, **no agent framework**. AIDLC is a *framework-agnostic agent system*:

- **Agents-as-instructions:** every agent is a versioned Markdown spec (charter,
  guardrails, skills, I/O contract) in `.claude/agents/`. The *execution engine* is
  whatever agentic runtime your IDE already has — Claude Code custom agents natively,
  or any `AGENTS.md`-standard assistant (Cursor, Copilot, Antigravity, Windsurf).
  No LangChain/LangGraph/ADK dependency to install, version, or secure.
- **Methodology layer:** Spec Kit (phase gates) + BMAD (persona pipeline) +
  Superpowers (composable skills) — see [SKILLS.md](SKILLS.md).
- **Governance layer:** a Constitution + runtime harness ([HARNESS.md](HARNESS.md))
  with hard/soft guardrails, five HITL gates, and an append-only audit ledger.
- **Connectors:** MCP (Model Context Protocol) — the one integration standard every
  major IDE speaks.
- **Packaging:** a small stdlib-only Python CLI (`aidlc`), built with hatchling,
  installed via **uv/uvx** — the same distribution pattern as GitHub's Spec Kit.

The solutions AIDLC *designs* do get a framework recommendation — chosen by the
winning cloud advisor from [registry/frameworks.json](registry/frameworks.json):
**GCP → Google ADK** (deploy: Vertex AI Agent Engine) · **AWS → Strands Agents +
Bedrock AgentCore** · **Azure → Microsoft Agent Framework + AI Foundry Agent
Service** · **on-prem → self-hosted LangGraph over vLLM/Ollama** — each with named
alternates, and "no framework" stated when a plain pipeline is the simpler answer.

## Design principles

1. **Ask before you build** — no PRD from a one-liner; the intake question loop is mandatory.
2. **Evidence over assertion** — every number is labelled; nothing is fabricated.
3. **Human-final** — the reserved decisions stop the pipeline until a person approves.
4. **One recommended path** — with the alternatives and why they lost. No paralysis.
5. **Artifacts are the interface** — the whole initiative is legible from the files.

---

*Built as a portable agent pack — one source of truth, four IDEs. Fork it, point it at
your problem, and let the org chart run.*
