# Install — load Applied AI Studio as custom agents in your IDE

One source of truth (`.claude/agents/` + `AGENTS.md` + `registry/`), installable in
every major AI IDE.

---

## ⚡ The fast path — install with uv (recommended, Spec Kit-style)

Prereq (one-time): install [uv](https://docs.astral.sh/uv/):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Scaffold the agent pack into **any project**, for **any IDE**, straight from GitHub:
```bash
# everything (all IDE flavors)
uvx --from git+https://github.com/karthikbadri12/applied-ai-studio.git aidlc init

# or per-IDE
uvx --from git+https://github.com/karthikbadri12/applied-ai-studio.git aidlc init --ide claude
uvx --from git+https://github.com/karthikbadri12/applied-ai-studio.git aidlc init --ide cursor
uvx --from git+https://github.com/karthikbadri12/applied-ai-studio.git aidlc init --ide copilot      # generates .github/chatmodes/
uvx --from git+https://github.com/karthikbadri12/applied-ai-studio.git aidlc init --ide antigravity  # AGENTS.md standard
```

Or install the CLI once and reuse it everywhere:
```bash
uv tool install git+https://github.com/karthikbadri12/applied-ai-studio.git
aidlc init ~/code/my-project --ide all
aidlc list     # show the 23-agent roster with BMAD persona + Spec Kit phase
aidlc check    # verify an install (core files + at least one IDE flavor)
```

`init` is non-destructive (skips existing files; `--force` overwrites). After
publishing to PyPI, this shortens to `uvx aidlc-studio aidlc init`.

The sections below are the manual (no-uv) paths per IDE — and what `init` sets up.

---

## 1. Claude Code (VS Code, JetBrains, terminal, desktop) — native

**Option A — project-scoped (recommended for the demo):**
```bash
git clone <your-repo-url> applied-ai-studio
cd applied-ai-studio
claude
```
That's it. Claude Code auto-discovers every agent in `.claude/agents/` as a **custom
subagent** and every skill in `.claude/skills/`. Verify with the `/agents` command —
you'll see all 23 (orchestrator, intake, assess, cloud-gcp, …).

**Option B — global (available in EVERY project you open):**
```bash
cp -R applied-ai-studio/.claude/agents/* ~/.claude/agents/
cp -R applied-ai-studio/.claude/skills/* ~/.claude/skills/
```
Note: global agents reference repo files (CONSTITUTION.md, registry/, templates). For a
full pipeline run, work inside the repo — or copy those folders alongside.

**Run it:**
> "Use the **orchestrator** agent. Problem statement: our care team handles 2M
> contacts/quarter at 11-min AHT across 6 systems — can AI help?"

Claude Code will delegate to `intake`, ask the clarifying questions, write
`artifacts/01-prd.md`, and stop at the sponsor gate.

**Connectors:** copy the blocks you need from `connectors/mcp.example.json` into the
project's `.mcp.json` (or add via `claude mcp add`). Secrets in env/secret manager.

---

## 2. Cursor

Cursor reads two things automatically when you open the repo:
- **`AGENTS.md`** (the cross-tool standard) — the roster, the flow, the rules.
- **`.cursor/rules/applied-ai-studio.mdc`** (`alwaysApply: true`) — tells Cursor to act
  as the orchestrator, adopt each agent's file as its role prompt, obey the
  Constitution, and stop at human gates.

**Run it:** open the repo, then in chat/Composer:
> "Act as the orchestrator per AGENTS.md. Here's my problem statement: …"

**Custom modes (optional):** Cursor supports custom modes — create one named
"AIDLC Orchestrator" whose instructions are: *"Follow .claude/agents/orchestrator.md
and CONSTITUTION.md exactly."*

**Connectors:** put the MCP blocks in `.cursor/mcp.json`.

---

## 3. VS Code (GitHub Copilot agent mode)

- Copilot reads **`AGENTS.md`** at the repo root automatically (agent instructions
  standard).
- For per-agent chat modes, copy any agent file into `.github/chatmodes/<name>.chatmode.md`
  (frontmatter `description:` + the body as instructions) — e.g. an "intake" mode and an
  "orchestrator" mode.
- **Run it:** open agent mode → "Follow AGENTS.md; act as the orchestrator; here's my
  problem statement…"

---

## 4. Google Antigravity

- Antigravity's agents read **`AGENTS.md`** from the repo root — the roster and flow load
  as workspace guidance automatically.
- Its agent manager can run long tasks: give it the orchestrator role and a problem
  statement; artifacts land in `artifacts/` exactly as in Claude Code.
- **Connectors:** Antigravity supports MCP — paste the blocks from
  `connectors/mcp.example.json` into its MCP settings.

---

## 5. Windsurf / other AGENTS.md-aware tools

Any tool that honors the `AGENTS.md` standard (Windsurf, Codex CLI, Amp, …) picks the
pack up the same way: open the repo → the roster + rules load → say "act as the
orchestrator" → artifacts appear in `artifacts/`.

---

## What "installed" gets you (any IDE)

| Capability | Where it comes from |
|------------|---------------------|
| 23 custom agents (pipeline · advisors · dev) | `.claude/agents/*.md` |
| 14 composable skills (Spec Kit · BMAD · Superpowers) | `.claude/skills/` + `registry/skills.json` |
| The rules of engagement | `CONSTITUTION.md` (injected everywhere) |
| Stage order, artifacts, human gates | `registry/stages.json` |
| Per-stage artifact templates | `artifacts/templates/` |
| Live data connections | `connectors/mcp.example.json` (MCP) |
| 15 industry frames | `domains/` |

## Smoke test (2 minutes, any IDE)

1. Open the repo in your IDE's AI chat.
2. Say: *"Act as the intake agent. Problem: invoice processing takes my AP team 4 days
   per cycle. Ask me your clarifying questions."*
3. ✅ Pass = it asks numbered questions across metric/scope/data/constraints **before**
   writing anything, then produces `artifacts/01-prd.md` from the template and stops at
   the `⛔ HUMAN GATE` for sponsor sign-off.
4. ❌ Fail = it writes a PRD instantly with invented numbers → the Constitution isn't
   loaded; re-check the install steps above.
