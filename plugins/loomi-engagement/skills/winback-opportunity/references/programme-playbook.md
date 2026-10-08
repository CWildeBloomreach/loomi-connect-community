# Win-back programme playbook

Use this to turn the grid into a programme. Adapt the timings to the business's purchase cycle: if the median time between orders is 60 days, "lapsing" starts at about 1.5× that (90 days), not at 31.

## Principles

1. **Start where the money is and nobody is working it.** Rank uncovered bands by recoverable revenue.
2. **Earlier is cheaper.** A lapsing customer often comes back with a reminder; a dormant one may need a real offer. Spend discount where it changes behaviour.
3. **Protect margin on high-value customers.** Lead with service, recognition and early access, not the deepest discount. Give the deepest offers to low-value, one-order customers, where there's least margin to lose.
4. **Always keep a holdout** (5–10% of each audience, receiving nothing) so you can measure the real lift rather than claiming customers who'd have come back anyway.
5. **Exclude** customers who bought in the last N days (re-check at every step), anyone without consent for the channel, recent complainers, and customers with open returns or service tickets, if that data exists.
6. **Stop when it isn't working.** After the last step, move non-responders to a lower-frequency or sunset path to protect email deliverability.

## Programme by band

| Band | Goal | Trigger and timing | Sequence | Channels |
|---|---|---|---|---|
| 31–90 days (early lapsing) | Nudge back before habits break | Daily, on reaching the band (for example 45 days after the last order, or 1.5× the median repurchase gap) | 1. Personalised reminder (recommendations, back in stock, new arrivals in their category). 2. After 7 days, a social-proof or content follow-up. | Email first; on-site personalisation (web layer) for returning visitors; mobile push for app users |
| 91–180 days (lapsing) | Reactivate with a reason to return | On entering the band | 1. "We miss you" with recommendations. 2. After 5–7 days, an offer sized by value tier. 3. After a further 7 days, a last reminder about the offer expiring. | Email, then SMS for consented high-value customers; paid-media retargeting audiences if available |
| 181–365 days (lapsed) | Win back the valuable ones; learn about the rest | On entering the band, then a monthly check | 1. Strongest offer for the tier. 2. A short survey or preference centre ("what would bring you back?"). 3. Final reminder. | Email; SMS only for high-value; direct mail for the top tier if the business uses it |
| 365+ days (dormant) | Reclaim the few, protect deliverability | Quarterly or seasonal, not continuous | 1. One seasonal re-permission or "still interested?" message. 2. Non-openers move to a sunset list. | Email only, at low frequency |

## Offer depth by value tier

Value tiers come from frequency tiers (1, 2–3, 4+ orders) or from lifetime-spend thresholds (pattern T in eql-patterns.md).

| Value tier | 31–90 days | 91–180 days | 181–365 days | 365+ days |
|---|---|---|---|---|
| High (4+ orders or top spend tier) | No discount: recognition, early access, free shipping | Free shipping or a gift with purchase; personal note | Up to ~10% or a fixed-value reward; consider direct contact | One win-back offer, then a low-frequency path |
| Mid (2–3 orders) | No discount: recommendations | ~10% or free shipping | ~15% | ~15%, one message |
| Low (1 order) | No discount: second-purchase content | ~10–15% second-purchase offer | ~15–20% | Re-permission only; sunset if no response |

These are starting points to **A/B test**, not rules. Test offer depth against no offer within each tier, and keep the holdout.

## Measures

- **Primary:** reactivation rate (purchased within 30 days of entering the flow) versus the holdout, and incremental revenue per customer messaged.
- **Secondary:** discount cost per reactivated customer, unsubscribe and complaint rates, and the 90-day repeat rate of reactivated customers (did they stay?).

## When a band is already covered

Don't recommend a duplicate flow. Instead, check:

- whether it's **active** (an inactive or draft flow isn't coverage);
- whether it covers **every tier** (many flows send everyone the same offer);
- whether it has a **holdout**, so its value can be proven;
- whether its timing matches the purchase cycle;
- whether more than one flow targets the same customers (use `engagement-send-collision-check`).

## Hand-off

- `engagement-segment-builder`: one audience per priority band and tier, for example "bought in the last 180 days but not the last 90, 2+ orders, email consent".
- `campaign-planner`: the sequence, timings, channels and offers above, the exclusions and the holdout.
