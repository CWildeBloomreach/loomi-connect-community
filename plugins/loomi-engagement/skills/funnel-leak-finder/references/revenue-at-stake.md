# Putting a revenue figure on a leak

These are the formulas `scripts/funnel_leaks.py` uses. Every figure is an estimate. Say which are upper bounds and which rest on an assumed rate.

## Inputs

| Input | From |
|---|---|
| Customers at each step, `n[0..k]` | F1 (`data.total.counts`) |
| Purchasers in the window | F3 |
| Average order value (AOV) | V3 |
| Average cart value | V2 (optional) |
| Customers per step for each segment | F2 or F4, one funnel per value |
| Recovery rate per step | The user's own results, or the defaults below |

## Formulas

For each step `i` after the first:

- **Step conversion** = `n[i] / n[i-1]`.
- **Lost** = `n[i-1] - n[i]`.
- **Downstream conversion** = `n[last] / n[i]`: the share of customers who reached step `i` and went on to buy.
- **Value walking away** = Lost × downstream conversion of the **next** step reached × value, where:
  - for the step into purchase (cart → purchase, or checkout → purchase), downstream conversion is 1 and value is the **lower** of AOV and average cart value;
  - for earlier steps, value is AOV.
  
  This is an **upper bound**: it assumes every lost customer could have been brought back to behave like those who carried on.
- **Realistically recoverable** = value walking away × recovery rate.

For each segment `s` (a device, OS or source):

- **End-to-end conversion** = `n_s[last] / n_s[0]`.
- **Segment gap** = `n_s[0]` × (overall end-to-end conversion − segment end-to-end conversion) × AOV, if positive.
- This answers "how much more would we make if <segment> converted like everyone else". It's an upper bound too.

## Default recovery rates (assumptions)

Use these only when the user has no figures of their own, and always label them "assumed". They're deliberately conservative round numbers, not benchmarks from Bloomreach data.

| Leak | Flow that addresses it | Default recovery rate |
|---|---|---|
| Cart → purchase (or checkout → purchase) | Cart or checkout abandonment | 5% |
| View → cart | Browse abandonment | 1% |
| Purchase → repeat purchase | Post-purchase cross-sell | not estimated here |

If an abandonment flow already runs, the current leak is **after** that flow's effect. The recoverable value is then the extra a better flow would bring (a second message, SMS, a better delay), so halve the default rate, or ask the user.

## When not to put a figure on it

- **The purchase step is unreliable** (F1's last step under about half of F3's purchasers): give view → cart only.
- **Fewer than about 100 customers** at a step or in a segment: show the counts, not a value.
- **No value property is filled:** give customer counts and ask the user for their AOV.
- **A sandbox or test project:** say the figures describe test traffic.

## Projections

Only if asked: monthly value = window value × 30 / window days. Say it's a straight-line projection that ignores seasonality.
