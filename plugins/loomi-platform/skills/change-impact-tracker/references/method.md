# The maths, by hand

`scripts/did_effect.py` does all of this. Use this page if you can't run scripts, or to explain a result.

## Windows

- **Equal length**, before and after, both ending or starting next to the change day, which is **left out** (it's half old, half new).
- **Whole weeks** (7, 14 or 28 days) so each window has the same weekdays.
- **Pair days by date.** `get_discovery_trend` leaves out days with no data and shows `$0.00` for others. If a window has missing days, shorten both windows or work per day with data: divide each window's counts by its number of days with data. The control has the same gaps on the same dates, so the ratio below is barely affected, but per-day scaling keeps visit counts honest.

## Difference-in-differences

For each metric (visits, orders, revenue, conversion = orders ÷ visits, revenue per visit, AOV = revenue ÷ orders):

```
treated change  = treated_after ÷ treated_before
control change  = control_after ÷ control_before
effect          = treated change ÷ control change − 1
```

Example (kids tops, live run): revenue fell 7.1% (6,471 ÷ 6,964); other category revenue fell 1.6%. Effect = 0.929 ÷ 0.984 − 1 = −5.5%.

**Control minus treated.** If the control is a card that includes the treated thing, subtract the treated numbers from the card first.

## Ranges (95%)

Work on the log scale. For one window, the approximate variance of log(metric) is:

| Metric | Variance of log |
|---|---|
| Visits | 1 ÷ visits |
| Orders | 1 ÷ orders |
| Conversion | (1 − conversion rate) ÷ orders |
| Revenue | (1 + cv²) ÷ orders |
| Revenue per visit | (1 − conversion rate + cv²) ÷ orders |
| AOV | cv² ÷ orders |

`cv` is the spread of order values (standard deviation ÷ mean). Its default is 1.0, a typical value for apparel; set `aov_cv` in the input if you know better.

Add the variances of the four cells (treated before, treated after, control before, control after) and take the square root to get `se`. Then:

```
range = exp(log(1 + effect) ± 1.96 × se) − 1
```

The control is usually large, so the treated cells dominate. **Orders drive the uncertainty:** with 150 orders a window, revenue ranges are about ±30%.

**Smallest detectable effect** (80% power): `exp(2.8 × se) − 1`. If this is ±30% and the change could only plausibly move revenue by 5%, observational measurement can't answer the question: recommend an A/B test.

## Conversion noise check (two-proportion z-test)

For the treated group, before (o1 orders out of n1 visits) against after (o2 of n2):

```
p1 = o1 ÷ n1, p2 = o2 ÷ n2, p = (o1 + o2) ÷ (n1 + n2)
z  = (p2 − p1) ÷ sqrt(p × (1 − p) × (1 ÷ n1 + 1 ÷ n2))
```

|z| above 1.96 (p below 0.05) means the conversion change is unlikely to be noise. It doesn't say the change caused it: that's what the control is for.

## Revenue impact

```
expected without the change = treated_after_revenue ÷ (1 + effect)
incremental                 = treated_after_revenue − expected
per 30 days                 = incremental × 30 ÷ days in the after window
```

Apply the same formula to the ends of the effect range for the revenue range. Present it as "about −$1.9k a month (range −$15k to +$7.5k)", never as a single number.

## Placebo

Run the same calculation on two windows that are both before the change (for example the before window against the window before it). The effect should be near zero, with a range that includes zero.

- If the placebo's range **excludes zero**, the treated thing and the control were already drifting apart (the "parallel trends" assumption fails). Choose another control.
- If the placebo's effect is **as large as** the real effect, the real effect is within normal wobble.

## Minimum data

| Check | Threshold | If it fails |
|---|---|---|
| Days after the change | at least 7 | "Too early to tell"; re-run at 14 days |
| Orders per window (treated) | at least 30 | "Too early to tell", unless the range already excludes zero (then flag "thin data") |
| Visits per window (treated) | at least 300 | warn |
| Window lengths | equal | fix the windows |
| Whole weeks | 7, 14 or 28 days | warn about weekday mix |

## What the ranges don't cover

Sampling noise only. They don't cover seasonality specific to the treated products, promotions or emails in one window, other rule changes, stock-outs, tracking changes, or day-to-day swings bigger than Poisson noise (common). The placebo and step 7 of the skill catch most of these. When in doubt, the honest verdict is "no clear effect" plus an A/B test.
