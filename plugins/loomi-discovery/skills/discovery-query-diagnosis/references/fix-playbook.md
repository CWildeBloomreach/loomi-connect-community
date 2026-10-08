# Fix playbook

This table matches the evidence from a diagnosis to the most likely fix. Choose the smallest fix that explains the evidence.

| Evidence | Likely cause | Fix | Effort / risk |
|---|---|---|---|
| Another wording (hyphen, space, plural) returns many more relevant products | Missing or one-way synonym | Add a **two-way synonym** linking the wordings, or extend the existing one-way synonym to include the wording the catalog uses | Low / low |
| A misspelling returns few results and `did_you_mean` is empty | Spelling correction not catching it | Add a **one-way synonym** from the misspelling to the correct term | Low / low |
| Shoppers use different words from the catalog ("trainers" vs "sneakers", "jumper" vs "sweater") | Vocabulary gap | Add a **two-way synonym**. If only one wording should expand, use a one-way synonym | Low / low |
| Almost no results in every wording and both search modes | The catalog doesn't carry the product | **Redirect** to the nearest category or a content page, or show a **media banner** explaining what's available. Raise it as an assortment gap | Low / low |
| Results exist but the top ones are off-topic, such as accessories ranking above the main product | Ranking or text relevance | Add a **ranking rule** for this query that boosts the main product type or category, or buries off-topic types | Medium / medium |
| A ranking rule applies, and turning it off in the grid improves the top results | An outdated or wrong ranking rule | **Edit or turn off** that rule | Low / medium |
| A redirect applies and sends people somewhere unhelpful, with high bounce | Bad redirect | **Fix the redirect's destination, or remove the redirect** | Low / medium |
| Relevant products exist but are missing from results; their titles or attributes lack the term | Weak catalog data | **Fix the product data** (title, product type, attributes) in the feed. This is the longer-term fix; a synonym helps meanwhile | Medium / low |
| Too many loosely related results, such as "black dress" returning black shoes | Precision too loose | Review the query precision and relaxation settings, or add a ranking rule that favours the main product type | Medium / medium |
| Results are relevant, but bounce is high and product views per visit are low; the top results show many near-identical titles | Duplicate listings (sizes or colours listed as separate products) make the grid look repetitive | **Group variants** into one product in the feed (the lasting fix). In the meantime, a ranking rule can bury the duplicates or boost a mix of brands | Medium / low |
| Results are relevant, but well-known or house brands with many products sit deep in the ranking | Ranking lacks brand or product variety | Run an **A/B test of a ranking rule** for the query that boosts those brands by attribute | Medium / medium |
| Engagement and add-to-cart are normal, but conversion is low | After the click: price, stock, product page or checkout | **Not a search fix.** Hand it to the merchandising or product-page team, with the product IDs | — |
| Average order value or revenue per visit is falling while traffic grows | Mix shifting to cheaper items | Use a ranking rule to boost higher-margin or core lines, if that suits the business. Check promotions | Medium / medium |
| Autosuggest steers people to the weaker wording | Autosuggest | Exclude or demote the weak suggestion; fix the main wording with a synonym first | Low / low |

## Notes

- **Synonym direction matters.** In `synonym.explain`, a one-way synonym from A expands A to B, but not B to A. If the catalog mostly says B, a search for A only works if A expands to B. Check every wording you rely on.
- **Bloomreach-generated synonyms** (`type: "BR Generated"`) are created automatically. Adding a user synonym doesn't remove them. Review them, then add your own.
- **Preview before you recommend.** Where you can, show the effect of a fix by running the product grid with the improved wording, or with rules turned off.
- **Prefer an A/B test for ranking changes** on high-traffic queries. Synonyms and redirects for clearly broken queries can usually be applied directly, after confirmation.
