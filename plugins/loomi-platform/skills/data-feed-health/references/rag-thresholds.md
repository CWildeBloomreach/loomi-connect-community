# RAG thresholds and pixel issue keys

## Thresholds

Use these as defaults. If the user has their own service levels (for example "the feed must run every 6 hours"), use theirs instead.

### Discovery pixel (per pixel type)

| Status | Rule |
|---|---|
| RED | A core type has an issue rate of 20% or more; **or** it has no events in 24 hours while other page types have traffic; **or** its 24-hour count is less than half its 7-day daily average |
| AMBER | Issue rate from 1% to 20%; **or** the 24-hour count is 25–50% below the 7-day daily average |
| GREEN | Issue rate below 1% and the count is steady |
| NOT IN USE | No events in 7 days for a type the site may not implement (content, thematic, quickview, impressions types) |

Core types: `product-pageview`, `category-pageview`, `search-pageview`, `conversion-pageview`, `atc-event`, `search-event`. Add `suggest-event` and the `widget-*` events if the site uses autosuggest or recommendation widgets.

Small numbers of `cdp_segments_invalid` issues (well under 1%) are common and don't need action on their own.

### Catalogs and jobs

| Status | Rule |
|---|---|
| RED | The latest product feed or index job failed; **or** no successful product feed or index for more than 48 hours, or twice the usual cadence; **or** the product count fell 30% or more between index jobs; **or** the latest run of a Data Hub or v2 Engagement catalog job type failed |
| AMBER | A successful job with a warning in its status message; failures followed by a later success; a product-count drop of 10–30%; last success 24–48 hours ago; standard events or the main catalog not mapped in Engagement |
| GREEN | Recent successes on the usual cadence, no warnings, steady counts |
| NOT ENABLED | The workspace has no Data Hub (`data_engine_url` is null) |
| NOT VISIBLE | Loomi Connect can't show freshness, for example v1 Engagement catalogs |

Work out the usual cadence from the gaps between successful runs of the same job kind in the list.

## Pixel issue keys

These are the `status_key` values seen in testing, with the most likely meaning. Confirm the cause with `get_pixel_event_details` on one sample event before reporting it.

| Key | Likely meaning | Usual fix |
|---|---|---|
| `catalogs_required` | The pixel doesn't send the `catalogs` parameter that this account or page type requires | Add the catalogs parameter to that page type's pixel |
| `cat_id_required`, `cat_required` | A category page view without a category ID or category name | Send `cat_id` and `cat` on every category page |
| `url_invalid`, `ref_invalid` | The page URL or referrer is malformed or missing | Send the full, encoded page URL and referrer |
| `missing_uid` | No `_br_uid_2` cookie value, so the visit can't be tied to a visitor | Check that the tracking cookie is set before the pixel fires, including after consent |
| `cdp_segments_invalid`, `cookie2_cdp_segments_invalid` | The segment value in the cookie couldn't be parsed | Usually low volume; investigate only if it grows |

## Tool quirks seen in testing

- `get_pixel_health_status` can return an empty `top_issues` list for a type with a 100% issue rate over longer windows (for example 168 hours). Use the 24-hour call to read the issue keys.
- `search_discovery_catalog_jobs` ignored the `status` filter. Filter jobs by `status` yourself.
- `search_discovery_catalogs` reports `last_index_refresh_at` for full refresh indexes only. Daily update indexes in the job list can be newer.
- `search_datahub_jobs` with a `project_id` returned no jobs and a hint to try `workspace_id`. A workspace without `data_engine_url` returns an error saying Data Hub may not be enabled.
- `list_catalog_jobs` works only for v2 Engagement catalogs.
