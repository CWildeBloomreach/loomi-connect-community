# Activation playbook

One concrete activation per model that isn't activated. Pick the row that matches the model type, adapt the score band to how the scores are distributed (ask the user, or use their existing bands), and always include a **holdout** so the model's lift can be measured.

## By model type

| Model type | Audience | Activation | Measure | Hand off to |
|---|---|---|---|---|
| **Churn risk** | High risk (top 20% of scores) who bought in the last 180 days | Win-back or retention scenario: a reminder, then a value-tiered offer; protect margin on high-value customers | Reactivation and retained revenue vs a 10% holdout | `winback-opportunity` to size it, `engagement-segment-builder` for the audience |
| **Churn risk** | Low risk, high value | Exclude from discount-led campaigns to protect margin | Discount cost saved, no drop in conversion | `engagement-segment-builder` |
| **Purchase propensity** (likely to buy in N days) | High propensity, no purchase in the window yet | Timely nudge: browse or cart reminder, recommendations, no discount | Conversion vs holdout | `engagement-segment-builder`, `campaign-planner` |
| **Purchase propensity** | Low propensity | Suppress from high-frequency promotional sends to protect deliverability | Unsubscribe and complaint rates | `engagement-send-collision-check` |
| **Category or product propensity** | High propensity for a category they haven't bought | Category launch or cross-sell email, plus a web layer for returning visitors | Category conversion vs holdout | `segment-opportunity-finder`, `engagement-segment-builder` |
| **Lifetime value** | Top predicted value, especially new customers | VIP onboarding, early access, service rather than discount | 90-day repeat rate and AOV vs holdout | `engagement-segment-builder`, `campaign-planner` |
| **Email engagement / open propensity** | Low predicted engagement | Sunset or re-permission flow; lower frequency | Deliverability, inbox placement | `campaign-planner` |
| **Custom** | Ask the user what the target is | Map it to the closest row above | | |

## Cheap first steps

If the team isn't ready for a new flow, suggest one of these:

1. **Add the score to an existing flow.** Put a `condition` or `segmentation-fork` on the score in an active scenario that already targets the same customers (a win-back flow branching by churn risk), so the offer depth depends on it.
2. **Use it as an exclusion** in a big promotional campaign (low propensity, low value).
3. **Expose it on site:** a web layer shown only to high-propensity visitors.
4. **Turn a reporting-only segmentation into an audience:** if a segmentation already bands the score and only reports use it, that segmentation is the audience. Point the new flow at it rather than rebuilding it.

## Before activating

- **Stale or failing models first:** fix training before anything targets the score. Check the target event still arrives, then retrain.
- **Check the score is filled:** a prediction that has never run leaves the attribute empty, and a filter on it matches nobody.
- **Inactive use:** if a draft or stopped scenario already uses the model, reviving it may be quicker than building a new one. Explain it first with `engagement-scenario-explainer`.
