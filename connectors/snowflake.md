# Snowflake connector

**Method:** MCP server (preferred) · **Category:** warehouse · **Default:** read-only

## Auth
- **Key-pair** (recommended for service use): generate an RSA key pair, register the
  public key on a dedicated service user. Private key → secret manager, referenced as
  `${SNOWFLAKE_PRIVATE_KEY}`. Never a password in the repo.
- **OAuth** for interactive/user-scoped access.

## Least-privilege scoping
- Create a dedicated role, e.g. `APPLIED_AI_READONLY`, with `USAGE` on one warehouse
  (size XS) and `SELECT` on only the required schema(s). No `ACCOUNTADMIN`.
- Pin `SNOWFLAKE_ALLOWED_SCHEMAS` so the agent can't wander the account.

## Regulated-data handling (do this at the source)
- Apply **dynamic data masking** policies on PII/PCI columns and **row-access
  policies** so masked/filtered data is what the agent ever sees.
- Only send results to a model the `architecture` artifact approved for that class.

## MCP block
See `mcp.example.json` → `mcpServers.snowflake`. Secrets checklist:
`SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PRIVATE_KEY`, plus the pinned
`SNOWFLAKE_ROLE` / `SNOWFLAKE_WAREHOUSE` / `SNOWFLAKE_ALLOWED_SCHEMAS`.
