# Engagement send collision check

Checks what's scheduled to send in a Bloomreach Engagement project over a window, works out who each send targets, and flags collisions (overlapping audiences messaged too close together), busy days, email and SMS conflicts, and sends with no frequency cap. It never changes anything.

| | |
|---|---|
| **Products** | Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_cloud_organizations`, `list_projects`, `get_campaign_calendar`, `search_scenarios`, `search_scenario_nodes`, `search_email_campaigns`, `search_sms_campaigns`, `search_segmentations`, `get_frequency_policies` |
| **Tested with** | Claude Code: each step run by hand against a live sandbox and a production project; script tested on illustrative data. Those projects had few scheduled message sends, so no real collision has been found with it yet. |
| **Maintainer** | Bloomreach |

## Example prompts

- "Are any of our campaigns clashing next week?"
- "Check the send calendar for October for over-messaging."
- "We're launching the autumn sale SMS on Tuesday. Will it collide with anything?"

See [examples/two-week-check.md](examples/two-week-check.md) for an illustrative output.

## How it works

1. Reads the campaign calendar a week at a time, and leaves out drafts and webhooks.
2. Finds always-on, event-triggered flows, which the calendar doesn't show.
3. Walks each scenario's graph to the segment or filter that each send targets, and cross-checks with segmentations' `used_by` lists.
4. Reads frequency policies.
5. Runs `scripts/find_collisions.py` to count sends per day and pair up close sends to overlapping audiences.

## Notes and limitations

- Audience overlap is judged from definitions, not measured. Different segments of one segmentation can't overlap. Different segmentations or inline filters are reported as "possible overlap".
- The calendar shows planned times for draft scenarios. The skill lists them separately, rather than counting them.
- `get_frequency_policies` and `search_scenario_nodes` are found through `search_tools` and run with `call_tool` when they're not listed directly.
- `search_sms_campaigns` returns HTTP 403 on projects without SMS.
