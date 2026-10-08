# Example: explain and audit (illustrative)

**This example is illustrative.** The structure is based on a live, read-only test run, but every name, ID, date and number has been changed or invented.

## 1. Explain

**Prompt:** "What does the 'Loyalty holdout split' scenario do?"

## Scenario: Loyalty holdout split (active, last edited 2026-05-04)

**In one sentence:** Every evening it puts customers from the loyalty audience who haven't been grouped yet into an 80/20 Target or Control group, so other campaigns can measure the effect of loyalty messages.

**How customers enter:** Daily at 07:30 (Europe/London). There are also one manual "run now" trigger, which is inactive.
**Who qualifies:** Customers in any segment of the *Loyalty audience* segmentation, who haven't already been assigned a group by this scenario (no earlier `campaign` event with action type `split` for this scenario).
**What happens:**
1. Checks the two conditions above.
2. A/B split: 80% *Target*, 20% *Control*. Customers are only assigned a group; the split has no branches, so nothing is sent here.
**Channels:** none. It's an assignment-only flow.

**Things to check:**
- The A/B split has no outgoing branches. That's fine if other scenarios read the group assignment; confirm that's the intent.
- The manual path skips the "not already assigned" check, so a manual run could re-assign customers.

**Not verified:** none.

## 2. Audit

**Prompt:** "Audit our scenarios and tell me what to clean up."

## Scenario audit: Example Project (6 live scenarios, 2026-10-08)

| Scenario | Status | Last edited | Finding | Severity | Suggested action |
|---|---|---|---|---|---|
| Ops alert emails | draft | 2024-12-12 | Stale draft (22 months); 1 email node disconnected ("Old – weekly summary") | Review | Archive, or delete the old node |
| Market test template | draft | 2024-11-08 | Stale draft; no actions on any path | Review | Archive if it's no longer used as a template |
| Market test B | active | 2025-06-27 | Two active market-test scenarios with similar names | Review | Confirm only one should run |
| Service health monitor | active | 2026-08-14 | Webhook with hard-coded recipient list; 1 orphan trigger (weekly, not connected) | Review | Move recipients into a segment; remove the orphan trigger |
| Loyalty holdout split | active | 2026-05-04 | Split with no branches (assignment only) | Info | Confirm intended |
| Market test A | active | 2025-05-30 | No issues found | — | — |

**Summary:** 0 need action, 4 to review, 2 look healthy or informational.
**Not checked:** run activity (the `campaign` event query was rated high cost on this project, and the user didn't approve it); IDs in limit nodes and saved metrics (no read tool).
