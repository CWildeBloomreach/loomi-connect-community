# Example: "tshirt" (demo apparel account)

The account name has been changed to a placeholder. This example comes from a real run against a demo account, from which the skill was developed.

**Prompt:** "Why is tshirt performing so badly in search, and how do we fix it?"

## Query diagnosis: "tshirt" (example_apparel, account level, last 30 days)

**Verdict:** "tshirt" finds less than half the T-shirt range, because its synonym is one-way. Making the synonym two-way across tshirt, t-shirt and t shirt should fix most of the problem.

| Metric | "tshirt" | Baseline (top queries) |
|---|---|---|
| Visits | 20,497 | — |
| Conversion rate | 11.4% | ~21.4% |
| Bounce rate | 60.4% | ~25.6% |
| Product views / visit | 0.40 | ~0.76 |
| Revenue / visit | $4.97 | ~$21 |

**What shoppers see:** 26 results. The top result is a shorts-and-tee set, followed by a thermal top.
**Wording comparison:** "tshirt" returns 26 products; "t-shirt" returns 65.
**Synonyms / rules / redirects in play:** A Bloomreach-generated **one-way** synonym expands tshirt to tee and t shirt, but not to "t-shirt". No ranking rules apply to this query, and no A/B test is running.

### Recommended fixes
1. **Make the synonym two-way: tshirt ↔ t-shirt ↔ t shirt ↔ tee.** Evidence: the hyphenated wording finds 2.5× as many products. Impact: up to about $90k over 30 days (20.5k visits × 10-point conversion gap × $43.68 average order value). Effort: low. Check by: re-running the product grid for "tshirt" and confirming about 65 results.
2. **Bury bundled sets and thermals for this query** if they still rank first after fix 1. Effort: medium. Check by: an A/B test.
3. **Add "T-shirt" to product titles and product type** in the feed where items are called only "Tee". Effort: medium. This is a longer-term fix.
