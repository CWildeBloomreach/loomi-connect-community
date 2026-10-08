# Example: prediction activation check (illustrative)

**This example is illustrative.** The method and the tool behaviour come from read-only testing, but the project, every prediction, segment, scenario and campaign name, and every date have been invented. Nothing was created or changed.

**Prompt:** "We've built a few predictive models. Is anything actually using them?"

---

## Prediction activation check: Example Store (production), 2026-10-08

**Verdict:** Of 4 predictions, only 1 drives live targeting. The churn model is unused and hasn't been retrained in 5 months; retrain it, then put it behind a win-back flow.

### Models

| Prediction | Type | Output attribute | Status | Used by | Refresh health |
|---|---|---|---|---|---|
| Churn risk 90d | churn | `churn_risk_90d` | **Unused** | — | Last trained 5 months ago, monthly schedule: **stale** |
| Likely to buy 14d | propensity | `purchase_propensity_14d` | **Activated** | 1 active scenario, 1 web layer | Trained 6 days ago: OK |
| Predicted CLV | lifetime value | `predicted_clv` | **Reporting only** | 1 segmentation, 1 dashboard | Trained 3 weeks ago: OK |
| Outdoor category affinity | propensity | `affinity_outdoor` | **Inactive use only** | 1 draft scenario | Never trained: **failing** |

### Where each model is used

- **Likely to buy 14d:** segmentation *Propensity bands* → active scenario *Browse abandonment* (a condition sends high-propensity visitors a reminder without a discount); active web layer *Free shipping bar* targets the top band.
- **Predicted CLV:** segmentation *CLV tiers* is used only by the dashboard *Customer value overview* (`used_by` has `dashboard_` and `report_` entries only).
- **Outdoor category affinity:** referenced by the draft scenario *Outdoor launch*, never started.
- **Churn risk 90d:** no reference in 12 segmentations, 4 customer filters, 9 expressions, 31 scenarios, 40 email campaigns, 6 web layers or 14 reports.

### Activation ideas

| Prediction | Audience | Activation | Measure | Hand off to |
|---|---|---|---|---|
| Churn risk 90d | First retrain. Then top 20% churn risk who bought in the last 180 days | Win-back scenario: reminder, then a value-tiered offer | Reactivation vs a 10% holdout | `winback-opportunity`, `engagement-segment-builder` |
| Predicted CLV | Top CLV tier among customers in their first 60 days | VIP onboarding: early access and service, no discount | 90-day repeat rate vs holdout | `engagement-segment-builder`, `campaign-planner` |
| Outdoor category affinity | Fix training first (no score yet) | Then review and start the *Outdoor launch* draft | Category conversion vs holdout | `engagement-scenario-explainer` |

**What was checked:** all 4 predictions (1 archived prediction listed, not checked); every segmentation, customer filter and expression; all 31 non-archived scenarios; 40 email campaigns (fetched 8 candidates); SMS campaigns skipped (HTTP 403); all 6 web layers; reports and dashboards named after the models or in a `used_by` list.

---

## Fallback mode (when `search_predictions` returns 403)

> **Fallback: predictions not readable with this account (HTTP 403).** To run the full check, a project admin needs to give your user a role that can view Predictions in Engagement. Below, I've used the customer properties you confirmed are prediction outputs (`churn_risk_90d`, `purchase_propensity_14d`). Refresh health can't be judged in this mode.
