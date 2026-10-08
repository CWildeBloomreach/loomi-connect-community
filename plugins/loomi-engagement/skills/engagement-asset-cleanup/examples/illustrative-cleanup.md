# Example: asset cleanup (illustrative)

**This example is illustrative.** The method and tool behaviour come from a live, read-only test run, but the project, every asset name and every number have been invented. Nothing was changed in the project.

**Prompt:** "Our Engagement project has years of junk in it. What can we clean up?"

---

## Asset cleanup: Example Store (production), 2026-10-08

**Verdict:** About a third of the project is clutter: 61 items can go. The riskiest item is an active scenario called "TEST - cart reminder v2", which may be messaging real customers.

**Summary:** 14 to delete, 32 to archive, 15 to review with owner, out of 412 assets checked.

| Asset type | Checked | Delete | Archive | Review |
|---|---|---|---|---|
| Scenarios | 118 | 6 | 17 | 5 |
| Email campaigns | 74 | 4 | 9 | 2 |
| SMS campaigns | not checked (no access, HTTP 403) | - | - | - |
| Segmentations | 46 | 2 | 3 | 4 |
| Aggregates | 58 | 2 | 3 | 2 |
| Expressions | 21 | 0 | 0 | 1 |
| Customer filters | 12 | 0 | 0 | 0 |
| Reports, funnels, trends, dashboards | 83 | 0 | 0 | 1 |

### Scenarios
| Name | Status | Last edited | Finding | Suggested action |
|---|---|---|---|---|
| TEST - cart reminder v2 | active | 2026-09-20 | Active, but named like a test | Review with owner |
| Birthday reward | active | 2024-07-02 | Active, untouched for 2 years; no `campaign` events in 30 days | Review with owner |
| Cart reminder / Cart reminder (copy) | active / draft | - | Duplicate names | Review with owner |
| Copy of Welcome series (x6) | draft | 2025-01 to 2025-06 | Test copies, never launched | Delete |
| 17 drafts and inactive flows | draft / inactive | 2023-11 to 2026-02 | Never launched, or stopped 180+ days ago; mostly seasonal ("BF 2024", "Xmas 2023") | Archive |

### Email and SMS campaigns
| Name | Status | Last edited | Finding | Suggested action |
|---|---|---|---|---|
| tmp newsletter, test send, old promo (+1) | draft | 2025 | Test copies | Delete |
| 9 one-off sends named with past dates | inactive | 2024-2025 | Dated, finished | Archive |
| Weekly digest | active | 2024-03-11 | Active, untouched for 19 months | Review with owner |

### Segmentations, aggregates and other analytics objects
| Name | Type | Finding | Suggested action |
|---|---|---|---|
| RFM test, tmp churn | Segmentation | Test copies, nothing references them | Delete |
| 3 segmentations last edited 2024 | Segmentation | Nothing tracked references them; stale | Archive |
| Loyalty tiers / Loyalty tiers v2 | Segmentation | Duplicate names; only v2 is used | Review with owner |
| Total purchases (old), test AOV | Aggregate | Test copies, unreferenced, not exposed | Delete |
| 3 aggregates last edited 2023 | Aggregate | Unreferenced, not exposed | Archive |
| Days since purchase / Days since purchase (copy) | Expression | Duplicate names; usage not checkable | Review with owner |

### Reports, funnels, trends and dashboards
- 31 of 83 aren't in an initiative, while most campaigns are filed. Review with owner and file them (no deletes suggested: analyses have no usage information).

**Not checked:** SMS campaigns (access denied); usage of expressions, customer filters and analyses (no `used_by`). Scenario activity: the 30-day `campaign` event count was rated medium and run.
**Out of scope:** web layers, in-app messages, surveys and experiments: run the onsite-experience-audit skill.
**How to act:** archive or delete in the Engagement UI, checking each item's dependencies there first. Archiving can be undone; deleting can't.
