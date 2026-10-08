# Example: data and feed health check

**This example is illustrative.** The Discovery section is based on a real read-only run against a Bloomreach demo account, renamed `example_apparel`. The Data Hub and Engagement sections are based on a run against a real organisation, so its names, IDs and figures have been replaced with placeholders and changed numbers.

**Prompt:** "Before I trust this month's numbers: is our tracking and catalog data healthy?"

## Data and feed health: example_apparel (Discovery, account level) and Example Org / Sandbox project, checked 2026-10-08 08:00 UTC

**Overall:** RED: the search results page pixel flags every event, so search page-view reporting is unreliable. Catalog feeds are running daily but with a data warning.

| Area | Check | Status | Evidence | Next step |
|---|---|---|---|---|
| Discovery pixel | search-pageview | RED | 100% of 26.5k events in 24h flagged `catalogs_required`; steady against the 7-day average | Add the `catalogs` parameter to the search results page pixel |
| Discovery pixel | category-pageview | GREEN | 0.05% issues over 7 days; a handful of `cat_id_required` events | Optional: find the page sending a URL instead of a category ID |
| Discovery pixel | product, conversion, add-to-cart, search events | GREEN | below 0.1% issues; counts steady | — |
| Discovery catalog | product feed | AMBER | daily full feed at 00:06 UTC succeeded, but both recent runs warn "Feed data contains null values" | Find and fix null fields in the feed, starting with the product ID named in the warning |
| Discovery catalog | index | GREEN | last update index 6h ago; 8,183 products, unchanged | — |
| Discovery catalog | staging | NOT IN USE | staging catalog has no documents | — |
| Data Hub | jobs | NOT ENABLED | workspace has no Data Hub | — |
| Engagement | catalogs | NOT VISIBLE | 4 product catalogs, all v1, so no job history | Check catalog imports in the Engagement app |
| Engagement | mapping | AMBER | no standard events and no main catalog mapped in the sandbox project | Map purchase, view_item and add_to_cart, and set the main catalog, if features rely on them |

**Not in use:** content, thematic, quickview and impressions pixel types (no or almost no events in 7 days).

**What this means for other reports:** search page-view based metrics may be incomplete until the search pixel is fixed. Search events, product views and orders are healthy, so conversion and revenue reporting can be trusted. Category reports are reliable apart from one page with a broken category ID.
