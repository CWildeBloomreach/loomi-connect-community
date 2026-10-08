# Segment opportunity finder

Finds valuable audiences a Bloomreach Engagement project isn't targeting yet. Where `engagement-segment-builder` needs you to know the audience you want, this skill proposes the audiences. It tests eight opportunity patterns against the project's real events and properties with aggregate EQL counts, measures how many people in each can actually be reached, estimates the value with stated assumptions, checks whether an existing segment, scenario or campaign already covers each one, and ranks them by value × reachability with a suggested action and channel. It can join in rising searches from Bloomreach Discovery. It never changes anything.

| | |
|---|---|
| **Products** | Engagement, optionally Discovery |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_cloud_organizations`, `list_projects`, `get_event_schema`, `get_customer_property_schema`, `get_consent_settings` (via `call_tool`), `estimate_eql_cost`, `execute_analytics_eql`, `search_predictions`, `search_segmentations`, `search_aggregates`, `search_scenarios`, `search_scenario_nodes` (via `call_tool`), `search_email_campaigns`, `search_sms_campaigns`; optionally `list_discovery_accounts`, `list_discovery_sites`, `get_discovery_search_performance`, `get_discovery_query_performance` |
| **Tested with** | Claude Code: every pattern's EQL run live and read-only, as aggregate counts, against a sandbox project (with `execution_time` moved to a period with purchases) and, for P2, P6, reachability and consent, a production project. Schema, consent settings, segmentation and scenario metadata read from both. Discovery query performance read from a demo account. The ranking script was run on illustrative inputs. **Not run end to end as a single session**, the Discovery-to-Engagement join was only done by hand across unrelated accounts, `search_scenario_nodes` and `search_email_campaigns` weren't exercised for this skill, and it hasn't been tested in an OpenAI client. |
| **Maintainer** | Bloomreach |

## Example prompts

- "Which audiences are we missing?"
- "Where's the untapped revenue in our customer base?"
- "Give me three segments we should be targeting that we aren't."
- "Who should our CRM team go after next?"

See [examples/illustrative-opportunities.md](examples/illustrative-opportunities.md) for an example output. Its names and numbers are illustrative.

## The patterns

| ID | Opportunity |
|---|---|
| P1 | Browsed a category but never bought it |
| P2 | One-time buyers in their likely repeat window |
| P3 | High-value customers whose buying is slowing |
| P4 | Customers who mostly buy on discount (if a discount property exists) |
| P5 | Category affinity matched to rising Discovery searches |
| P6 | Cart abandoners nobody contacted |
| P7 | New customers without a second purchase |
| P8 | Large groups without consent (if consent is tracked) |

Every query, with its tested status (Ran or Parsed), is in [references/opportunity-patterns.md](references/opportunity-patterns.md). Value assumptions and ranking are in [references/value-and-ranking.md](references/value-and-ranking.md), and actions and hand-offs in [references/actions-and-handoffs.md](references/actions-and-handoffs.md). [scripts/rank_opportunities.py](scripts/rank_opportunities.py) builds the ranked table (standard library only, no network).

## Notes and limitations

- On large projects, every customer count is rated `high` by `estimate_eql_cost`. A full scan is about 15–25 queries and, at EQL's limit of about one query every 3 seconds per Engagement instance, takes 3–5 minutes. The skill asks once before running them and never runs `very_high` queries.
- Values are estimates built on default response rates, not forecasts. Discount (P4) is margin protected and consent (P8) is long-term value; they're labelled so nobody adds them to revenue.
- In testing, four things made patterns silently empty or wrong: category values in different formats on view and purchase events, purchases not linked to browsing identities, an affinity property that existed but was empty, and consent not recorded in Engagement at all. The skill checks for each.
- The `campaign` event can be dominated by A/B split assignments, so "not contacted" filters on message types.
- Discovery has no customer IDs: the trending-search join is by category, not by person.
- It doesn't size lapsed customers beyond 365 days; that's `winback-opportunity`.
