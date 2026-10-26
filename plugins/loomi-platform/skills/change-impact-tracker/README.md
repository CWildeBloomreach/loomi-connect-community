# Change impact tracker

Answers "did my change work?" for one merchandising or marketing change. It finds the change (or lists recent ones to choose from), checks that it actually fires, measures what it affected in equal-length windows before and after, and compares that with a control the change didn't touch, so a busy or quiet week isn't mistaken for the change's effect.

- **Supported changes:** Discovery synonyms, ranking rules (search, category, global), redirects, facet rules, media banners and dynamic categories; Engagement campaign or scenario launches.
- **Method:** difference-in-differences against one or two controls (the search or category card minus the treated rows, and comparable queries or categories), a two-proportion test on conversion, 95% ranges, a placebo on two pre-change windows, and minimum-data warnings.
- **Output:** a verdict (**worked**, **no clear effect**, **made it worse** or **too early to tell**), the effect with a range, revenue per month, caveats (seasonality, other changes, promotions) and next steps (keep, roll back, re-run, or A/B test with `discovery-experiment-setup`).

It never changes anything.

| | |
|---|---|
| **Products** | Discovery, Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `list_site_search_ranking_rules`, `list_category_ranking_rules`, `list_ranking_rules_global`, `list_synonyms_user`, `list_synonyms_br_generated`, `search_redirects`, `list_site_search_facets`, `list_category_facets`, `list_site_search_media_rules`, `list_category_media_rules`, `search_dynamic_categories`, `search_discovery_experiments`, `get_ranking_rule`, `get_facet_rule`, `get_discovery_media_rule`, `search_discovery_product_grid_insights`, `get_discovery_query_performance`, `get_discovery_category_performance_table`, `get_discovery_product_performance_table`, `get_discovery_search_performance`, `get_discovery_category_performance`, `get_discovery_overall_performance`, `get_discovery_trend`; for Engagement: `list_cloud_organizations`, `list_projects`, `get_campaign_calendar`, `search_scenarios`, `search_email_campaigns`, `estimate_eql_cost`, `execute_analytics_eql` |
| **Tested with** | Claude Code: manual read-only run on a demo Discovery account with no sites, measuring a scheduled category ranking rule end to end (finding it, confirming it fires in the product grid, custom before/after windows on the category table and card, a placebo, the script). Script tested on that run and on synthetic large-effect and zero-traffic inputs. **Not yet tested:** a site-level account; synonym, redirect, facet, banner and dynamic-category measurements; the Engagement campaign path (no live EQL was run); an OpenAI client |
| **Maintainer** | Bloomreach |

## Example prompts

- "Did the synonym I added for 'tshirt' last week work?"
- "We boosted linen on 'long dresses'. Has it helped?"
- "Has the Halloween rule on kids tops made any difference?"
- "What did our recent merchandising changes do? Should we keep them?"
- "Did launching the welcome scenario lift purchases?"

See [examples/halloween-category-rule.md](examples/halloween-category-rule.md) for a full example output.

## Scripts

- `scripts/did_effect.py`: reads a small JSON file with visits, orders and revenue for the treated thing and each control, before and after, and prints the difference-in-differences effect for visits, orders, revenue, conversion, revenue per visit and AOV with 95% ranges; a two-proportion test on conversion; incremental revenue for the window and per 30 days with a range; the smallest detectable effect; a placebo check (`--placebo`); warnings; and a verdict. `--template` prints an example input (`--template --out <file>` saves it), `--json` prints JSON. Standard library only; no network access.

## Notes and limitations

- This is an observational estimate, not an A/B test. The ranges cover sampling noise only, not seasonality specific to the products, promotions, stock-outs or other changes in the window. The skill checks for those and says when an A/B test is the only way to get a clean answer.
- Small queries and categories rarely give a clear answer: with about 150 orders a window, revenue ranges are about ±30%.
- Scheduled rules can start without their `lastModifiedAt` changing, so the skill reads `startedAt` too.
- Audience-targeted rules affect only that audience; account-level numbers dilute their effect.
- Rules on wordings nobody searches can't be measured; the skill reports that rather than "no effect".
- Rule, synonym and experiment lists include editors' email addresses. The skill never repeats them.
- Related skills: [revenue-anomaly-explainer](../revenue-anomaly-explainer/) (why did revenue change, from the other direction), `discovery-rule-audit`, `discovery-synonym-review`, `discovery-experiment-readout`, `discovery-experiment-setup`, `engagement-campaign-digest`.
