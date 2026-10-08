# Autosuggest audit

Audits Bloomreach Discovery autosuggest, the suggestions shoppers see while they type. It samples prefixes of the account's top-traffic and top-revenue queries, then checks what autosuggest offers against query analytics and the live product grid. It flags top queries that are never suggested, suggestions that lead to weak or zero results, "product + attribute" suggestions ("skirt colors") that pull shoppers away from the product query, near-duplicates, junk or competitor terms, one brand hogging the list, and suggestions that steer people to a weaker wording. It also reviews the existing exclusion rules. It recommends exclusions and fixes, and never changes anything.

| | |
|---|---|
| **Products** | Discovery |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `get_discovery_query_performance`, `get_autosuggest_results`, `search_autosuggest_exclusion_rules`, `search_discovery_product_grid_insights` |
| **Tested with** | Claude Code (manual, read-only run of the method against a demo Discovery account with no sites, at account level: 21 autosuggest prefixes, about 36 calls in all). Not yet tested in an OpenAI client, and not yet run end-to-end from the skill file in a fresh session |
| **Maintainer** | Bloomreach |

## Example prompts

- "Audit our autosuggest."
- "Are our search suggestions costing us sales?"
- "Why doesn't 'cocktail dress' come up when people start typing?"
- "Which autosuggest terms should we exclude?"

See [examples/example-apparel.md](examples/example-apparel.md) for a full example output.

## What it found in testing

- Two queries worth $728k a month together ("cocktail dress" and "school bags") never appeared in autosuggest, even after typing the whole first word.
- Four "skirt ..." suggestions ("skirt colors", "skirt styles", "skirt fabric", "skirt trends") converted at about 6% against 21% for "skirt", worth up to about $83k a month.
- One brand filled 10 of the 20 slots for "di", mostly long-tail variants such as "disney xl jeans".
- Several suggestions that looked misspelt ("scharf", "suitltd") turned out to be brands the catalog carries, so the skill checks the brand facet before recommending an exclusion.

## Notes and limitations

- `get_autosuggest_results` returns only the suggestion strings, without type, ranking reason or popularity. The skill can't tell a query suggestion from a category or product suggestion.
- Autosuggest can't be listed in full, so the audit samples prefixes. The skill says which prefixes it tested.
- The Loomi Connect tools can exclude suggestions but not add them, so missing top queries are reported for someone to raise, not fixed directly.
- `scripts/autosuggest_check.py` (standard library only, no network) cross-checks collected suggestions against saved query-performance responses. Its flags are leads, not verdicts.
- Revenue figures are upper bounds, not forecasts.
- Related skills: `discovery-synonym-review` (wording fixes), `discovery-zero-results-triage` (dead-end queries), `facet-optimizer` (the filters shoppers need once they land on the product query).
