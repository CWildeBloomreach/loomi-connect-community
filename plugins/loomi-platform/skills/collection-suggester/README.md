# Collection suggester

Suggests new product collections: groups of products that shoppers want but can't easily browse to. It combines rising and underserved search demand (grouped by the attributes the matching products share, not by wording), rising products, existing dynamic categories and seasonal moments. For each suggestion it gives a rule-based definition, a live preview from the product grid, the evidence, where to use it and the assortment gaps it reveals. It also flags broken, thin, manual and duplicate dynamic categories. It never creates or changes anything.

| | |
|---|---|
| **Products** | Discovery (Engagement optional, for co-purchase affinity) |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `get_discovery_search_performance`, `get_discovery_query_performance`, `search_discovery_product_grid_insights`, `get_discovery_product_performance_table`, `get_discovery_products_overview`, `list_categories`, `search_dynamic_categories`; optional: `list_cloud_organizations`, `list_projects`, `get_event_schema`, `estimate_eql_cost`, `execute_analytics_eql` |
| **Tested with** | Claude Code, by a manual run of the method on a demo Discovery account (account level, no sites) on 8 October 2026. The Engagement schema and cost estimate were checked on a test project; the co-purchase EQL itself was not executed. Not yet tested in an OpenAI client. |
| **Maintainer** | Bloomreach |

## Example prompts

- "What new collections should we build from our search data?"
- "Suggest some dynamic categories for the holiday season, for the UK."
- "Shoppers keep searching for camo. Should that be a collection?"
- "Are any of our dynamic categories broken or duplicated?"

See [examples/example-apparel.md](examples/example-apparel.md) for a full run.

## Scripts

Standard library only; no network access. Both work on responses the client has saved to files.

- `scripts/preview_summary.py`: summarises saved product grid responses. It gives the product count, a thin or broad flag, the top titles, the repeated-title rate, brand spread, dominant attribute values, and overlap with existing dynamic categories.
- `scripts/group_themes.py`: groups queries into themes by shared dominant attribute values, and adds up sessions, baseline-adjusted growth, revenue and underserved members.

## Can it create the collections?

Not in v1, and not through Loomi Connect today. In October 2026, `search_tools` found **no tool that creates or edits Discovery dynamic categories**. It did find `create_item_collection`, but that creates a **Data Hub item collection**, a product-data container that feeds catalogs, not a merchandising collection. The skill outputs each definition in readable form and in the dashboard's condition format, with set-up steps for the Discovery dashboard.

## Notes and limitations

- **Previews and AND:** the product grid's `fq` accepts OR within one string, but AND inside one string returns 0. The skill sends several `fq` values through `extra_params` instead (verified). Price-range `fq` syntax was not verified.
- **Rules need attribute data.** Themes that live only in titles (prints, fabrics, cuts) can't be rule-based. The skill says so, offers a manual list, and names the feed attribute to add.
- **Facet name and condition name can differ** (facet `colors` is condition attribute `color`; `category` is `category_id`). These were checked against one account's existing dynamic categories; confirm them on yours.
- **Co-purchase** is a customer-level category affinity from aggregate EQL, not same-basket pairs, and needs a purchase line-item event with categories. On large projects the query rates `very_high`, so the skill asks first.
- **Seasonal ideas** default to US, UK and EU, accept any market, and fall back to global moments (with a note) for markets not listed. The `campaign-planner` skill has the full calendar by market.
- Growth is measured against overall search growth. On sites with strong overall growth, raw percentages are misleading.
