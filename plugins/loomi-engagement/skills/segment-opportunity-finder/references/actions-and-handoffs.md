# Actions, channels and hand-offs by pattern

Suggest one action per opportunity. Keep it specific enough to brief: trigger or timing, channel, message angle, offer, exclusions and how to measure it. Always recommend a **holdout** (5–10%) so the effect can be measured.

| Pattern | Suggested action | Channel | Offer | Exclusions | Measure |
|---|---|---|---|---|---|
| P1 Browsed category, never bought | Category introduction: best sellers, reviews, "complete the look" from categories they already buy | Email if contactable; web layer or recommendations block on next visit otherwise | None at first; a small first-purchase-in-category incentive on the second touch | Bought in the category in the last 30 days; in an active cart flow | Category conversion vs holdout |
| P2 One-time buyer in repeat window | Replenishment or "next item" reminder timed to the window | Email, then SMS or push if consented | Usually none; cross-sell over discount | Bought again; returned or cancelled the first order | Second-purchase rate vs holdout |
| P3 VIP slowdown | Personal, non-discount touch: early access, new arrivals in their categories, service check-in | Email; paid-social audience for the unreachable | Perks, not discounts | Open support issues; bought in the last 60 days | Purchase rate and spend vs holdout |
| P4 Discount-led | Move to non-price value: bundles, loyalty points, free shipping thresholds. Exclude them from blanket discounts aimed at others | Email; on-site messaging | Smaller or no discount (test depth) | — | Margin per order and purchase rate vs holdout |
| P5 Affinity × trending | Timely category promotion built on what's trending in search this week | Email; homepage or category web layer | New arrivals, trend content | Bought the category in the last 30 days | Category revenue vs holdout; check the search query's conversion too |
| P6 Cart abandoners not contacted | Cart abandonment flow (first send in 1–4 hours, purchase check before every send) | Email for contactable; on-site cart reminder and exit-intent capture for anonymous visitors | None on the first send | Purchased since the cart; contacted in the last 24 hours | Recovery rate vs holdout |
| P7 New, no second purchase | Second-purchase nurture: onboarding series, complementary products, reviews | Email | Small time-limited incentive on the last step only | Bought again | Second-purchase rate within 60 days vs holdout |
| P8 No consent | Consent capture: preference centre, on-site prompt with a clear value exchange, checkout opt-in | Web layer, checkout, transactional emails where allowed | Value exchange (early access, a guide), not just a discount | Already consented | Consent rate; reachable audience growth |

## Who does what next

- **`engagement-segment-builder`**: to build any of these as a customer filter or segmentation. Pass it the plain-English definition and the EQL from the pattern; it confirms before it writes anything.
- **`campaign-planner`**: to choose when to run the campaign-style ideas (P1, P3, P4, P5, P8) against the calendar and avoid clashes.
- **`winback-opportunity`**: for anyone beyond the windows here (no purchase in more than 365 days, or all lapsing tiers together). **Don't size win-back bands in this skill.** If the user asks about lapsed customers, hand off.
- **`funnel-leak-finder`**: if P6 is the top opportunity, for the full funnel and the purchase-identity check.
- **`engagement-scenario-explainer`**: to inspect an existing flow marked "partial" or "inactive".
- **`engagement-tracking-health`**: if a pattern is empty because events, categories or identities look broken.
- **`discovery-trending-searches`**: for the full trend method behind P5.

Mention a hand-off only if it's useful for that opportunity, and only by skill name: some users won't have every skill installed.
