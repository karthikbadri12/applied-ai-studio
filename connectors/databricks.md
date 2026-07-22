# Databricks connector

**Method:** MCP server (preferred) · **Category:** lakehouse · **Default:** read-only

## Auth
- **Service principal + OAuth (M2M)** for production agents (recommended), or a
  scoped **PAT** for a spike. Token → `${DATABRICKS_TOKEN}` from a secret manager.
- Point at a **SQL Warehouse** (`${DATABRICKS_WAREHOUSE_ID}`), not an all-purpose
  cluster, for governed query access.

## Least-privilege scoping
- Use **Unity Catalog** grants: `SELECT` on the specific catalog.schema.table only.
- No metastore-admin or catalog-owner rights for the agent principal.

## Regulated-data handling
- Unity Catalog **column masks** and **row filters** enforce PII/PHI limits centrally.
- Lineage in Unity Catalog gives you the audit trail Article 7 wants.

## MCP block
See `mcp.example.json` → `mcpServers.databricks`. Secrets checklist:
`DATABRICKS_HOST`, `DATABRICKS_TOKEN`, `DATABRICKS_WAREHOUSE_ID`.
