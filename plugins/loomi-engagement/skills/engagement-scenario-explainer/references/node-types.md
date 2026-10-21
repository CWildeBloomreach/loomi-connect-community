# Scenario node types

How to read each node type in a `search_scenarios` detail response, and how to say it in plain English. The types marked **(seen)** were seen in live testing. The others come from the tool documentation, so read their fields defensively.

## Triggers (entry points)

| Type | Plain English | Fields to read |
|---|---|---|
| `repeated-trigger` **(seen)** | "Runs every day / week at HH:MM (timezone) for everyone who passes the next conditions" | `repeat` (`daily`, `weekly`, ...), `days` (weekday numbers, 1 = Monday), `times` (list of `{hour, minute}`), `timezone`, `from_date`, `to_date` |
| `now-trigger` **(seen)** | "Runs once, when someone presses Run now" | `active` (`false` means it isn't firing) |
| `on-event-trigger` | "Starts when a customer tracks event X" | the event type and any property filters |
| `on-date-attribute-trigger` | "Starts on (or N days before/after) each customer's date in property X" | the property and offset |
| `on-api-trigger` | "Starts when an external system calls the scenario's API trigger" | — |
| catalog or planned triggers | "Starts when a catalog item changes" / "starts on a fixed date" | — |

A scenario can have **several** triggers. Each one starts its own path, so explain each path separately. The top-level `trigger` field is usually `null`.

The `search_scenarios` list accepts a `trigger_types` filter (`now`, `repeated`, `onevent`, `onapi`, `onapi-interest`, `ondateattribute`, `oncatalog`, `planned`). The list records don't show the trigger type, so use the filter, or read the nodes.

## Logic

| Type | Plain English | Fields to read |
|---|---|---|
| `condition` **(seen)** | "Only customers who ... continue; the others go down the 'no' branch (or stop)" | `customer_filter.filters` (atoms) and `formula` (`F0&F1`, `!F0`, ...). Output `1` = matches, `2` = doesn't match |
| `condition-raw` **(seen)** | "A custom Jinja check: continues only if ..." | `jinja_filter`. Summarise the logic, such as "if the saved metric is above 5", without pasting long templates |
| `ab-split` **(seen)** | "Randomly splits customers: 50% Target, 50% Control" | `variants` (`id`, `name`, `percentage`). Each output is numbered by the variant's `id`, not its position (ids can have gaps). An arrow from a number no variant has is a leftover from a removed variant |
| `ab-split-contextual` **(seen)** | "Bloomreach picks the variant most likely to work for each customer" | `variants` with ids from `0`; each output is `id + 1`. `optimization_goals_events` and `optimization_target` say what it optimises for |
| `segmentation-fork` | "Sends each customer down the branch for their segment in segmentation X" | the segmentation ID and its segments |
| `limit` **(seen)** | "Lets at most N customers through per period (resets daily at ...)" | `steps[].limit` (text; may be Jinja), `reset` schedule (`null` = never resets). Output `1` = within the limit, `2` = over it |

### Reading filter atoms

- `{"type": "attribute", "attribute": {"type": "segmentation", "id": "..."}, "constraint": {...}}`: "is in segment `<value>` of segmentation `<name>`". With the operator `has value` and an empty operand, it means "is in **any** segment of that segmentation".
- `{"type": "attribute", "attribute": {"type": "property", "property": "x"}, ...}`: a customer property check.
- `{"type": "funnel_steps", "steps": [...], "date_filter": {...}}`: "has done event X (with these properties)". Each step's `filter` lists the property checks. If `date_filter.enabled` is `false`, there's no time window, so it's lifetime. In the formula, `!F0` means "has **not** done it".
- A step on the `campaign` event that filters `campaign_id` equal to the scenario's own ID, with `action_type` `split`, means "hasn't already been assigned an A/B group by this scenario". It's a common pattern that keeps group assignment stable across runs.

## Waits

| Type | Plain English |
|---|---|
| `wait-action` | "Waits N minutes / hours / days" |
| `wait-action-dynamic` | "Waits until a date taken from a property or event" |
| `wait-action-optimal` **(seen)** | "Waits for each customer's predicted best send time, within `time_range` hours" |
| `wait-action-silent-hours` | "Holds messages during silent hours" |

## Actions (channels)

| Type | Channel | Fields to read |
|---|---|---|
| `send-email-action` **(seen)** | Email | `name`, `template_id` (`null` means an inline design), `consent_category`, `general_consent`, `frequency_policy` |
| `send-sms-action`, `send-mms-action` | SMS / MMS | `name`, `consent_category` |
| `push-notification-mobile-action`, `push-notification-browser-action` | Push | `name`, `consent_category` |
| `send-app-inbox-action` | App inbox | `name` |
| `serve-banner-action` | On-site banner | `name` |
| `per-customer-webhook-action` **(seen)** | Webhook, one call per customer | `method`, the host of `url` only, `response_handling`. **Never paste `data`, `headers` or full URLs.** They can contain email addresses and tokens |
| `batch-webhook-action` | Webhook, one batched call | as above |
| `add-event-action` | Tracks an event on the customer | event type |
| `set-property-action` | Updates a customer property | property name |

## Other

| Type | Meaning |
|---|---|
| `label` **(seen)** | A note on the canvas, written by the author. It has no connections and that's normal. Read its `text` for purpose and warnings |
