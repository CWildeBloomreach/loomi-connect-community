# Synonym risks and fixes

This file matches each synonym flag to a recommendation. Prefer the smallest change that fixes the evidence, and preview it in the product grid where you can.

## One-way or two-way?

| Situation | Use | Example |
|---|---|---|
| The words describe exactly the same products, and the catalog uses more than one | **Two-way group** | tshirt, t-shirt, t shirt, tee |
| A misspelling or shorthand should find the real word, but not the reverse | **One-way** from the misspelling | handbga → handbag |
| The shopper's word is narrower or regional, and the catalog uses a broader or different word | **One-way** from the shopper's word | capris → cropped trousers |
| The shopper's word is broader than the target | **Don't add a synonym.** It would flood a specific query with a broad set. Use a ranking rule or a redirect instead | — |
| Two words overlap but aren't the same product (e.g. "jersey" the fabric and "jersey" the sports top) | **No synonym.** Fix it with ranking or catalog data | — |

**Direction check:** a one-way synonym from A expands A to B, not B to A. If the catalog mostly says B, a search for A works only if A expands to B. List every wording you rely on, and test each one.

## Flags and recommendations

| Flag | Risk | Recommendation | Effort / risk of change |
|---|---|---|---|
| **Missing wording**: another wording returns many more relevant products | High on high-traffic queries | Extend the synonym, or add a two-way group covering every wording | Low / low |
| **Bad expansion that fires**: the synonym adds unrelated products | High; scales with sessions | Add a user synonym or rule that overrides it, or edit or disable the entry if the tools allow. Preview first | Low / medium |
| **Bad chain via a lemma**: a plural or word form leads into a synonym meant for something else (straw → straws → coffee stirrers) | Medium | Fix the synonym at the end of the chain. If the account doesn't sell that product, the expansion only adds noise | Low / low |
| **Too broad** on a short, common word | Medium | Narrow it: one-way from the specific phrase, not the single word | Low / medium |
| **Synonym fires, results still empty** | — (not a synonym problem) | Treat as a catalog gap: redirect, and raise it with merchandising | — |
| **No-op** (source = target) | Low, but it hides an unsolved problem | Replace it with a real mapping, or delete it if the query is a catalog gap | Low / low |
| **Leftover test data** (unrelated targets) | Low if disabled; high if enabled | Delete disabled ones in a clean-up; disable enabled ones first | Low / low |
| **Off-catalog** (products the account doesn't sell) | Low | Clean-up only | Low / low |
| **Listed but not applied** | Low | Note it. Recheck after the next index refresh | — |

## Estimating impact

- For a missing wording on an underperforming query: `sessions × (baseline conversion − query conversion) × average order value`. This is an upper bound for the period.
- For a bad expansion on a healthy query, give the sessions affected, not a revenue figure. The risk is a fall in conversion, which you can't measure until it happens. Suggest an A/B test for changes on queries with high traffic.

## Notes

- Bloomreach-generated synonyms keep applying after you add a user synonym. Review both.
- Hybrid search can hide a missing synonym, because semantic matching still finds some products. Compare `numFound` and titles across wordings, and check `search_mode="standard"` if the counts look similar.
- Synonym changes go live immediately. Writes are blocked while an A/B test runs.
