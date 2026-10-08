# Dynamic category checks and priorities

These are the checks `scripts/review_dynamic_categories.py` runs, so you can apply them by hand if scripts aren't available. "With traffic" means at least 100 browse sessions in the period. "Dynamic median" is the median across dynamic categories with traffic.

| Check | How to spot it | Priority | Suggested action |
|---|---|---|---|
| **Empty** | Grid `numFound` is 0 | Fix now if it has any sessions; otherwise Tidy up | Correct the conditions (check the values exist in the catalog with `search_discovery_catalog_products`), or retire it and remove links |
| **Near-empty** | Fewer than 24 products (one screen) | Fix now with traffic; otherwise Tidy up | Widen the conditions so the page fills a screen with on-theme products |
| **No conditions** | `conditionConfig.rules` is empty and `productIds` is empty | Fix now with traffic | Add conditions, or retire it |
| **Fixed date in the past** | A condition on a date attribute (`start_date`, `end_date`, …) whose value is before today | Fix now with traffic | Update or remove it; use a relative attribute such as `days_since_release` |
| **Name promises a sale** | Name contains sale, offer, deal, discount, clearance or BOGO, and the grid's `onSale` facet has no `true` values | Fix now with traffic | Add an `onSale` or price condition, or rename it |
| **Traffic but poor performance** | With traffic, and conversion more than 25% below the dynamic median, or bounce more than 25% above it | Fix now | Check that the products match the name and purpose first; then hand ranking work to `discovery-category-health` |
| **Traffic to a deleted category** | A `brg_dyn_` row in the performance table with no matching definition | Fix now with traffic | Fetch it by ID; if it's gone, fix the links that still point to it |
| **Hard-coded product IDs** | A condition on `pid`, `sku`, `product_id` or a similar attribute, or non-empty `productIds` | Make robust with traffic; otherwise Tidy up | Replace with an attribute condition (brand, collection, tag), so new and replacement products join automatically |
| **Single-value definition** | Exactly one condition with exactly one value | Make robust with traffic | Add a fallback (a second value or attribute with `OR`), or monitor that value in the feed. One feed change empties the page |
| **Seasonal or campaign tag** | A condition on `season`, `collection`, `campaign`, `tag`, `special_offer`, `is_new`, `released_since` and similar, or a value such as "summer", "black friday" or a year | Make robust with traffic | Confirm the tag is still maintained in the feed; plan an end date or a replacement definition |
| **Duplicates a static category** | 80% or more of its products sit in one static category, and overlap (shared ÷ (A + B − shared)) is 80% or more | Make robust | Link to the static category instead, or make the dynamic one distinct |
| **Overlaps another dynamic category** | Overlap of 80% or more between two dynamic categories | Make robust | Merge them, or sharpen one definition so each page has a distinct purpose |
| **Re-slices static categories only** | Every condition is on `category_id` | Review | Check whether shoppers need it as a separate page |
| **Test or demo name** | Name contains test, demo, example, sample, temp or "copy of" | Fix now with traffic; otherwise Tidy up | Remove it from live links, or rename it and make it a real collection |
| **Seasonal name, evergreen definition** | The name mentions a season or campaign, but no condition does | Tidy up | Rename it, or tie it to the season and plan its end |
| **No tracked traffic** | Defined, but not in the performance table for the period | Tidy up | Retire it if nothing links to it; check pixel tracking if it should have traffic |
| **Not in the navigation tree** | Empty `paths` | Info | Fine for campaign landing pages; otherwise add it to the navigation |
| **Big swing after an edit** | Revenue changed by 100% or more against the previous period, and the definition was edited in the last 90 days | Info | Confirm what changed before reporting it as a win or loss |

## Notes

- **Containment isn't duplication.** A "Women's sneakers under $100" collection is a subset of /shoes/sneakers by design. It's only a duplicate when the two are about the same size.
- **Facet counts can overcount.** Colour facets count variants. The category facet counts products, but it may list only the top values on very large categories, so a missing overlap isn't proof there is none.
- **Single-value isn't always wrong.** `onSale = true` is a simple, stable definition for a sale page. Flag it, but judge whether the attribute is reliably maintained.
- **Price-capped collections** have low AOV and RPV by design. Judge them on bounce and conversion.
- **Empty can be temporary.** A category for a brand or drop that hasn't arrived yet may be empty on purpose. Ask before recommending deletion.
