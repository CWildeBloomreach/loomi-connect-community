# Discovery redirect audit

Audits the search redirects in a Bloomreach Discovery account or site and returns a prioritised fix list. It flags destination URLs that look malformed, non-production or out of date; duplicate and overlapping redirects; phrase-match redirects that hijack product searches; conflicts with synonyms and with ranking or banner rules; and redirects that may be hiding good results. It also finds popular navigational searches, such as "returns", "store locator" or "gift cards", that have no redirect. It never changes anything.

| | |
|---|---|
| **Products** | Discovery |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `search_redirects`, `search_discovery_product_grid_insights`, `get_discovery_query_performance`, `get_discovery_search_performance`, `list_synonyms_user`, `list_synonyms_br_generated`, `list_site_search_ranking_rules`, `list_site_search_media_rules` |
| **Tested with** | Claude Code: live read-only calls to `list_discovery_accounts`, `search_redirects` (list and `rule_id`), `get_discovery_query_performance` (with `search`), `list_synonyms_user` and `search_discovery_product_grid_insights` against a demo account with three redirects. The full method was not run end to end, and `get_discovery_search_performance`, `list_synonyms_br_generated` and the rule lists were not called. `scripts/redirect_checks.py` was tested on made-up responses. Not yet tested in an OpenAI client |
| **Maintainer** | Bloomreach |

## Example prompts

- "Audit our search redirects."
- "Why does searching 'sale dresses' take people to the sale page?"
- "Which searches should we be redirecting?"

See [examples/example-home-goods.md](examples/example-home-goods.md) for an illustrative output.

## Notes and limitations

- Destination URLs aren't loaded: Loomi Connect can't fetch web pages. The skill checks their shape (scheme, host, placeholders, dated paths) and says so. If the client has a web-fetch tool, it can check them with the user's agreement.
- Redirected searches never appear in query performance, so there's no click-through or exit rate for a redirect. The skill uses the product grid instead: its `keywordRedirect` field shows whether a search redirects, and its results show what shoppers would see without the redirect.
- `scripts/redirect_checks.py` (Python standard library, no network) reads saved responses and applies the checks in [references/redirect-checks.md](references/redirect-checks.md).
- Suggested destinations for new redirects are guesses; the user must supply the real URLs.
- Hands off to discovery-synonym-review for synonym problems and discovery-zero-results-triage for dead-end searches that aren't navigational.
