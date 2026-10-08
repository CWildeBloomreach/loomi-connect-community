# Asset cleanup checks

Apply these to each asset. Report a finding only when the evidence supports it, and say what you couldn't check.

## Suggested actions

- **Delete:** clearly a test or throwaway copy, inactive, and nothing references it.
- **Archive:** no longer used or launched, but may be worth keeping for history. Reversible in the UI.
- **Review with owner:** may be intended, or removing it could break something. A person must decide.

When in doubt, prefer archive over delete.

## What the list tools return (as seen in testing, October 2026)

| Tool | Useful list fields | Usage information | Initiative |
|---|---|---|---|
| `search_scenarios` | `_id`, `name`, `status` (`draft`/`active`/`inactive`/`paused`), `archived`, `tags`, `created`, `edited`; `archived_items_exists` | None. No trigger type or run history in list records | `initiative_id` |
| `search_email_campaigns` | `name`, `status` (`draft`/`active`/`inactive`), `archived`, `tags`, paused flag; paginated with `has_more` / `next_offset` | None | `initiative_id`; filters `initiative_id`, `only_initiatives` |
| `search_sms_campaigns` | `name`, `status`, `archived`, `tags`, schedule, customer filter | None | Not confirmed |
| `search_segmentations` | `_id`, `name`, `archived`, `tags`, `created`, `edited`, `used_by`, `parametrized` | `used_by` | No |
| `search_aggregates` | `_id`, `name`, `archived`, `tags`, `created`, `edited`, `used_by`, `all_exposing_properties` | `used_by`, plus `all_exposing_properties` | No |
| `search_running_aggregates` | `name`, `tags`, `archived` | Not confirmed (returned an empty list in testing) | No |
| `search_event_segmentations` | `name`, `tags`, `archived` | Not confirmed | No |
| `search_expressions` | `name`, context type, variable bindings, `tags`, exposing attributes; `archived_items_exist` | None (but its variable bindings show which aggregates it uses) | No |
| `search_customer_filters` | `name`, `tags`, `archived` | None | No |
| `search_reports`, `search_funnels`, `search_trends` | `_id`, `name`, `archived`, `tags`, `created`, `edited`, `parametrized` | None | `initiative_id` |
| `search_dashboards` | `_id`, `name`, `archived`, `shared`, `home`, `created`, `edited` | None | No |
| `search_initiatives` | `_id`, `name`, `description`, `pinned`, `archived`, `tags` | `get_initiative_items` (via `call_tool`) lists contents | n/a |
| `search_catalogs` | name, type, `catalog_version` | `get_catalog_usages` per catalog | No |

Timestamps are Unix seconds (with fractions). Lists also include `created_by_display_name` and `edited_by_display_name`: never repeat them.

Fields marked "not confirmed" were not seen in a live response. If a field is missing, skip the check that depends on it and say so.

### Reading `used_by`

`used_by` is a list of strings `<type>_<id>`. Seen or documented prefixes:

| Prefix | Means |
|---|---|
| `campaign_design_` | a scenario |
| `banner_` | a web layer |
| `report_`, `funnel_`, `metric_`, `dashboard_` | an analysis |
| `segmentation_` | another segmentation (for aggregates, a segmentation built on it) |
| `managed_tag_` | a managed tag |

An empty `used_by` means **no reference that the API tracks**. It doesn't rule out: Jinja in email or SMS templates (`aggregates.x`, `segmentations.x`), exports and integrations, API consumers, or a person who looks at it in the UI. So unreferenced alone is **review with owner**, not delete.

An aggregate with entries in `all_exposing_properties` is written back to a customer or event property, so something may read it through that property: treat it as used.

Reports, funnels, trends and dashboards have no `used_by`. A report may appear in a dashboard; only the dashboard's detail shows that. Don't call an analysis unused; judge it by staleness and naming only.

## Checks

Defaults: draft 90 days, inactive 180 days, active-but-untouched 365 days, measured from `edited`. Use the user's thresholds if given.

### Drafts and stopped items

| Check | Applies to | Rule | Action |
|---|---|---|---|
| Draft never launched | scenarios, email, SMS | `status` = `draft`, `edited` > 90 days ago | Archive (Delete if also a test copy) |
| Long inactive | scenarios, email, SMS | `status` = `inactive` or `paused`, `edited` > 180 days ago | Archive |
| Paused by Bloomreach | scenarios | appears with `paused_by_bloomreach=true` | Review with owner (find out why first) |
| Old and active | scenarios, email | `status` = `active`, `edited` > 365 days ago | Review with owner: confirm content and audience are current |
| Active but quiet | scenarios | active and no `campaign` events in 30 days (step 4, optional) | Review with owner; check the trigger first |

A `draft` scenario has never been started (a stopped scenario becomes `inactive`). That's the best "never launched" signal the lists give.

### Names

| Check | Rule | Action |
|---|---|---|
| Test copy | name contains (case-insensitive, whole word) copy, "copy of", "(copy)", test, testing, tmp, temp, old, backup, draft, dev, QA, POC, sandbox, "do not use", "dnu", "delete" | Delete if inactive and unreferenced; Review with owner if active or referenced |
| Dated name | name contains a date: `2024-05-01`, `01.05.2024`, `05/01/24`, a year 2015–2029 with a month name, `Q1 2024`, "BF 2023" | Archive if inactive and the date is past; Review if active |
| Labelled archived | name starts with "[ARCHIVED]", "ZZ", "xx" or similar, but `archived` is false | Archive |
| Duplicate | two or more items of the same type with the same name after lowercasing, trimming and removing copy/test/version markers ("v2", "[NEW]", "(1)") | Review with owner: keep one |

Don't flag "[REF]", "[TEMPLATE]" or "template" names as test copies: they're often intentional reference assets. Mention them as Info if they're stale.

### Unreferenced analytics objects

| Check | Rule | Action |
|---|---|---|
| Unused segmentation | `used_by` empty | Review with owner; Archive if also stale (> 180 days) or a test copy |
| Unused aggregate | `used_by` empty **and** `all_exposing_properties` empty, and no expression binds it | Same as above |
| Event segmentation, running aggregate | `used_by` present and empty | Same; if `used_by` isn't returned, "usage not checkable" |
| Expression, customer filter | no `used_by` field | Don't call unused. Judge by name and staleness only, and say "usage not checkable" |
| Catalog | `get_catalog_usages` shows no scenarios, campaigns, recommendations, banners, experiments, in-app messages or surveys, and not in the data mapping | Review with owner (imports and APIs may still write to it) |

### Initiatives (filing)

Treat filing as a convention only if, for a given asset type, **most** (about two-thirds or more) of the live items have an `initiative_id`. Then an item with no initiative is **Review** ("file it in an initiative"). If few items are filed, say "the project doesn't consistently use initiatives" and skip the check.

Also flag initiatives that are empty (`get_initiative_items` returns nothing) or whose items are all archived or long inactive: **Archive** the initiative. Only check initiative contents if there are 20 or fewer initiatives, or the user asks.

## Before recommending deletion

- Archive first where the UI allows it; delete only obvious throwaways.
- A segmentation or aggregate used only by archived items still shows them in `used_by`. Say which kinds of users remain (by type), not their names.
- Scenarios can reference segments in Jinja or webhooks in ways `used_by` doesn't catch. Tell the user to check the UI's dependency panel before deleting.
