# Scoring a product's association with a topic

Read this when you score candidate products in step 5. For companion families and their qualifiers, see `topic-mapping.md`. `scripts/score_association.py` implements it; the same rules work by hand.

## What counts as evidence

Loomi Connect has no tool that shows which products shoppers clicked or bought **for a given query**. `get_discovery_product_performance_table` is site-wide. So association comes from **where the search engine ranks a product** across the topic's wordings, checked against keyword matching and the product's title:

| Signal | Why it matters | Weight |
|---|---|---|
| Returned by several wordings | One wording can be ambiguous ("paddle" is also kayaking); several agree | Summed across wordings |
| High position | The engine's ranking already blends relevance and, on most accounts, engagement | 1 / log2(rank + 2): rank 0 = 1.0, rank 9 ≈ 0.29 |
| Wording's demand | A wording with more sessions reflects more shoppers' intent | Share of the topic's sessions, at least 0.05 |
| Keyword (standard) search returns it | Hybrid search fills results with semantically close products even when nothing matches | × 1.5 |
| Title names the topic | The plainest evidence; also the only one for a topic no attribute carries | Sets the tier (below) |
| Title names a neighbour topic and not the topic | Classic false positive: "tennis balls" for "pickleball" | Sets the tier (below) |

Score = sum over appearances of `weight × position × (1.5 if standard mode)`.

Title matching ignores case, and also tries each term with spaces and hyphens removed, so "pickle ball" and "pickle-ball" match "pickleball".

## Tiers

Apply these in order:

1. **off-topic**: title contains an exclude term and none of the topic terms.
2. **core**: title contains a topic term, **or** standard search returns it and two or more wordings return it.
3. **likely**: standard search returns it, **or** two or more wordings return it.
4. **review**: everything else (one hybrid wording only).

Products found only through a companion family's catalog terms get the tier **companion**. They have no association score: they belong because they meet the family's qualifier, which you check by reading the title and attributes. A companion that the topic's searches also return is labelled **both**, the strongest evidence.

Then read the titles. Typical corrections:

- Products that serve the topic without naming it (a "court shoe" in a pickleball search, a "dink practice net") move **up** to likely when the title or category clearly fits.
- Generic items (socks, water bottles, gift cards) that rank because of a popularity boost move **down** to review.
- Multi-sport products ("tennis and pickleball shoe") stay core or likely; they belong in both collections.

Say how many products you moved and why.

## Scope

If the user gave a scope ("equipment only", "women"), apply it as an `fq` on the grid calls. If you couldn't (no attribute for it), drop out-of-scope products by title and say so.

## Comparing a rule with the scored list

For each candidate rule, using all its product IDs (paged to 600 at most):

- **Precision** = (rule products that are core, likely or qualifying companions) ÷ (rule products that were scored). Products the rule returns that never appeared in any wording's top 48 are **unscored**, not wrong. Count them separately and read a sample of their titles. A rule that is mostly unscored is broader than the topic's searches, so judge it by those titles, not by its precision.
- **Core recall** = (core products in the rule) ÷ (all core products).
- **Wrongly included** = off-topic products in the rule.
- **Missed** = core products not in the rule, highest score first.

Good: precision 80% or more and core recall 70% or more. A rule under 12 products is too thin to be a page; consider a wider rule or a manual list. A rule over about 500 products is a category, not a collection.
