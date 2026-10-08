# Trending searches

Shows which site searches are rising, new and falling, adjusted for overall traffic, and flags trending queries whose results are letting shoppers down.

| | |
|---|---|
| **Products** | Discovery |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `get_discovery_search_performance`, `get_discovery_query_performance`, optionally `get_discovery_trend` |
| **Tested with** | Claude Code (manual run of the method and script on a demo account) |
| **Maintainer** | Bloomreach |

## Example prompts

- "What's trending in search this week?"
- "Which searches are rising or falling compared with last month?"
- "Any new search terms we should know about?"

## How trends are measured

Loomi Connect has no dedicated "trending" report. This skill builds one from the query performance report, which gives each query's figures for both the current and the previous period. For each query:

- it compares the query with the overall change in search traffic, so a sitewide spike doesn't make everything look like a trend;
- it ranks queries by extra sessions weighted by volume, so large queries aren't drowned out by tiny ones with big percentage swings.

[scripts/rank_trends.py](scripts/rank_trends.py) does the ranking. It uses only the Python standard library and makes no network calls. Where Python isn't available, the skill explains how to do the same calculation by hand.

## Example output (demo account, 7 days)

> **Overall search traffic:** −2.9% (a flat week, so the rises below are real)
>
> | Query | Sessions (prev → now) | vs baseline | Conversion | Bounce |
> |---|---|---|---|---|
> | shorts | 1,679 → 1,791 | +9.8% | 20.6% | 19.1% |
> | camo pants | 1,181 → 1,267 | +10.4% | 22.5% | 26.1% |
> | casual belt | 217 → 256 | +21.4% | 11.7% | 2.3% |
> | mens belt | 1,345 → 1,408 | +7.8% | 10.0% | 62.6% |
>
> **Themes:** belts are rising across three queries, while "womens shorts" is falling (−10% vs baseline) even as "shorts" rises.
>
> **Opportunities:** "mens belt" is rising, but its bounce rate is 63% compared with about 25% for top queries. Worth diagnosing.

## Limitations

- The skill only looks at the top queries by volume (up to about 200), so a brand-new long-tail term with little traffic may not appear.
- There are no statistical significance tests. On small sites, a week-on-week change can be noise.
