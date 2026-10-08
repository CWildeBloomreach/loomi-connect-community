# Working out value and revenue at stake

These figures are **estimates built on stated assumptions**, not forecasts. Show the assumptions every time, and replace the defaults with the user's own numbers whenever they have them.

## Inputs

From the EQL queries:

- `N[b]`: customers in recency band *b*;
- `N[b, 2–3]` and `N[b, 4+]`: customers in band *b* with 2–3 and 4+ lifetime orders; `N[b, 1] = N[b] − N[b, 2–3] − N[b, 4+]`;
- `AOV`: average order value (pattern V), or supplied by the user.

Assumptions (defaults, all adjustable):

| Assumption | Default | Why |
|---|---|---|
| Orders per customer, used for historical value | 1, 2.5, 5 for the 1, 2–3 and 4+ tiers | Tier midpoints; 5 is a conservative figure for "4 or more" |
| Orders per year if retained | 0.5, 1, 2 for the 1, 2–3 and 4+ tiers | One-time buyers rarely buy every year; repeat buyers do |
| Win-back rate | 31–90 days 12%; 91–180 days 7%; 181–365 days 4%; 365+ days 1.5% | Typical retail reactivation rates fall sharply with time since purchase. Use the business's own history if it has run win-back before |

## Formulas

**Average historical value per customer in band *b***

    value[b] = AOV × (N[b,1]×1 + N[b,2–3]×2.5 + N[b,4+]×5) ÷ N[b]

**Revenue at stake in band *b*, next 12 months** (what these customers would spend in a year if they behaved like retained customers)

    at_stake[b] = AOV × (N[b,1]×0.5 + N[b,2–3]×1 + N[b,4+]×2)

Don't calculate it for the 0–30 band: they're active.

**Recoverable revenue**

    recoverable[b] = at_stake[b] × winback_rate[b]

**Total opportunity** = the sum of `recoverable[b]` over the **uncovered** and **partly covered** bands. Show the covered bands separately, as "already being worked".

## Worked example (illustrative numbers)

Band 91–180 days: 10,000 customers, of whom 7,000 have 1 order, 2,200 have 2–3 and 800 have 4+. AOV is $80.

- Historical value = 80 × (7,000×1 + 2,200×2.5 + 800×5) ÷ 10,000 = 80 × 16,500 ÷ 10,000 = **$132 per customer**.
- At stake = 80 × (7,000×0.5 + 2,200×1 + 800×2) = 80 × 7,300 = **$584,000 a year**.
- Recoverable at 7% = **about $41,000**.

Say it like this: "About 10,000 customers last bought 3–6 months ago. Kept as active customers, they'd be worth about $580,000 a year. A typical win-back programme recovers around 7% of that, about $41,000."

## Sanity checks

- The five bands should add up to all buyers.
- If the 4+ tier is large in the dormant band, check that the purchase event isn't item-level (inflated order counts).
- If `value[b]` is far above what the user expects, check that the value property is the order total, not a line price, and that it isn't in a minor currency unit (cents).
- If the 0–30 band is empty on a production project, check that purchase tracking hasn't stopped (`engagement-tracking-health`) before telling anyone their customers have all lapsed.
