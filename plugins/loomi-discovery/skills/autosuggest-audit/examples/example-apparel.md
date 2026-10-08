# Example: autosuggest audit (demo apparel account)

The account name has been changed to a placeholder. This example comes from a real, read-only run against a demo account. Its traffic is synthetic, so the growth rates are unusually uniform, but the autosuggest lists, product counts and rules are real.

**Prompt:** "Audit our autosuggest. Is it costing us sales?"

## Autosuggest audit: example_apparel (account level, last 30 days)

**Headline:** Autosuggest pushes shoppers from "skirt" and "dress" towards question-like suggestions ("skirt colors", "dress style") that earn a fraction as much per visit. Excluding eight terms is worth up to about $156k a month. Separately, two queries worth $728k a month are never suggested at all.

**How I sampled:** 21 prefixes, covering the top 20 queries by sessions and the top 5 by revenue. Two-letter prefixes for every top query ("me", "sk", "dr", "di", "je", "ba", "pa", "su", "be", "co", "ca", "ru", "sc", "sw", "ts"), the single letter "t", the hyphenated "t-", and deeper prefixes where a top query was missing ("coc", "cocktail", "sch", "school"). 36 calls in total, one at a time.

**Exclusion rules today:** none. Nobody has curated autosuggest on this account.

### Fix first

| # | Prefix → suggestion (position) | Problem | Evidence | Sessions | At stake (upper bound) | Recommendation |
|---|---|---|---|---|---|---|
| 1 | sk → "skirt colors" (#3), "skirt styles" (#4), "skirt fabric" (#5), "skirt trends" (#6); also "co" #8 and "t" #19 | Product + attribute suggestions pull shoppers off "skirt" | Conversion 5.4–6.1% and bounce 51–54%, against 21.5% and 26% for "skirt". Revenue per visit $2.39–$2.49 against $17.82. All four return ordinary skirt results (351 for "skirt colors") | 5,388 | ~$83k | Exclude: `skirt colors`, `skirt styles`, `skirt fabric`, `skirt trends`. Keep "skirt length" for now ($8.69 per visit, 5% bounce) |
| 2 | dr → "dress color" (#3), "dress fabric" (#4), "dress length" (#5), "dress style" (#6) | Same pattern on "dress", the second-highest revenue query | Conversion 10.2–12.7% against 21.7%; revenue per visit $14.96–$20.35 against $32.77. Bounce is low (2–4%), so shoppers browse but buy less | 4,844 | ~$73k | Exclude: `dress color`, `dress fabric`, `dress length`, `dress style`. Then check that colour, fabric and length filters exist on "dress" (see `facet-optimizer`) |
| 3 | t → "tshirt" (#1), ts → "tshirt" (#1); "t-" → nothing | Autosuggest offers only the weaker wording | "tshirt" finds 26 products and converts at 11.4%; "t-shirt" finds 65. "t-" returns no suggestions at all | 20,853 | see `discovery-synonym-review` | Don't exclude "tshirt" (it's the top T-shirt query). Fix the one-way synonym so "tshirt" also finds "t-shirt" products. That fixes the destination of the suggestion |

None of the dead-end queries (13 under `no_search_results`, 31 under `no_revenue`, about 7,600 current sessions between them) were offered by autosuggest for the prefixes tested. "swim trunks", the largest, doesn't appear under "sw", and "capris" doesn't appear under "ca".

### Top queries autosuggest never offers

| Query | Sessions | Revenue | Conversion | Prefixes tested |
|---|---|---|---|---|
| cocktail dress | 14,376 | $467,225 | 22.0% | "co", "coc", "cocktail" (the last two return nothing) |
| school bags | 9,580 | $260,660 | 21.7% | "sc", "sch", "school" ("sch" offers only "scharf") |

Both queries convert at the baseline, so their results are fine. Shoppers have to type the whole query to reach them. Under "co", 13 of the 20 slots go to "cotton ..." suggestions. No exclusion rule explains the gap (there are none). Raise it with whoever manages autosuggest; the Loomi Connect tools can't add a suggestion.

### Clean-up

- **Slot hogs:** "disney ..." takes 10 of 20 slots under "di", mostly long-tail ("disney xl jeans", "disney gray mid-rise jeans"). "sweet dreams ..." takes 9 of 20 under "sw". "scotch & soda ..." takes 7 of 17 under "sc". Exclude the long-tail variants, and keep one head term per brand ("disney jeans", "sweet dreams shorts", "scotch & soda").
- **Near-duplicates:** "men jeans" (suggested, 678 sessions, 13.7% conversion; it had no sessions in the previous period) and "men's jeans" (not suggested, 848 sessions, 9.1%). The suggested wording is the stronger one, so no action. Under "me", 13 suggestions say "mens" and 6 say "men": pick one form. "sweatshirt" (#1) and "sweat shirt" (#19) under "sw": exclude `sweat shirt`. "camo tshirt" and "camo tee tshirt" under "ts": exclude `camo tee tshirt`.
- **Junk:** "diameter" (#6 under "di"). It has no query traffic, and its 32 results match only through semantic search. Exclude `diameter`. "diamond shape", "diamond cut", "diamond size" and "jersey size / brand / material / color" follow the product + attribute pattern, but had no traffic of their own in the period. Low priority.

**Checked and fine:** "scharf" (#1 under "sc") looks like a misspelling of "scarf", but SCHARF is a brand with 5 products. "suitltd", "cantabil", "canary london" and "scorpius" are brands in the catalog's brand facet. "berry powder" and "berry blush" match cosmetics the catalog carries. No competitor retailers or offensive terms were found. Not checked: "baggit" and "jewel junction".

**Fixes outside autosuggest:** the "tshirt" synonym (`discovery-synonym-review`); colour, fabric and length filters on "skirt" and "dress" (`facet-optimizer`).

**Next steps:**
1. Add one exclusion rule with the eight skirt and dress attribute terms, then re-check "sk" and "dr".
2. Fix the tshirt ↔ t-shirt synonym.
3. Ask why "cocktail dress" and "school bags" aren't suggested.
