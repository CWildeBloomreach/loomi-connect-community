# Example: explain and audit (illustrative)

**This example is illustrative.** The structure is based on live, read-only test calls, but every name, ID, date and number has been changed or invented.

## 1. Inventory

**Prompt:** "List our dashboards."

## Dashboards in Example Project (3, 2026-10-08)

| Name | Home | Shared | Last edited | Archived |
|---|---|---|---|---|
| Weekly KPIs | yes | yes | 2026-09-30 | no |
| Black Friday 2024 | no | yes | 2024-12-02 | no |
| Service health | no | no | 2026-04-30 | no |

Want me to explain any of these?

## 2. Explain a dashboard

**Prompt:** "What does the 'Service health' dashboard show?"

## Dashboard: Service health (last edited 2026-04-30, 9 components)

**In one sentence:** A monitoring page for an automated chat assistant: message volume and error rates over the last hour and day, next to the thresholds at which the team is alerted.

| # | Component | Type | What it shows | Window | Current value | Caveat |
|---|---|---|---|---|---|---|
| 1 | "Last hour" / "Last day" headings | text | Column labels for the tiles below | — | — | — |
| 2 | 4 KPI tiles | metric | Error and "sorry" rates | 1 hour / 24 hours (per heading) | not readable | Saved metrics: definitions not readable through Loomi Connect |
| 3 | Alert thresholds | html | A table of warning and stop thresholds for each rate | — | — | Static text; check it still matches the alerting rules |
| 4 | Daily replies 30D | report | Daily count of `chat` events where `action` = `respond` | Rolling last 30 days | 27 in total; 6 days with messages | Counts messages, not conversations or customers |
| 5 | Daily errors | report | Daily `chat` events where `action` = `error` | Rolling last 30 days | 0 | All zeros: no errors, or the cache is cold. Open it in the UI to confirm |
| 6 | Replies by source | report | Messages by event source | Rolling last 30 days | not calculated | — |

**Caveats across the dashboard:** the top tiles (1 hour, 24 hours) sit next to 30-day charts; read the headings before comparing them.
**Not verified:** 4 KPI tiles (no read tool); report 6 not calculated (ask if you want it).

## 3. Explain a funnel

**Prompt:** "Explain the 'Repeat purchase funnel'."

## Funnel: Repeat purchase funnel (last edited 2024-03-14)

**In one sentence:** Of customers who made a first purchase, how many went on to make a 2nd, 3rd, 4th and 5th.

**What it counts:** Five steps, each a `purchase` event. Step 1 only counts a purchase where the expression *Prior orders* equals 0 (a first order). Steps 2–5 are any later purchase.
**Window:** All time. A 30-day window is configured but switched off, so the funnel covers the project's whole history.
**Conversion window:** None: a customer whose 2nd purchase came two years later still counts.
**Broken down by:** nothing.
**Who's included:** all customers.

**Current numbers:** not calculated (there's no calculate tool for funnels). I can count step 1 and step 2 with EQL; the estimate is "high" on this project. Shall I?

**Caveats:**
- All-time with no conversion window, so it describes lifetime repeat behaviour, not recent performance. It won't move week to week.
- Step 1 depends on the *Prior orders* expression. If that is calculated differently from how the team defines a "first order", step 1 is off.

For questions like "how has repeat rate changed this year?", the `ask-your-data` skill can take it from here using the same definition.

## 4. Audit

**Prompt:** "Audit our saved reports."

## Analysis audit: Example Project (8 checked, 2026-10-08)

| Analysis | Type | Last edited | Finding | Severity | Suggested action |
|---|---|---|---|---|---|
| Email revenue YTD | report | 2025-02-10 | Fixed window 2025-01-01 to 2025-01-31 (ended 615 days ago) but named "YTD" and on the home dashboard | Action | Switch to a rolling or year-to-date window |
| Churn segments | segmentation | 2025-06-01 | Segment 2 uses an archived aggregate | Action | Restore or replace the aggregate |
| Active buyers 30D | report | 2026-08-14 | Counts `purchase` events, not customers, but is named "buyers" | Review | Change to unique customers, or rename |
| Mobile conversion | report | 2026-07-02 | Filters `platform` = `ios`: Android is excluded | Review | Confirm intended; rename if so |
| Daily replies 30D | report | 2026-04-30 | No issues found | — | — |

**Summary:** 2 need action, 2 to review, 4 look healthy.
**Not checked:** numbers (not calculated in audit mode); 3 dashboard KPI tiles (no read tool).
