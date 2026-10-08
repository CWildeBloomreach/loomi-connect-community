# Autosuggest checks: evidence and fixes

Choose the smallest fix that explains the evidence. An exclusion is cheap, but it hides the term from every prefix. A synonym or catalog fix often helps more, because it also improves the results of the query itself.

| Finding | Evidence needed | Recommended fix | Effort / risk |
|---|---|---|---|
| **Suggestion leads to zero results** | the suggested query is under `no_search_results`, or has 0 product views and 100% bounce under `no_revenue`, or the product grid returns `numFound` = 0 | **Exclude** it. If the catalog has the product under another word, also fix the query with a synonym (`discovery-zero-results-triage`) | Low / low |
| **Product + attribute suggestion** ("skirt colors", "dress fabric", "diamond size") | its revenue per visit is well below the bare product query's. In testing, four "skirt ..." suggestions earned $2.39–$2.49 per visit against $17.82 for "skirt", with 51–54% bounce against 26% | **Exclude** the attribute words for that product (e.g. "skirt colors", "skirt styles", "skirt fabric", "skirt trends"), so shoppers land on the product query and use the filters. Make sure colour, style and fabric filters exist (`facet-optimizer`) | Low / low |
| **Steers to a weaker wording** ("tshirt" over "t-shirt") | another wording returns many more relevant products, or converts better | Fix the **synonym** first (`discovery-synonym-review`), so both wordings return the same products. Only exclude the weaker wording if the synonym can't be fixed and the stronger wording is suggested instead | Low / low |
| **Top query missing** ("cocktail dress", "school bags") | the query has high sessions or revenue, and doesn't appear for any prefix, even its first full word | Check it isn't excluded. Then raise it with whoever manages autosuggest. Bloomreach builds suggestions from search and catalog data, and the Loomi Connect tools can't add a suggestion directly | Medium / low |
| **Near-duplicates** ("men jeans" / "men's jeans"; "sweatshirt" / "sweat shirt") | two or more suggestions differ only by spacing, hyphen, apostrophe, plural or "men"/"mens" | **Exclude** the weaker one (lower revenue per visit, or fewer results). Make sure a synonym links the wordings so nobody loses results | Low / low |
| **Misspelt or junk** ("diameter", "camo tee tshirt") | not a product, brand or style word; no or very little traffic; results come only from semantic matching | **Exclude** it | Low / low |
| **Looks wrong, but is a brand** ("scharf", "suitltd", "cantabil") | the term is in the grid's `brand` facet or in product titles | **No action**, or report it as checked. If a brand outranks a common product word ("scharf" above "scarf" for "sc"), mention it and let the merchandiser decide | — |
| **Inappropriate or competitor term** | offensive words; another retailer's name; a brand the catalog doesn't carry (check the `brand` facet and `fq='brand:"<name>"'`) | **Exclude** it. For a competitor search with real traffic, also consider a redirect or banner | Low / low |
| **One lead word hogs the list** ("disney ..." x10 under "di") | 5+ slots start with the same brand or theme, mostly long-tail variants ("disney xl jeans") with little traffic | **Exclude** the long-tail variants, and keep the brand head term ("disney jeans") | Low / medium |
| **Existing exclusion blocks a good term** | an excluded keyword has meaningful sessions and normal conversion | **Remove or narrow** the exclusion | Low / medium |

## Notes

- **Order matters.** Shoppers see the first few suggestions most. Report each problem suggestion's position (for example "dr #3"), and rank position 1–5 problems above 15–20.
- **One suggestion can show under many prefixes.** "skirt colors" appeared under both "sk" (#3) and "co" (#8). An exclusion fixes every place at once.
- **Check before you call something a misspelling.** In testing, "scharf" looked like a misspelling of "scarf", but SCHARF is a brand with 5 products. "berry powder" looked off-catalog on an apparel account, but the catalog has cosmetics.
- **A new query with traffic from nowhere** can be a sign that autosuggest started offering it. In testing, "men jeans" had 678 sessions and 0 in the previous period, and autosuggest offered it for "me". This is consistent with autosuggest creating the traffic, but doesn't prove it.
- **Hybrid search hides weak suggestions.** A junk suggestion can still return results through semantic matching ("diameter" returned 32 diamond items). Judge by the titles and by analytics, not by `numFound`.
- **What the tool can't tell you:** `get_autosuggest_results` returns only the suggestion strings. It doesn't say whether a suggestion is a query, a category or a product suggestion, or why it ranks where it does.
