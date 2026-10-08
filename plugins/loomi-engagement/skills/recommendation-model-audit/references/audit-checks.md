# Recommendation model audit checks

Apply these to each engine and placement. Report a finding only when the evidence supports it, and say what you couldn't check.

## Severity

- **Action:** probably wrong now (empty, stale or broken recommendations in a live placement). Fix this week.
- **Opportunity:** a high-value placement with no recommendations.
- **Review:** may be intended; a person should confirm.
- **Cleanup:** not used, but clutter. Archive it.
- **Info:** worth knowing.

## What the tools return (as seen in testing)

| Tool | Returns | Notes |
|---|---|---|
| `search_recommendations` (list) | `_id`, `name`, `status` (`running` seen), `archived`, `tags`, `initiative_id`, `created`, `edited`, editor display names | No type or catalog in the list. Returned HTTP 403 in one project |
| `search_recommendations` (by ID) | the list fields plus `definition`: `type`, `mapping.catalog`, `mapping.filter`, `event`, `event_filter`, `date_filter`, `blacklist*`, `dynamic_catalog_filter*`, `customer_preferences*`, `pinning_*`, `model_id`, `status` | No fallback setting was seen in the definition. `model_id` had an `upsale_` prefix even on a `recently_viewed` engine, so don't infer the type from it |
| `search_catalogs` (list) | `_id`, `name`, `type` (`product`, `generic`), `catalog_version` (`v1`/`v2`), `is_product_catalog` | v1 catalogs had `created` and `edited` as `null` |
| `get_catalog_usages` | `used_by.recommendations` (engine `id` and `name`), plus `scenarios`, `email_campaigns`, `sms_campaigns`, `banners`, `experiments`, `in_app_messages`, `surveys`, `other`; `used_by_data_mapping` | Shows what references the **catalog** directly, not where an engine is placed. Don't treat it as engine usage |
| `list_catalog_jobs` | jobs with `type`, `state`, `status_code`, `stats`, `created`, `started` | v2 only. v1 returns `success: false` and "Catalog jobs are not available for v1 catalogs" |

Only the `recently_viewed` type was observed in testing. Other types exist (for example personalised, popular or trending, similar items, bought together); report the `type` value as the tool returns it.

## Catalog checks

| Check | Rule | Severity |
|---|---|---|
| Deleted catalog | `mapping.catalog` isn't in `search_catalogs` | Action |
| Failing catalog | latest import or update job in `list_catalog_jobs` has `state` = `fail` | Action if the engine is used, otherwise Review |
| Stale catalog | last successful job older than 7 days (2 days for price or stock data) | Action if the engine is used in an active placement, otherwise Review |
| Empty catalog | `search_catalog_items` returns no items | Action |
| Freshness unknown | v1 catalog, or v2 with no jobs | Review: confirm the feed with `data-feed-health` |
| Non-product catalog | `is_product_catalog` is false for an engine used in product slots | Review |

Hand every catalog finding to `data-feed-health`. Don't diagnose feeds in this skill.

## Engine checks

| Check | Rule | Severity |
|---|---|---|
| Not running but used | `status` isn't `running` and the engine is found in an active placement | Action: slots may render empty |
| Near-duplicate | two or more non-archived engines with the same `type`, `mapping.catalog`, `event.event_type`, `event.attribute.property`, `mapping.filter`, `event_filter` and exclusions. Differences only in `date_filter` or names still count, but say what differs | Review: keep one, repoint placements, archive the rest |
| No filters, no exclusions | product engine with empty `mapping.filter`, `blacklist_enabled` false, `dynamic_catalog_filter_enabled` false | Review: it can recommend out-of-stock, unavailable or already-bought items. Suggest an availability or stock filter and excluding recent purchases |
| Very restrictive | three or more catalog filters, or a look-back (`date_filter.duration`) under 7 days, or pinning rules that fill most of the slot | Review: risk of empty or repetitive slots. Test with `get_customer_recommendations` if the user can supply a test customer |
| No look-back limit | `date_filter.enabled` false on a behaviour-based engine | Info: it learns from all history, which can surface old products |
| Name doesn't match type | for example "Most popular" or "Shuffle" on a `recently_viewed` engine | Review: either rename or rebuild with the right type |
| No fallback | no fallback is visible in the definition; it's usually set where the engine is called (for example a fill-with-random option in the placement) | Info: mention once; ask the owner to confirm placements handle an empty result |

## Usage checks

| Check | Rule | Severity |
|---|---|---|
| Not found in any active placement | engine ID not found in active scenarios, active email campaigns or serving web layers | Review if edited in the last 90 days; Cleanup otherwise. Always add: "it may be called through the API from the website or app" |
| Only in inactive placements | found only in drafts or inactive placements | Cleanup |
| Test engine | name contains test, copy, old, dev, POC, QA, sandbox, tmp | Cleanup (Review if used in an active placement) |
| Many placements on one engine | one engine serves very different slots (for example home page and abandoned cart) | Info: a slot-specific engine usually performs better |

## Placements that should have recommendations

Flag an active placement as an **Opportunity** when it references no engine:

| Placement (by name or trigger) | Suggested engine type |
|---|---|
| Abandoned cart | similar items or bought together, on the cart items |
| Abandoned browse or product view | recently viewed plus similar items |
| Post-purchase or cross-sell | bought together, excluding purchased items |
| Welcome or onboarding | popular or trending |
| Win-back | personalised, falling back to popular |
| Back in stock or price drop | similar items |
| Home page web layer | personalised, falling back to popular |
| Product page web layer | similar items or bought together |
| Cart web layer | bought together, with a low-price filter |
| 404 or zero-results page | popular or trending |

Match placement names loosely ("cart", "abandon", "browse", "post purchase", "thank you", "welcome", "home", "PDP", "product page"). If a name is ambiguous, list it under Review instead.
