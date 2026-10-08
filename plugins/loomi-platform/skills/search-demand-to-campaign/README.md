# Search demand to campaign

Connects Discovery and Engagement. It finds what shoppers are searching for (rising searches, and searches with no results or no revenue), checks whether Engagement tracks those searches, counts the people who searched and the people who can be reached, and recommends a campaign. Only if the user explicitly confirms the full payload does it create the campaign as an email or SMS **draft**.

If Engagement doesn't track searches, it still delivers the demand insights and a campaign brief, and explains what tracking to add.

| | |
|---|---|
| **Products** | Discovery, Engagement |
| **Access** | **Writes**: can create one email or SMS campaign **draft** per confirmation. It never activates, updates or deletes campaigns, and never changes Discovery |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `get_discovery_search_performance`, `get_discovery_query_performance`, `search_discovery_product_grid_insights`, `list_cloud_organizations`, `list_projects`, `get_event_schema`, `get_customer_property_schema`, `estimate_eql_cost`, `execute_analytics_eql`, `get_consent_settings`, `search_customer_filters`, `create_email_campaign`, `create_sms_campaign` |
| **Tested with** | Claude Code: the read-only steps were run manually (Discovery on a demo account; Engagement schema checks and aggregate EQL on a live sandbox, plus a schema check and one aggregate query on production). **Creating drafts is untested**: the create tools were not called |
| **Maintainer** | Bloomreach |

## Example prompts

- "Turn our failed searches into a campaign."
- "How many people searched for capris, and can we email them when they're back?"
- "What's trending in search that we should run a campaign on?"

See [examples/capris.md](examples/capris.md). Its Discovery figures are from a demo account; the Engagement side is illustrative.

## How it decides whether a campaign is possible

Engagement projects track search in different ways, so the skill classifies the project:

| Tier | Search signal | Result |
|---|---|---|
| A | A dedicated search event with a term property | Audience by term |
| B | Search results pages tracked as page visits, with the term in the URL | Audience by term (approximate) |
| C | Search text on another event (a widget or chat) | Audience by term, if the property is still filled |
| D | None | A brief only, plus the tracking to add |

It always checks that the signal is **still arriving**, because a property marked "used" in the schema may have had no values for months. It always counts **reachable** people separately from searchers: in testing, search-page visitors were all anonymous.

## Notes and limitations

- **Writes are untested.** The payload shapes in [references/campaign-drafts.md](references/campaign-drafts.md) come from the tools' descriptions. The create tools always make drafts, and a person must activate them in the UI.
- The campaign audience must come from a **saved customer filter** created in the UI, because the API can't reference a saved filter by ID and the filter JSON format isn't documented. Event-triggered campaigns aren't covered; build those as scenarios in the UI.
- EQL is limited to about one query every 3 seconds. Audience queries that scan every customer can be rated "high" cost.
- The Discovery account and the Engagement project must be the same business. The skill asks if that's unclear.
