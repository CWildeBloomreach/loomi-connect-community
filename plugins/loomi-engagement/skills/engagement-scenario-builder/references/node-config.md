# Scenario node configuration

The fields each node type needs in a `create_scenario` or `update_scenario` payload, and the output numbers (`connector_index`) to connect from. Fields sit at the top level of the node, next to `id`, `type`, `name`, `x` and `y`.

Types marked **(seen)** were read from real scenarios saved in Engagement. Others come from the Loomi Connect tool documentation. For any type not listed here, copy an existing node of that type from another scenario rather than guessing its shape: the backend ignores unknown keys silently, so a wrong guess saves without an error and then doesn't behave as intended.

## Outputs

| Node | Outputs (`source.connector_index`) |
|---|---|
| Any trigger | `0` |
| `wait-action` and other waits | `1` |
| `condition` | `1` = matches, `2` = doesn't match |
| `ab-split` | one per variant, numbered by the variant's `id` (not its position). Ids can have gaps, for example `1`, `2`, `4` |
| `ab-split-contextual` | one per variant, numbered `id + 1` (its variant ids start at `0`) |
| `limit` | `1` = within the limit, `2` = over the limit |
| Most actions (`send-*`, webhooks) | `1` = done, `2` = failed |
| `label` | none, and nothing may connect into it |

`0` is the input on every non-trigger node and can't be used as a source. Nothing may connect into a trigger. An output leads to one step.

## Triggers

| Type | Fields |
|---|---|
| `on-event-trigger` **(seen)** | `event: {type, filter: []}`, `delay_seconds` (0–3600, default 30). Optional `re_entry` (true lets a customer start again while already in the flow) |
| `repeated-trigger` **(seen)** | `repeat` (`hourly`, `daily`, `weekly`, `monthly`), `times: [{hour, minute}]` (not for hourly), `minutes: [0-59]` (hourly only; `[]` otherwise), `days` (weekly 1–7 with Monday = 1, monthly 1–31 or `-1` for the last day; `[]` for daily), `timezone` (IANA name), `from_date` / `to_date` (Unix seconds or `null`) |
| `on-date-attribute-trigger` | `attribute: {type: "property", property}`, `trigger_period` (`annually`, `monthly`, `once`), `times`, `timezone`, optional `offset: {units, quantity}` (negative is before: days ±90, weeks ±13, months ±3) |
| `planned-trigger` | `datetime` (Unix seconds; must be in the future when switched on), `active: true` |
| `now-trigger` | none |
| `on-api-trigger` | `trigger: {api_trigger_id, filter: []}` (the ID from `search_api_triggers`) |

Legacy names (`repeat_type`, `repeat_on_days`, `start_date`, `repeat_at_time` …) are rejected by the tool and ignored by the backend.

A weekly or monthly schedule saved with `days: []` is accepted by the backend (it was seen on a real draft) but may never run. Warn rather than refuse.

## Logic

| Type | Fields |
|---|---|
| `condition` **(seen)** | `name` (required), `customer_filter: {filters: [atoms], formula}`. Formula uses `F0`, `F1` … with `&`, `|`, `!`. Atom shapes are in the Loomi Connect guide `scenario-write-best-practices` and the `engagement-segment-builder` skill |
| `ab-split` **(seen)** | `variants: [{id, name, percentage}]` (shares add up to 100), `highest_variant_id_used`, `variants_immutable: false`, `touched: false`. Once a split has run, `variants_immutable` is true: don't change its variants |
| `limit` **(seen)** | `steps: [{group: "", id: <24-hex string>, limit: "<number as text>"}]`, `reset: null` (never resets). The `id` is a new random 24-character hex string for a new limit. `limit` may also be Jinja |
| `label` **(seen)** | `text`, `width`, `height`. A note on the canvas |
| `segmentation-fork`, `ab-split-contextual`, `ab-split-auto-winner` | Not verified. Copy an existing node; don't build from scratch |

## Waits

| Type | Fields |
|---|---|
| `wait-action` **(seen)** | `units` (`minutes`, `hours`, `days`, `weeks`), `count` |
| `wait-action-optimal` **(seen)** | `time_range` (hours, at most 168), `optimize_action_types: null`, `send_before_time: null` |
| `wait-action-dynamic`, `wait-action-silent-hours` | Not verified. Copy an existing node |

## Actions

| Type | Fields |
|---|---|
| `per-customer-webhook-action` **(seen)** | `method`, `url`, `headers: [{name, type: "public", value}]`, `data` (body, may use Jinja), `content_type`, `response_handling` (`discard`), `consent_category`, `general_consent`, `frequency_policy`. `parametrized_parts` repeats `url`, `data` and `headers`: keep both in step. Headers often hold API tokens: never repeat their values |
| `set-property-action` **(seen)** | `properties: [{property, type: "string", value}]`. Only text values were seen; for numbers, booleans or lists, copy an existing node |
| `add-event-action` | `event_type`, `properties: [{property, type, value}]`, `custom_timestamp: false`, `trigger_scenarios` |
| `send-email-action`, `send-sms-action`, push, in-app, banners | Content lives in the node's `design`. Reuse an existing node (fetched with `include_node_designs=true`) or a block/snippet reference. Don't invent a design |

## Scenario-level fields

`name`, `nodes`, `connections`, `last_node_id`.

The tool documentation also lists `description`, `max_customers` and `conversion_goal`, but in testing an `update_scenario` with `description` and `max_customers` set saved successfully and neither was kept. Don't promise them: tell the user to set the description, hourly cap and conversion goal in the Engagement UI.
