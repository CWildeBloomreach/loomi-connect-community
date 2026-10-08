# Example: win-back opportunity (illustrative)

**This example is illustrative.** The method, the queries and the tool behaviour come from a live, read-only test run, but the project, every scenario and segment name, and every number have been invented or changed. Nothing was created.

**Prompt:** "How much revenue are we losing to customers who've stopped buying, and are we doing anything about it?"

---

## Win-back opportunity: Example Store (production), as of 2026-10-08 10:30 UTC

**Verdict:** About 85,000 customers haven't bought in over 90 days. Kept as active customers, they'd be worth about $4.2M a year, and a win-back programme could plausibly recover about $114,000 of that. The 91–365 day groups have no win-back flow at all, so start there.

### Customers by recency and frequency

| Days since last purchase | Customers | 1 order | 2–3 | 4+ | Avg historical value | Revenue at stake (12 mo) | Recoverable | Coverage |
|---|---|---|---|---|---|---|---|---|
| 0–30 (active) | ~25,000 | ~16,000 | 6,000 | 3,000 | $147 | — | — | — |
| 31–90 (lapsing) | ~18,000 | ~12,500 | 4,000 | 1,500 | $133 | $1.1M | $127k | covered |
| 91–180 (lapsing) | ~10,000 | 7,000 | 2,200 | 800 | $132 | $584k | $41k | **uncovered** |
| 181–365 (lapsed) | ~15,000 | ~11,900 | 2,500 | 600 | $113 | $772k | $31k | **uncovered** |
| 365+ (dormant) | ~60,000 | ~51,800 | 7,000 | 1,200 | $100 | $2.8M | $42k | partly covered |

**How these were worked out:** AOV $80 (EQL, average `total_price` over the last 30 days, USD only). Average historical value = AOV × orders, using 1, 2.5 and 5 orders for the three tiers. Revenue at stake assumes retained customers would order 0.5, 1 and 2 times a year. Recoverable revenue applies win-back rates of 12%, 7%, 4% and 1.5% by band. All counts are aggregate EQL counts (16 queries, all rated "high", run with your agreement). These are estimates, not forecasts.

### Existing models, segments and coverage

- **Predictions:** not available: `search_predictions` returned "access denied" for this account.
- **Reusable segments:** *Customer value bands* (lifetime spend tiers) can supply the offer-depth tiers. Nothing segments by recency.
- **Covered:** 31–90 days: *Post-purchase replenishment reminder* (active scenario, email; daily trigger, "purchased 45–90 days ago"). It sends the same message to every tier and has no holdout.
- **Partly covered:** 365+ days: *Annual re-permission* (inactive scenario, last edited 14 months ago). It exists but isn't running.
- **Uncovered:** 91–180 and 181–365 days. No active scenario or campaign targets customers who haven't bought in more than 90 days.

### Recommended win-back programme

| Priority | Group | Trigger / timing | Channels | Offer by value tier | Measure |
|---|---|---|---|---|---|
| 1 | 91–180 days | Daily, on entering the band; 3 steps over about 14 days | Email, then SMS for consented 4+ order customers | 4+: free shipping, no discount. 2–3: 10%. 1 order: 15% second-purchase offer | 30-day reactivation vs a 10% holdout |
| 2 | 181–365 days | On entering the band, then a monthly check | Email; SMS for 4+ only | 4+: fixed $15 reward. 2–3: 15%. 1 order: 20%, plus a "what would bring you back?" survey | Reactivation and discount cost per reactivated customer vs holdout |
| 3 | 31–90 days (improve) | Keep the existing flow | Add web layer personalisation for returning visitors | Split by tier; no discount for this band | Add a 5% holdout to prove its value |
| 4 | 365+ days | Revive the inactive re-permission flow, quarterly | Email only | One seasonal message; sunset non-responders | Re-permission rate; deliverability |

**Next steps**

- Build the audiences with `engagement-segment-builder`: "purchased in the last 180 days but not the last 90" and "purchased in the last 365 days but not the last 180", each split into 1, 2–3 and 4+ orders, with email consent.
- Plan the two new flows with `campaign-planner`: the sequences, offers, exclusions (anyone who buys during the flow exits) and holdouts above.

**Assumptions and gaps:**
- "Purchase" is the order-level `purchase` event. The project also tracks an item-level purchase event, which wasn't used.
- Cancelled orders weren't excluded. The `purchase_status` property exists if you'd like them removed.
- Win-back rates are industry-style defaults. If you've run win-back before, give me your rates and I'll recalculate.
