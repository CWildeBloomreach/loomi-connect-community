# Where predictions hide

A prediction stores its score on each customer under an **output customer attribute**. Anything that targets or measures by that score has to reference either the **prediction ID** or that **attribute name**. Search every definition for both strings.

## What a reference looks like

Engagement customer filters are a list of conditions plus a formula (`"F0&F1"`). Each condition has an `attribute`. Confirmed live:

```json
{"attribute": {"type": "property", "property": "has_wishlist"},
 "constraint": {"type": "boolean", "operator": "is", "value": "true"},
 "type": "attribute"}
```

A prediction usually appears the same way, either as an attribute of type `prediction` that carries the prediction's ID, or as a `property` whose name is the prediction's output attribute. The exact shape of a prediction-type attribute **wasn't seen in testing** (the test accounts couldn't read predictions), so don't rely on the key names: search for the ID and the attribute name as plain strings anywhere in the JSON.

Watch for indirect use: a prediction can feed an **aggregate**, **running aggregate** or **expression**, which is then used by name in a filter. Follow the chain: prediction → derived attribute → filter → campaign.

## Where to look, by object type

| Object | Tool | Where the reference sits | Notes |
|---|---|---|---|
| Segmentation | `search_segmentations` (by ID) | `customer_filter.filters[]` and each `segments[].customer_filter.filters[]` | List mode has no definitions, but has `used_by` |
| Customer filter | `search_customer_filters` (by ID) | `filters[]` | Reusable conditions, used inside other objects |
| Aggregate / running aggregate | `search_aggregates`, `search_running_aggregates` (by ID) | event filter, attribute | Rare for predictions |
| Expression | `search_expressions` (list shows bindings, detail shows formula) | variable bindings | A common way to bucket a score into bands |
| Scenario | `search_scenarios` (by ID, designs stripped) | `condition`, `segmentation-fork`, `limit` and trigger nodes' `customer_filter`; `segmentation-fork` nodes reference a segmentation ID | Use `search_scenario_nodes` via `call_tool` for one node's config |
| Email campaign | `search_email_campaigns` (by ID, `include_design=false`) | `customer_filter` | List mode has no filter |
| SMS campaign | `search_sms_campaigns` (list includes filter) | `customer_filter` | Can return 403 |
| Web layer | `search_banners` (by ID) | customer filter and trigger conditions | Detail includes HTML/JS: never repeat it |
| Report | `search_reports` (by ID) | rows, columns, filters | Reporting only |
| Dashboard | `search_dashboards` (by ID) | embedded analyses | Reporting only |

## Reading `used_by` on a segmentation

A segmentation's list record has a `used_by` list. The prefix says what uses it:

| Prefix | Means | Counts as |
|---|---|---|
| `campaign_design_<id>` | a scenario | activation, if that scenario is active |
| `banner_<id>` | a web layer | activation, if that banner is active |
| `report_`, `metric_`, `dashboard_`, `funnel_` | analytics | reporting only |
| `segmentation_` | another segmentation | follow it |
| `managed_tag_` | a managed tag | neither on its own |

Don't rely on `used_by` alone: email and SMS campaigns, customer filters and derived attributes aren't guaranteed to appear in it, so check their filters directly.

## Status of the user of a reference

- Scenario `status`: `active` counts; `draft`, `inactive` and `paused` are "inactive use only". `is_paused` (paused by Bloomreach) also isn't active.
- Email and SMS campaign `status`: `active` counts. A one-off campaign that already sent is "inactive" afterwards: say it used the model once.
- Banners: only `active` (and, if scheduled, `serving`) counts.
