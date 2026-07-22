# BigQuery connector

**Method:** MCP server (preferred) · **Category:** warehouse · **Default:** read-only

## Auth
- **Service account** with a JSON key referenced via
  `${GOOGLE_APPLICATION_CREDENTIALS}` (path to a secret-managed file), or Workload
  Identity Federation on GCP compute (keyless — preferred in production).

## Least-privilege scoping
- Grant `roles/bigquery.dataViewer` on **only the required datasets**, plus
  `roles/bigquery.jobUser` to run queries. No project-level `dataEditor`.
- Pin `BIGQUERY_ALLOWED_DATASETS` so the agent queries only what it should.

## Regulated-data handling
- Use **authorized views** / **column-level security** (policy tags via Data
  Catalog) and **row-level security** so PII never leaves the source unmasked.
- Keep queries in-region to honor residency (`architecture` controls).

## MCP block
See `mcp.example.json` → `mcpServers.bigquery`. Secrets checklist:
`GOOGLE_APPLICATION_CREDENTIALS`, `BIGQUERY_PROJECT`, `BIGQUERY_ALLOWED_DATASETS`.
