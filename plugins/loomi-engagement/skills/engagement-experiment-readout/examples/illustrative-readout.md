# Example: scenario A/B split readout (illustrative)

**This example is illustrative.** The method, query shapes and statistics script are the skill's own, but the project, the scenario and every number are invented. No live test was available when this skill was written. Nothing was changed.

**Prompt:** "How's the A/B test in our welcome flow doing? Can we call it?"

---

| Test | Type | Metric | Lift | Recommendation |
|---|---|---|---|---|
| Welcome series: discount vs no discount | Scenario split | Conversion (7 days) | +16.7% | **Keep running** about 7 more days |

Web experiments: not checked (no access). No email campaigns with A/B tests matched.

## Welcome series: discount vs no discount (scenario split, active, 17 Sep to now, 21 days)

**Recommendation: Keep running, about 7 more days, to the planned 4-week end.** The variant is ahead and just significant, but the lift has faded week by week and the planned end hasn't passed.

**What's being tested:** Control group (welcome email without an offer) vs Variant A (the same email with a 10% first-order code). Planned split 50/50.
**Primary metric:** conversion: a purchase within 7 days of entering the split. **Guardrail:** revenue per customer.

| Variant | Customers | Converted | Rate | Lift vs control (95% CI) | Chance it beats control |
|---|---|---|---|---|---|
| Control group | 10,400 | 312 | 3.00% | — | — |
| Variant A (10% code) | 10,310 | 361 | 3.50% | +16.7% (+0.6% to +35.5%) | 98% |

**Is it real?** Probably, but not by much. p = 0.04, just under the 5% line, and the interval runs from almost nothing (+0.6%) to +35%. At about 15,000 new sign-ups a month, the observed lift is worth roughly 75 extra first orders a month, before the cost of the discount.
**Has it run long enough?** 21 days, 3 whole weeks, against a planned 28. The lift was +45% in week 1, +11% in week 2 and −3% in week 3: a classic novelty pattern, so the long-run effect is likely much smaller than +16.7%. Finding a 10% lift reliably needs about 53,000 customers per variant; it has about 10,300.
**Checks:** split 50.2/49.8 against a planned 50/50, which is fine (p = 0.53). 140 customers (0.7%) landed in both variants after profile merges and were excluded.
**Guardrail:** revenue per customer is $2.80 vs $2.40 (+17%), but not significant (p = 0.15, assuming order values vary by about their own mean). The discount also lowers margin per order, which this readout doesn't measure.
**Assumptions:** purchase = order-level `purchase` event, value `total_price`; 7-day attribution from the split; 95% significance, 80% power, 10% minimum lift worth finding. 5 medium EQL queries and 2 high ones (revenue), run with your agreement, plus 4 weekly queries for the novelty check.

**Next step:** re-read on 15 Oct after the planned end. If the week 4 lift stays near zero, stop the test and keep the version without the discount. To see exactly what each branch sends and who enters the flow, ask for the scenario to be explained (`engagement-scenario-explainer`).
