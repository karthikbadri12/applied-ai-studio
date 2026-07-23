# Install — load Applied AI Enterprise as custom agents in your IDE

One source of truth (`.claude/agents/` + `AGENTS.md` + `registry/`), installable in
every major AI IDE. Every path below is: **① install prerequisites → ② scaffold the
pack → ③ open the project → ④ verify → ⑤ run → ⑥ fix if broken.**

## How a run works in EVERY IDE (read this once)

Whatever the IDE, you start the pipeline the same way — give the orchestrator a
problem statement:

> **"Start AIDLC. Problem statement: our claims team processes 2,400 packets a week
> at 22 minutes each — can AI help?"**

What happens next, in order:
1. It asks you **one batched set of numbered questions** (cloud/stack, connectors +
   credential env-var names, model token, plan-vs-build). Answer in chat.
2. It runs the stages and writes files into `artifacts/` in your project.
3. At each decision reserved for humans it prints a **`⛔ HUMAN GATE`** message and
   **stops**. You reply `approved` (or your decision) in chat to continue.
   - In **Claude Code** gates can also appear as interactive prompts.
   - In **Cursor / Copilot / Antigravity / Windsurf** there are **no popups** —
     the ⛔ chat message *is* the gate. This is expected, not a bug.

---

## 0. Prerequisite for all paths: uv (one-time, 30 seconds)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Close and reopen your terminal, then check: `uvx --version`.

---

## 1. Claude Code (VS Code, JetBrains, terminal, desktop) — the full experience

**Global — agents in every folder you ever open (recommended for individuals):**
```bash
uvx --from aidlc-studio aidlc init --global
```
This installs a **clean picker**: only `orchestrator` appears as a custom agent;
the other 22 workers live in `~/.claude/aidlc/agents/` and are delegated to
automatically. The `/aidlc` slash command is installed too.

1. Open **any** folder in VS Code → open Claude Code (or run `claude` in a terminal).
2. Restart/reload once after installing (the picker caches).
3. Verify: type `/agents` → you should see `orchestrator`. Type `/aidlc` → the
   skill should be recognized.
4. Run: `/aidlc <your problem statement>`.
5. Update later: re-run the install command with `--force`.
   Prefer all 23 in the picker? Add `--roster full`.

**Project-scoped — ship the agents WITH a team repo:**
```bash
cd ~/code/your-project
uvx --from aidlc-studio aidlc init --ide claude
claude
```
Verify with `/agents` (all 23 appear — project installs don't hide the roster).
Commit the files; every teammate gets them on clone.

**Connectors:** copy the servers you need from `connectors/mcp.example.json` into
the project's `.mcp.json` (or `claude mcp add`). Secrets go in env vars, never files.

**If it misbehaves:** agents missing from `/agents` → reload the window; still
missing → `uvx --from aidlc-studio aidlc check`
in the project (or check `~/.claude/agents/` exists for global).

---

## 2. Cursor — step by step

1. **Scaffold** (in Cursor's built-in terminal, at your project root):
   ```bash
   uvx --from aidlc-studio aidlc init --ide cursor
   ```
   This writes: `AGENTS.md` (the roster + rules), `.cursor/rules/applied-ai-studio.mdc`
   (an always-on rule that tells Cursor to act as the orchestrator and honor the
   gates), plus the constitution, registries, and templates.
2. **Open the folder in Cursor** (File → Open Folder). If it was already open:
   Cmd+Shift+P → *"Reload Window"*.
3. **Verify it loaded:** Cursor Settings (Cmd+Shift+J) → **Rules** → under
   *Project Rules* you should see `applied-ai-studio` with **Always** apply.
   If the list is empty, the folder you opened is not the folder you scaffolded —
   check that `.cursor/rules/applied-ai-studio.mdc` exists at the workspace root.
4. **Run:** open chat (Cmd+L), select **Agent** mode (dropdown at the bottom of the
   chat panel), and type:
   > Start AIDLC. Problem statement: …
5. **Gates:** arrive as `⛔ HUMAN GATE` chat messages. Reply `approved` to continue.
   Artifacts appear in `artifacts/` in your file tree as each stage completes.
6. **Optional — a dedicated mode:** Settings → Chat → Custom Modes → *New mode* →
   name it `AIDLC` → instructions: *"Follow .claude/agents/orchestrator.md and
   CONSTITUTION.md exactly; run the AIDLC pipeline per AGENTS.md."* Then pick
   `AIDLC` from the mode dropdown instead of typing the kickoff phrase.
7. **Connectors (optional):** create `.cursor/mcp.json` and paste the server blocks
   you need from `connectors/mcp.example.json`. Cursor Settings → MCP shows the
   connected servers; secrets stay in env vars.

**If it misbehaves:** Cursor answers generically → the rule didn't load (step 3);
it writes a PRD instantly without questions → say *"You skipped the intake question
loop — re-read AGENTS.md and CONSTITUTION.md and start again"*.

---

## 3. VS Code with GitHub Copilot — step by step

Requires: VS Code **1.101+**, GitHub Copilot + Copilot Chat extensions signed in.

1. **Scaffold** (VS Code terminal, project root):
   ```bash
   uvx --from aidlc-studio aidlc init --ide copilot
   ```
   This writes `AGENTS.md` **and generates `.github/chatmodes/` — all 23 agents as
   ready-made custom chat modes** (orchestrator.chatmode.md, intake.chatmode.md, …).
   Nothing to copy by hand.
2. **Reload:** Cmd+Shift+P → *"Reload Window"* (chat modes are discovered on load).
3. **Enable AGENTS.md support:** Settings (Cmd+,) → search `agents md` → check
   **Chat: Use Agents Md File** (`chat.useAgentsMdFile: true`).
4. **Verify:** open Copilot Chat (Ctrl+Cmd+I) → click the **mode dropdown** at the
   top of the chat input (where Ask / Edit / Agent live) → you should see
   **orchestrator** and the other custom modes listed.
   Not there? → Settings → search `chat.modeFilesLocations` → ensure it includes
   `.github/chatmodes` → reload again.
5. **Run:** select the **orchestrator** mode, then type:
   > Start AIDLC. Problem statement: …
6. **Gates:** Copilot has **no popup mechanism for custom agents** — the
   `⛔ HUMAN GATE` message in chat *is* the gate; reply `approved` in chat.
   Copilot's own confirmation dialogs (run this command? apply this edit?) still
   appear for terminal/file actions — approve those as normal.
7. **Know the limits:** no `/aidlc` slash command, no true sub-agent spawning —
   the selected mode role-plays the pipeline from the same files. Quality tracks
   the model you pick in Copilot's model selector.

---

## 4. Google Antigravity — step by step

1. **Scaffold** (terminal, project root):
   ```bash
   uvx --from aidlc-studio aidlc init --ide antigravity
   ```
2. **Open the folder as a workspace** in Antigravity. It reads `AGENTS.md` from the
   repo root automatically as workspace guidance.
3. **Run (chat):** in the sidebar chat, type the kickoff phrase from the top of
   this doc.
   **Run (Agent Manager, better for long runs):** open the Agent Manager surface →
   new task → paste:
   > Act as the orchestrator per AGENTS.md. Run the full AIDLC pipeline. Problem
   > statement: … Stop at every ⛔ HUMAN GATE and wait for my decision.
   Antigravity executes it as a long-running agent task; artifacts land in
   `artifacts/` exactly as in Claude Code, and its own Artifacts panel shows the
   task plan/walkthrough.
4. **Gates:** ⛔ chat/task messages — reply with your decision to resume.
5. **Connectors:** Antigravity supports MCP — Settings → MCP servers → paste the
   blocks you need from `connectors/mcp.example.json`.

---

## 5. Windsurf / Codex CLI / Amp / other AGENTS.md-aware tools

1. Scaffold with the generic flavor:
   ```bash
   uvx --from aidlc-studio aidlc init --ide windsurf
   ```
2. Open the folder. Any tool honoring the `AGENTS.md` standard loads the roster and
   rules automatically.
3. Type the kickoff phrase. Gates arrive as ⛔ chat messages; artifacts land in
   `artifacts/`.
4. (Windsurf) Connectors: Settings → MCP → paste blocks from
   `connectors/mcp.example.json`.

---

## One project, every IDE at once

```bash
uvx --from aidlc-studio aidlc init --ide all
```
Writes every flavor side by side — your teammate on Cursor, another on Copilot, and
you on Claude Code all get the same pipeline from the same repo.

Useful CLI extras:
```bash
aidlc list    # the 23-agent roster with BMAD persona + Spec Kit phase
aidlc check   # verify an install (core files + at least one IDE flavor, exit code)
```
`init` never overwrites existing files unless you pass `--force`. Installing from
the bleeding-edge repo instead of the PyPI release:
`uvx --from git+https://github.com/karthikbadri12/applied-ai-enterprise.git aidlc init …`

---

## What "installed" gets you (any IDE)

| Capability | Where it comes from |
|------------|---------------------|
| 23 custom agents (4 phases + advisors + dev pipeline) | `.claude/agents/*.md` (canonical) |
| 14 composable skills (Spec Kit · BMAD · Superpowers) | `.claude/skills/` + `registry/skills.json` |
| The rules of engagement + runtime harness | `CONSTITUTION.md` · `HARNESS.md` · `QUALITY_BAR.md` |
| Stage order, phases, artifacts, human gates | `registry/stages.json` · `registry/phases.json` |
| Cloud → agent-framework matrix (ADK/Strands/MAF/LangGraph) | `registry/frameworks.json` |
| Per-stage artifact templates + gold exemplar | `artifacts/templates/` · `exemplar/claims-idp/` |
| Live data connections | `connectors/mcp.example.json` (MCP) |
| 15 industry frames | `domains/` |

## Smoke test (2 minutes, any IDE)

1. Open the scaffolded project in your IDE's AI chat (orchestrator mode where applicable).
2. Say: *"Start AIDLC. Problem statement: invoice processing takes my AP team 4 days
   per cycle."*
3. ✅ **Pass** = it asks numbered questions (metric/scope/data/cloud/connectors)
   **before** writing anything, then produces `artifacts/01-prd.md` and stops at
   `⛔ HUMAN GATE — Sponsor signs PRD`.
4. ❌ **Fail** = it writes a PRD instantly with invented numbers → the pack isn't
   loaded; go to your IDE's *verify* step above.
