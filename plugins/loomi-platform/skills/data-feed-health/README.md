# Data and feed health check

Checks the data every other Bloomreach report depends on, and returns one red, amber and green summary with evidence and next steps:

- **Discovery tracking pixel:** error rates, missing or collapsing event types, and what the errors mean;
- **Discovery catalog:** product feed and index job freshness, failures, warnings and product-count drops;
- **Data Hub:** failed or stale pipeline jobs, and which catalogs Data Hub manages;
- **Engagement (optional):** catalog job history and whether standard events and the product catalog are mapped.

It never re-runs jobs, uploads data, changes settings or reads individual customer records.

| | |
|---|---|
| **Products** | Discovery, Data Hub, Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `get_pixel_health_status`, `get_pixel_event_stream`, `get_pixel_event_details`, `search_discovery_catalogs`, `search_discovery_catalog_jobs` (via `search_tools` and `call_tool`), `list_cloud_organizations`, `list_workspaces`, `list_projects`, `search_datahub_jobs`, `search_datahub_catalogs`, `search_catalogs`, `list_catalog_jobs`, `get_mapping` |
| **Tested with** | Claude Code (manual read-only run: Discovery pixel and catalog checks on a demo account; Engagement catalog and mapping checks on a sandbox project. Not yet tested: a workspace with Data Hub enabled, and v2 Engagement catalogs with job history) |
| **Maintainer** | Bloomreach |

## Example prompts

- "Is our tracking working?"
- "Are our product feeds up to date?"
- "Did any catalog or Data Hub jobs fail this week?"
- "Run a data health check before I send the monthly report."

See [examples/example-health-check.md](examples/example-health-check.md) for an example output.

## Scripts

- `scripts/discovery_jobs_summary.py`: summarises saved `search_discovery_catalog_jobs` output by job kind (latest success, hours since, failures, warnings, product-count changes) and suggests a RAG status. Standard library only; no network access.

## Notes and limitations

- `search_discovery_catalog_jobs` isn't always listed directly; the skill finds it with `search_tools` and runs it with `call_tool`. Its `status` filter was ignored in testing, so the skill filters jobs itself.
- `last_index_refresh_at` in `search_discovery_catalogs` tracks full refresh indexes only; the skill uses the job list for freshness.
- v1 Engagement catalogs have no job history in Loomi Connect, so their freshness is reported as "not visible".
- Pixel samples include masked user IDs and IP addresses. The skill uses them only to identify the faulty parameter and never repeats them.
- Thresholds are defaults in [references/rag-thresholds.md](references/rag-thresholds.md); adjust them to your own service levels.
