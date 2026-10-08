# Example: completed tests (demo apparel account)

The account name has been changed to a placeholder. The figures come from a real run against a demo account. Experiment and rule IDs are left out.

**Prompt:** "How did our last couple of A/B tests do? Did the winners actually win?"

| Experiment | Status | Metric | Declared winner | Recommendation |
|---|---|---|---|---|
| Backpacks test | Completed | RPV | Test (rule) | **Stop**: no real difference; the rule is live but unproven |
| Search terms - shirt | Completed | AOV | Control | **Stop**: far too little traffic to tell |

No experiments are running. One draft ("Search terms - pretty blue shirt") points to rules that no longer exist, so it can't be started.

## Backpacks test (completed, 7 Jan to 13 Jul 2026, 187 days)

**Recommendation: Stop. No meaningful difference.** The rule was shipped as the winner, but the data shows a coin toss.

**What's being tested:** default ranking (control) vs a ranking rule on the Backpacks & Totes category. 100% of traffic, split 50/50.
**Success metric:** revenue per visit. **Declared winner:** Test Bucket B (the rule).

| Bucket | Visits | Conv. rate | ATC rate | AOV | RPV | Lift on RPV | Chance it's best |
|---|---|---|---|---|---|---|---|
| A (control, default) | 21,907 | 20.58% | 35.22% | $126.66 | $26.06 | — | 42% |
| B (rule) | 21,736 | 20.58% | 35.59% | $127.29 | $26.20 | +0.5% | 58% |

**In plain English:** both versions convert at exactly 20.58%, and revenue per visit differs by 14 cents. There's a 58% chance the rule is better, which is barely better than a coin toss. Confidence peaked at 75% after five weeks and then fell back, a classic sign of noise. At about 8,800 visits a month, even if the +0.5% were real it would be worth around $1,200 a month.
**Caveats:** the report only covers 15 Feb to 13 Jul. The first five weeks fall outside the data available. The rule is live now, so keep it only if the merchandising team prefers it for other reasons.

## Search terms - shirt (completed, 29 Apr to 13 Jul 2026, 76 days)

**Recommendation: Stop. Inconclusive; the query is too small to test.**

**What's being tested:** default ranking (control) vs a ranking rule for the search "shirt". 100% of traffic, split 50/50.
**Success metric:** average order value. **Declared winner:** Test Bucket A (control, default ranking).

| Bucket | Visits | Conv. rate | ATC rate | AOV | RPV | Lift on AOV | Chance it's best |
|---|---|---|---|---|---|---|---|
| A (control, default) | 274 | 8.76% | 31.75% | $86.67 | $7.59 | — | not calculated |
| B (rule) | 291 | 10.65% | 31.96% | $72.87 | $7.76 | -15.9% | not calculated |

**In plain English:** only 565 visits and 55 orders in 11 weeks, so confidence couldn't be calculated. The rule's AOV is 16% lower, but that rests on 31 orders. Choosing the control was reasonable, but it wasn't proven. "shirt" gets about 200 visits a month, so a test here would take years to settle.
**Caveats:** consider testing on "shirts" (about 700 visits a month) or the shirts category instead.
