# Statistics for Engagement A/B test readouts

Engagement has no "experiment report" tool in Loomi Connect, so this skill works the statistics out itself from aggregate counts. `scripts/ab_stats.py` does every calculation here. If you can't run it, do the same sums by hand and show the working for at least one variant.

## Inputs, per variant

| Input | What it is | Where it comes from |
|---|---|---|
| `n` | Unique customers assigned to the variant (for email: unique customers delivered) | EQL pattern A1 or A2 in [data-sources.md](data-sources.md) |
| `conversions` | Unique assigned customers who did the goal (purchase, or click for a click metric) in the attribution window | EQL pattern C1 or C2 |
| `revenue` | Total revenue from those customers in the window (only for a revenue metric) | EQL pattern R1 |
| `planned_share` | The split the test was set up with | The scenario's `ab-split` node, the campaign's A/B config, or the experiment's variants |

Always use **unique customers**, not event counts. A customer who is shown a web experiment ten times counts once.

## Rate metrics (conversion, click)

For control rate p₁ = c₁ / n₁ and variant rate p₂ = c₂ / n₂:

- **Absolute lift** = p₂ − p₁, with a confidence interval of ± z × √(p₁(1−p₁)/n₁ + p₂(1−p₂)/n₂).
- **Relative lift** = p₂ / p₁ − 1. Its interval comes from the log of the ratio: exp(ln(p₂/p₁) ± z × √((1−p₁)/c₁ + (1−p₂)/c₂)) − 1. This interval isn't symmetric, which is correct.
- **Significance**: two-proportion z-test with the pooled rate. Two-sided p-value.
- **Chance to beat control**: Bayesian, with flat Beta(1, 1) priors, by simulation. This is the figure Bloomreach's own Bayesian calculator reports, and it is easier for a marketer to read than a p-value. It is **not** the same as "95% significant": a 95% chance to beat control is roughly a one-sided test at 5%.

z is 1.96 for 95% intervals. With several test variants, the script uses a **Bonferroni** correction: α ÷ (number of test variants), so 2 variants against one control use 97.5% intervals.

## Revenue metric (revenue per customer)

Revenue per assigned customer = revenue ÷ n. Its significance needs the spread of revenue across customers, which aggregate EQL can't return. The script assumes:

- non-buyers contribute 0;
- buyers' revenue has a standard deviation equal to `aov_cv` × its mean (default **1.0**, typical for retail orders; use 1.5–2 for catalogues with a long tail of big orders).

It then runs a z-test on the difference in means. **Always state this assumption.** Revenue metrics need far more traffic than conversion for the same lift. If the user has per-customer revenue variance from elsewhere, use it.

When conversion and revenue per customer disagree, Bloomreach's guidance is to trust revenue per customer (RPV) for business impact, but only once it is itself significant.

## Sample size and "how much longer"

Customers needed per variant to detect a relative lift L on a baseline rate p, at two-sided α and power 1−β:

  n = [z₍α/2₎ √(2 p̄(1−p̄)) + z₍β₎ √(p(1−p) + p′(1−p′))]² ÷ (p′ − p)², with p′ = p(1+L), p̄ = (p+p′)/2

Rule of thumb at 5% and 80% power: n ≈ 16 × p(1−p) ÷ (pL)². At a 3% conversion rate, finding a 10% relative lift needs about 53,000 customers per variant.

**Days remaining** = (n needed − n so far) ÷ (n so far ÷ days run). Report it for:

1. the **observed** lift (how long until this result, if real, is confirmed), and
2. the **minimum detectable effect** (MDE) the user cares about (default 10% relative).

If the remaining time is more than about 4 weeks, or more than a year for the observed lift, the test is very unlikely to settle: recommend stopping as inconclusive.

## Validity checks

| Check | Rule | What to say |
|---|---|---|
| **Sample ratio mismatch (SRM)** | Chi-square test of actual `n` against `planned_share`. p < 0.001 is a mismatch | "The split is off plan, so assignment or tracking may be broken. Don't trust the result until it's explained." Common causes: conditions after the split node, consent filtering in one branch only, a changed ratio mid-test |
| **Mixed customers** | Customers who appear in more than one variant (profile merges across devices) | Exclude them. If more than about 5% are mixed, say the result is less reliable |
| **Duration** | At least 7 days, ideally 14+ and whole weeks; Bloomreach recommends 1–2 full business cycles | Under 7 days: "Too early, whatever the numbers say" |
| **Planned end** | If a duration was set up front and hasn't passed, don't call it early | "Significant now, but stopping before the planned end inflates false positives" |
| **Peeking** | Results checked repeatedly with no planned end | Require p < 0.01 (99%) before calling a winner, and say why |
| **Novelty** | Lift in the first week much bigger than in the last (the later figure under half the first) | "The lift is fading. The long-run effect is likely nearer the recent figure" |
| **Ratio changed mid-test** | The split percentages were edited while running | Bloomreach warns this skews results. Evaluate only the period after the change, or start a new test |
| **Automatic winner tests** | Scenario or email A/B tests set to "automatic winner" | The test phase is short (often hours) and on a small sample. Read out the test phase only; after it, nearly everyone gets the winner, so there's no comparison left |
| **Email opens** | Open-rate metric | Opens are inflated by mail privacy features. Prefer clicks or conversions |

## Decision table

| Evidence | Recommendation |
|---|---|
| Variant significantly better on the primary metric (p below the threshold, or ≥ 95% chance to beat control), duration ≥ 14 days in whole weeks (or the planned end has passed), no SRM, no fading lift, and no guardrail clearly worse | **Call the winner** |
| Control significantly better, or a guardrail clearly worse (for example conversion up but revenue per customer significantly down, or unsubscribes significantly up) | **Stop: keep the control** |
| Not yet significant, and the observed lift or the MDE can be reached in about 4 more weeks at the current rate | **Keep running** for about N more days |
| Significant but before the planned end, under 14 days, or the lift is fading | **Keep running** until the planned end, then re-read |
| Not significant, and it would take months, or the CI is tight around zero | **Stop as inconclusive**: no difference worth having. Keep the simpler or cheaper variant |
| SRM detected | **Fix before deciding**: investigate assignment; don't call it either way |
| No data for a variant | **Can't say**: check the variant names and that the split tracks events |

Guardrails: for a conversion test, check revenue per customer; for an email test, check unsubscribes and complaints; for a click test, check conversion.

To size a winner: (variant revenue per customer − control revenue per customer) × customers per month entering the test. Label it an estimate.
