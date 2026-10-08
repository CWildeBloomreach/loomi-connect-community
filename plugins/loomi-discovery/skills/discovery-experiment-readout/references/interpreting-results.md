# Interpreting Discovery A/B test results

## What the report numbers mean

| Field | Meaning |
|---|---|
| `visits` | Visits assigned to the bucket that saw a search or category page in the test's scope |
| `orders`, `revenue` | Orders and revenue attributed to those visits |
| `cr` | Conversion rate: orders ÷ visits |
| `atc_rate` | Add-to-cart rate |
| `aov` | Average order value: revenue ÷ orders |
| `rpv` | Revenue per visit: revenue ÷ visits. It combines conversion and order value, so it's usually the best single metric for ranking tests |
| `lift.<metric>` | Relative change against the control. 0.05 means +5%, and -0.16 means -16%. The control's lift is always 0 |
| `confidenceValues.<metric>` | Probability (0–1) that this bucket is the best on that metric. Values add up to 1 across buckets |
| `dayWisedata.dailyMetrics.<metric>[]` | Per day: `dailyValues`, `dailyLift`, `cumulativeValues`, `cumulativeLift` and `cumulativeConfidence` |
| `meta.currency` | Currency. `currencySymbol` may come back as a character code (for example "36", which means "$") |

Confidence is only reported for `cr`, `atc_rate`, `aov` and `rpv`. If every bucket's confidence is 0, it wasn't calculated, usually because there was too little data. Treat that as inconclusive, not as "0% chance".

## Thresholds

| Chance the leader is best | How to describe it |
|---|---|
| 95% or more | Conclusive. The difference is very likely real |
| 80–95% | Promising but not proven. Keep running if traffic allows |
| 50–80% | Inconclusive. Close to a coin toss |

Also require:

- **At least 14 days, in whole weeks**, so weekday and weekend shoppers are both covered. Early results swing a lot. A test that looked 84% likely to win after 5 weeks can fall back to 50% by the end.
- **Enough orders.** With fewer than about 100 orders per bucket, even a large lift is unreliable.

## How much traffic a test needs

For a rate metric (conversion or add-to-cart), the visits needed per bucket to detect a relative lift *L* on a baseline rate *p*, at 5% significance and 80% power, are roughly:

  n ≈ 16 × p × (1 − p) ÷ (p × L)²

For example, with a 20% conversion rate, detecting a 10% lift (20% → 22%) needs about 6,300 visits per bucket. Detecting a 1% lift needs about 100 times as many. `scripts/summarise_report.py` does this calculation for you.

Revenue metrics (RPV, AOV) vary more from order to order, so they need more traffic than conversion rate for the same lift.

## Decision table

| Evidence | Recommendation | Wording |
|---|---|---|
| Test ≥ 95% best on the success metric, ≥ 14 days, guardrails not clearly worse | **Ship it** | "The new ranking is very likely better: about +X% revenue per visit, worth roughly $Y a month at current traffic." |
| Control ≥ 95% best on the success metric | **Stop** | "The change makes things worse. Keep the current ranking." |
| Test wins the success metric, but a guardrail is clearly worse (≥ 90% the other way) | **Stop**, or redesign | "It lifts conversion, but order value drops by more, so revenue doesn't improve." |
| Inconclusive, and the remaining traffic needed fits in about 4 more weeks | **Keep running** | "Too early to call. Give it about N more weeks." |
| Inconclusive, and it would take months, or the lift is under about 1% | **Stop**: no meaningful difference | "There's no difference worth having. Keep whichever is simpler to maintain." |
| Report shows no data | **Can't say** | "There's no data for this period. It may be past the retention window, or the session type may be wrong." |

To size the value of shipping, use: (test RPV − control RPV) × monthly visits to the query or category.

## Pitfalls

- **Declared winners aren't proof.** `winnerBucketId` only records what someone chose when ending the test. Check whether the data supported it.
- **Peeking.** Checking every day and stopping as soon as the result looks good inflates false positives. Decide the duration up front.
- **Uneven split.** If a bucket planned at 50% gets noticeably more or fewer visits (more than about 5% off), assignment may be broken.
- **Overlapping changes.** If other rules for the same query changed during the test, the result is muddied. Rule changes inside a running test's scope are blocked, but changes to global rules or the catalog aren't.
- **Small queries.** A test on a query with a few hundred visits a month will almost never be conclusive. Say so, and suggest testing on a broader query or category, or accepting a judgment call.
- **Session type mismatch.** A category test read with `SEARCH`, or the other way round, returns zeros or the wrong traffic.
