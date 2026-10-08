# Reading audiences from scenarios

Use this when step 4 of the skill is unclear for a particular scenario.

## Node types that matter

| Node type | What it tells you |
|---|---|
| `now-trigger`, `repeated-trigger` and other scheduled triggers | Scheduled entry. `repeated-trigger` has `repeat` (daily, weekly), `days`, `times[{hour, minute}]`, `timezone`, `from_date`, `to_date`. These produce calendar entries. |
| `on-event-trigger`, `on-date-attribute-trigger`, `on-api-trigger` | Always-on entry. Not on the calendar. |
| `condition` | `customer_filter` narrows who continues. Output connector 1 = matches, 2 = doesn't match. Follow the branch that leads to the send. |
| `segmentation-fork` | Splits by segment. Each output is one segment. |
| `ab-split` | Splits traffic; every branch is still the same audience. |
| `limit` | Caps how many customers pass, per period. Note it as protection. |
| `wait-action*` | Delays. Add the wait to the trigger time when comparing send times. |
| `send-email-action`, `send-sms-action`, `send-mms-action`, `push-notification-*` | The send. Read its `frequency_policy` and `consent_category`. |
| `per-customer-webhook-action`, `batch-webhook-action` | Not a customer message. Skip unless the user asks. |
| `label` | A sticky note on the canvas. Ignore. |

## How a segment reference looks

Inside a `customer_filter.filters[]` entry:

```json
{"attribute": {"type": "segmentation", "id": "<segmentation id>"},
 "constraint": {"type": "string", "operator": "equals", "operands": [{"type": "constant", "value": "<segment name>"}]},
 "type": "attribute"}
```

The `has value` form, with an empty operand, was seen in live testing and means "in any segment of that segmentation". The `equals` form above, which picks one segment, is the expected shape but wasn't seen live: check the operator and operands you actually get. `formula` (for example `F0` or `F0&F1`) combines the filters.

Other filter types (customer properties, event aggregates, funnels) are inline conditions. Summarise them; don't try to compare them precisely.

## Segmentations' `used_by`

`search_segmentations` list mode returns `used_by` for each segmentation, with entries prefixed by type: `campaign_design_<id>` (a scenario or campaign), `report_`, `metric_`, `funnel_`, `segmentation_`, `dashboard_`. Only `campaign_design_` entries matter here. An ID there that isn't in your calendar list may be an always-on flow, or an inactive one.

## Things to watch

- One `campaign_id` with several send nodes appears several times on the calendar, once per action.
- Repeating scenarios list every planned occurrence in `times`, so a daily scenario adds one entry per day.
- A scenario can have more than one trigger. Check every trigger node in the graph map.
- Full scenario details can include templates with personal data, such as webhook recipient lists. Don't quote them.
