# Recommendation model audit

Audits the recommendation engines (models) in a Bloomreach Engagement project. It lists each engine with its type, catalog, the behaviour it learns from and its filters, checks whether each catalog is fresh and healthy, and searches active scenarios, email campaigns and web layers for where each engine is used. It flags unused engines, engines on stale or failing catalogs, near-duplicates, engines with no or very restrictive filters, and important placements (abandoned cart, post-purchase, home and product pages) that use no recommendations. It returns a prioritised cleanup and improvement list, and it never changes anything.

| | |
|---|---|
| **Products** | Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_cloud_organizations`, `list_projects`, `search_recommendations`, `search_catalogs`, `get_catalog_usages`, `list_catalog_jobs`, `search_scenarios`, `search_email_campaigns`, `search_banners`, optionally `search_scenario_nodes` (via `call_tool`), `search_catalog_items`, `get_customer_recommendations` |
| **Tested with** | Claude Code: `search_recommendations` list and detail, `search_catalogs`, `get_catalog_usages` and `list_catalog_jobs` read live from sandbox and production projects (one production project had two engines; the sandboxes had none, and one sandbox returned HTTP 403 for `search_recommendations`). The only catalogs with engines were v1, so v2 job-based freshness checks are untested (one v2 catalog returned no jobs). Placement searches (scenarios, email campaigns, web layers), `search_catalog_items` and `get_customer_recommendations` were not run. The script was tested on synthetic responses. Not tested in an OpenAI client. |
| **Maintainer** | Bloomreach |

## Example prompts

- "Audit our recommendation engines. Which ones are actually used?"
- "Do we have duplicate recommendation models?"
- "Why are the recommendations in our emails empty? Check the engines and their catalogs."
- "Which of our key emails and web layers don't use recommendations yet?"

See [examples/illustrative-audit.md](examples/illustrative-audit.md) for an example output. Its names and numbers are illustrative.

## How it works

1. Lists the engines and fetches each definition: type, catalog, event, look-back, catalog and event filters, exclusions, pinning.
2. Checks each catalog: whether it still exists, what else uses it (`get_catalog_usages`), and, for v2 catalogs, how recent and successful its last update jobs were (`list_catalog_jobs`).
3. Finds where each engine is used by searching active scenario designs, active email campaign designs and serving web layers for the engine's ID. There's no direct "where used" tool for engines.
4. Applies the checks in [references/audit-checks.md](references/audit-checks.md) and suggests an engine type for high-value placements that have none. [scripts/audit_engines.py](scripts/audit_engines.py) does this from saved responses (standard library only, no network, never prints placement content).

Catalog problems are handed to `data-feed-health` (in the `loomi-platform` plugin).

## Notes and limitations

- Usage is found by searching placement content for engine IDs. Engines called from the website or app through the API won't be found, so "unused" means "not found in the placements searched".
- Finding engine IDs needs full designs (`include_design=True` / `include_node_designs=True`), which are large. The skill searches active placements only unless asked.
- `list_catalog_jobs` only works for v2 catalogs. v1 catalogs have no job history or edited date, so their freshness is reported as unknown and handed to `data-feed-health`.
- No fallback setting was found in engine definitions; fallbacks are usually set where the engine is called.
- Only the `recently_viewed` engine type was observed in testing. Engine and catalog records include editor names; the skill never repeats them.
- `search_recommendations` can return HTTP 403 depending on permissions. The skill stops and says so rather than reporting "no engines".
