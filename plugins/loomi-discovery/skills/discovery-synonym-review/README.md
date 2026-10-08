# Discovery synonym review

Audits an account's search synonyms, both user-created and Bloomreach-generated. It flags risky or bad expansions, no-op and leftover test synonyms, and one-way synonyms that miss the catalog's wording. It then checks which synonyms actually fire on the highest-traffic and worst-performing queries, using the live product grid. It returns a prioritised list of synonyms to fix, add or clean up. It never changes anything.

| | |
|---|---|
| **Products** | Discovery |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `list_synonyms_user`, `list_synonyms_br_generated`, `get_discovery_query_performance`, `search_discovery_product_grid_insights` |
| **Tested with** | Claude Code (manual, read-only run of the method against a demo Discovery account with no sites, at account level). Not yet tested in an OpenAI client |
| **Maintainer** | Bloomreach |

## Example prompts

- "Audit our search synonyms."
- "Are any synonyms hurting our search results?"
- "Why doesn't 'tshirt' find all our T-shirts?"

See [examples/example-apparel.md](examples/example-apparel.md) for a full example output.

## What it found in testing

- A one-way Bloomreach-generated synonym for "tshirt" skipped "t-shirt": 26 results instead of 65, on a query with about 20,000 sessions a month.
- A lemma chain sent "straw hat" to "coffee stirrers" via "straws".
- Every dead-end query had a user synonym mapping it to itself, which does nothing.
- A flagged Bloomreach-generated synonym was on the list but didn't fire, so the skill checks the product grid before calling a synonym a risk.

## Notes and limitations

- Accounts can have tens of thousands of Bloomreach-generated synonyms. The skill reviews only the newest ones from the list, and finds the rest through the queries that matter.
- Product grid responses are very large. The skill asks for few fields and rows, turns off facets, and includes `scripts/grid_summary.py` (standard library only) to summarise a saved response.
- `simple_debug=false` returned HTTP 500 errors in testing, so the skill doesn't use it.
- The meaning of `groupSynonym` (two-way group) was inferred from the data, and not confirmed against the synonyms guide.
- Revenue figures are upper bounds, not forecasts.
