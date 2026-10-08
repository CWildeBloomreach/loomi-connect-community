# Peak readiness check

Answers "are we ready for Black Friday, the sale or the launch on date X?" with a go/no-go checklist. Every item gets a RED, AMBER or GREEN status, the evidence, the fix and the type of person who usually owns the fix, with blockers first. It checks:

- **Data:** Discovery pixel health and catalog feed freshness;
- **Merchandising:** ranking rules, media rules (banners) and redirects scheduled for the event window, rules expiring mid-event, A/B tests that would block changes, event landing pages and top category grids;
- **Search:** whether the event's likely queries ("black friday", "sale", "gifts for him") return relevant results or redirect;
- **Marketing:** event sends on the Engagement campaign calendar, clashes, target segments and frequency caps;
- **On-site:** Engagement banners and weblayers for the event.

It never changes, schedules or sends anything.

| | |
|---|---|
| **Products** | Discovery, Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `get_pixel_health_status`, `search_discovery_catalogs`, `search_discovery_catalog_jobs`*, `list_site_search_ranking_rules`, `list_category_ranking_rules`, `list_ranking_rules_global`, `list_site_search_media_rules`*, `list_category_media_rules`*, `list_global_media_rules`, `search_redirects`, `search_discovery_experiments`, `search_dynamic_categories`, `get_discovery_category_performance_table`, `search_discovery_product_grid_insights`, `get_discovery_query_performance`, `list_cloud_organizations`, `list_projects`, `get_campaign_calendar`, `search_scenarios`, `search_scenario_nodes`*, `search_email_campaigns`, `search_segmentations`, `get_frequency_policies`*, `estimate_eql_cost`, `execute_analytics_eql`, `search_banners`, `search_in_app_messages` (* via `search_tools` and `call_tool`) |
| **Tested with** | Claude Code (manual read-only run, October 2026: Discovery rules, redirects, experiments, dynamic categories, category previews, event-query searches, pixel and catalog jobs on a demo account; Engagement campaign calendar, scenario list and banner list on a real production project, metadata only. Not run live: segment sizing and frequency policies in this skill, which reuse the tested methods of `engagement-segment-builder` and `engagement-send-collision-check`; banner schedules for a banner that has one. Both scripts tested on fixtures built from live response shapes) |
| **Maintainer** | Bloomreach |

## Example prompts

- "Are we ready for Black Friday?"
- "Run a go/no-go for the summer sale starting 1 July."
- "We launch the new collection on the 14th. What could go wrong?"
- "Pre-flight check for Cyber Monday: rules, search, emails, banners."

See [examples/black-friday.md](examples/black-friday.md) for an example output.

## Scripts

Python 3 standard library only, no network access.

- `scripts/check_rule_windows.py`: reads saved Discovery rule and redirect listings, plus running experiments, and flags event rules that start late, end early, are disabled or never end, rules that expire mid-event, leftovers from past events and tests that lock rules.
- `scripts/render_checklist.py`: turns the checked items into the final checklist, blockers first, with a verdict and lead times.

## Notes and limitations

- The rule-list `duration` filter returned HTTP 400 in testing, so the skill lists every rule and filters by date itself.
- Dynamic categories never show their products in the list or by-ID views; the skill previews them in the product grid by category ID.
- `search_banners` list mode doesn't return schedules. The skill classifies banners with the `serving_status` filter.
- "No event rules found" depends on the vocabulary. The skill asks for the team's own campaign names before reporting it.
- Works with Discovery only or Engagement only; the missing half is marked NOT CHECKED.
