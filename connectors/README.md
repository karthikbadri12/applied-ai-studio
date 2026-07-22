# Connectors

How the agents reach real data systems — safely, and portably across IDEs.

- **`catalog.json`** — the machine-readable list the `connector-advisor` agent reads:
  each source's method (MCP / SDK / JDBC / REST), auth pattern, default access, and
  the regulated-data classes it may hold.
- **`mcp.example.json`** — a ready-to-adapt Model Context Protocol config. MCP is the
  common denominator across **Claude Code, Cursor, and Antigravity**, so a connector
  enabled here works in every IDE. Copy the servers you need into your IDE's MCP
  config (see below).
- **`*.md`** — per-connector how-to guides (auth, scoping, data-class controls).

## Principles (from the Constitution, Article 4)
1. **Least privilege.** Read-only by default; scope to the specific
   tables/buckets/channels the initiative needs.
2. **Secrets never in the repo.** Use `${ENV_VAR}` references resolved from a secret
   manager or a gitignored `.env`. The example file contains zero real credentials.
3. **Control regulated data at the source.** Apply masking / row filters / column
   policies before data reaches a model — and only send it to a model the
   `architecture` artifact approved for that data class.

## Enabling a connector per IDE
- **Claude Code:** merge the server block into `.mcp.json` (project) or `~/.claude.json`.
- **Cursor:** add it under `.cursor/mcp.json`.
- **Antigravity / other MCP clients:** add it to the client's MCP settings.

The `connector-advisor` agent generates the exact block + the secrets checklist for
whatever sources your architecture names.
