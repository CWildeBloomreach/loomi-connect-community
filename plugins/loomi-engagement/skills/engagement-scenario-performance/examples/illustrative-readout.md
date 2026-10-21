# Example: scenario readout

Illustrative. Names and numbers are made up.

## Prompt

> How is the abandoned cart flow doing over the last 30 days?

## Output

```
## Abandoned cart — last 30 days

| Step | Sent | Delivered | Opened | Clicked | Unsubscribed | Bought within 3 days |
|---|---|---|---|---|---|---|
| Cart reminder (email) | 18,240 | 98.6% | 38.2% | 6.1% | 0.3% | 7.4% of 17,950 |
| Last chance (email) | 9,880 | 98.2% | 29.5% | 3.0% | 0.9% | 2.8% of 9,690 |
| Cart reminder (SMS) | 2,105 | 91.0% | — | 2.2% | 1.6% | 4.1% of 1,910 |

**Splits:** Discount test: Variant A 9,050 · Control 2,260 (for a winner, ask for an experiment readout)

**Worth fixing:**
1. Cart reminder (SMS): 1.6% unsubscribed and 9% undelivered — check the sender and the consent category.
2. Last chance (email): clicks are half the first reminder's — try a different subject or offer, or test dropping it.

**Not counted:** 4 steps that don't send (waits and conditions)
```
