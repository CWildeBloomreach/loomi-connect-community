# Example: audience opportunities (illustrative)

**This example is illustrative.** The method, the query shapes and the kinds of finding come from live, read-only runs against a real Engagement organisation and a demo Discovery account, but the project name, every segment and scenario name, and every Engagement number have been invented or changed. The Discovery query names come from a demo account (called `example_apparel` here). **The join between that Discovery account and this Engagement project is illustrative**: in the test they were different businesses. Nothing was created.

The ranked table is the output of `scripts/rank_opportunities.py` on [illustrative-opportunities.json](illustrative-opportunities.json).

**Prompt:** "Which audiences are we missing? Where's the untapped revenue in our customer base?"

---

## Audience opportunities: Example Store (production), as of 2026-10-08 10:30 UTC

**Verdict:** The best opportunity is about 14,000 one-time buyers now 1–3 months past their first order, worth about $63,000 over the next 30 days, because nearly all of them can be emailed and no flow targets them. Cart abandoners look bigger on paper, but only 1 in 20 can be messaged, so they rank third and need an on-site approach.

| Rank | Opportunity | Size | Reachable | Est. value (30 days) | Covered by | Action and channel |
|---|---|---|---|---|---|---|
| 1 | Bought exactly once, 31–90 days ago | ~14,000 | 95% (email address) | ~$63,000 | none | "What's next" cross-sell series, email then SMS |
| 2 | First and only order 15–30 days ago | ~5,200 | 94% | ~$37,000 | none (the "Lifecycle Stage (placeholder)" segmentation exists but no scenario uses it) | Second-purchase nurture, email |
| 3 | Added to cart in last 7 days, didn't buy, no email/SMS/push | ~6,000 a week | 5% + on-site | ~$34,000 a month | none: the only active scenarios are on-site A/B splits | Abandonment flow for the 5%; on-site cart reminder and exit-intent email capture for the rest |
| 4 | 2+ orders, $300+ lifetime, no order in 60 days | ~2,100 | 95% | ~$14,000 (partly covered) | partial: a VIP segmentation feeds one draft scenario | Early-access and new-arrivals email, no discount |
| 5 | Viewed women's clothing in last 30 days, never bought it | ~18,000 | 4% + on-site | ~$10,000 | none | Category best-sellers web layer; email for the contactable |
| 6 | 3+ views of shorts in 30 days while "shorts" searches rise | ~3,400 | 18% + on-site | ~$3,000 | none | Homepage and category web layer featuring shorts this week |
| 7 | 2+ discounted orders out of 3 or fewer (margin) | ~900 | 96% | ~$1,200 margin | none | Move to bundles or loyalty points; exclude from blanket discounts |

**How these were worked out:** AOV $95 (30-day AOV query); cart value $110 (30-day average cart query); response rates are the skill's defaults (2–10%); reachability = `email_address` has value, plus a 0.2 on-site factor for anonymous visitors; 21 aggregate EQL counts at 10:30 UTC, all rated high. Estimates, not forecasts. Rows 1 and 2 don't overlap (different windows); rows 5 and 6 may overlap.

**Skipped or not possible:**
- No-consent groups (P8): nobody in the project has any consent recorded, so consent isn't tracked in Engagement. Where is it managed?
- Predictions: not available with this account's permissions (403).

**Data issues found:**
- Category values differ between product views (slugs such as `womens-clothing`) and purchased items (display names), so "never bought it" was matched on a shared word in `categories_path`.
- The category-affinity customer property exists but is empty for almost everyone, so affinity was measured from product views instead.
- Adding "still visiting the site" to the VIP group emptied it: purchases aren't linked to browsing identities. Worth checking with `engagement-tracking-health`.

**Demand signal (example_apparel, last 7 days vs the 7 before):** search sessions overall were down about 3%, while "shorts" grew about 7% (about 10% above the baseline) with conversion in line with top queries.

### Next steps
1. **One-time buyers 31–90 days:** build with `engagement-segment-builder` ("bought exactly once; that purchase in the last 90 days but not the last 30"), then a 2-email cross-sell series with a 10% holdout.
2. **New customers 15–30 days:** reuse the existing "Lifecycle Stage (placeholder)" segmentation as the base in `engagement-segment-builder`; nurture series.
3. **Cart abandoners:** set up the on-site reminder now; the email flow only reaches 5% until more visitors are identified. See `funnel-leak-finder` for the full funnel.
4. **Shorts affinity:** time the shorts web layer with `campaign-planner` while the search trend lasts.
5. For customers beyond 365 days, run `winback-opportunity`; they aren't sized here.
