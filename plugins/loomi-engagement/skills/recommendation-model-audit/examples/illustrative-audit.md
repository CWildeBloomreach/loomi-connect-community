# Example: recommendation model audit (illustrative)

**This example is illustrative.** The method and the tool behaviour come from a live, read-only test run, but the project, every engine, catalog and placement name, and every number have been invented or changed. Nothing was changed in the project.

**Prompt:** "Can you audit our recommendation engines? I suspect half of them aren't used and the product emails look stale."

---

## Recommendation model audit: Example Store (production), 2026-10-08

**Verdict:** 3 of 7 engines are used, and the one behind the abandoned-cart email learns from a product catalog that last updated 12 days ago. Two pairs of engines are near-duplicates, and the post-purchase email uses no recommendations at all.

**Inventory:** 7 engines (7 running, 0 archived) on 2 catalogs; placements searched: 9 active scenarios, 4 active email campaigns, 3 serving web layers

### Engines
| Engine | Type | Catalog (freshness) | Learns from | Filters / exclusions | Used in |
|---|---|---|---|---|---|
| Cart cross-sell | bought together | Products (stale: last success 12 days ago) | `purchase_item.product_id`, 90 days | 1 catalog (in stock) | Abandoned cart (scenario) |
| Recently viewed - email | recently viewed | Products (stale) | `view_item.product_id`, 1 quarter | none | Browse abandonment (scenario) |
| Recently viewed - web | recently viewed | Products (stale) | `view_item.product_id`, all history | none | Product page carousel (web layer) |
| Most popular items | recently viewed | Products (stale) | `view_item.product_id`, 1 quarter | none | not found |
| Shuffle picks | recently viewed | Products (stale) | `view_item.product_id`, all history | none | not found |
| Top sellers | popular | Products-legacy (unknown, v1) | `purchase.product_id`, 30 days | 4 catalog, pinning | not found |
| Homepage test copy | personalised | Products (stale) | `view_item.product_id`, 2 days | none | not found |

### Fix now
| Engine or placement | Problem | Evidence | Do this |
|---|---|---|---|
| Products catalog (used by 6 engines) | Stale | Last successful import 12 days ago; the 3 since then failed | Run `data-feed-health` on this catalog before anything else |
| Cart cross-sell | Live in abandoned-cart email on a stale catalog | As above | Fix the feed; meanwhile check the email isn't showing sold-out items |

### Add recommendations here
| Placement | Type | Why | Suggested engine type |
|---|---|---|---|
| Post-purchase thank you | Scenario email | Active, high volume, no engine referenced | Bought together, excluding purchased items |
| Welcome series | Scenario email | Active, no engine referenced | Popular or trending |

### Review
- **Near-duplicates:** "Recently viewed - email", "Recently viewed - web", "Most popular items" and "Shuffle picks" all use the same type, catalog and event, differing only in look-back. Keep one (or two, if email and web need different windows), repoint the placements and archive the rest.
- **Name doesn't match type:** "Most popular items" and "Shuffle picks" are built as `recently_viewed`, so they don't do what their names say.
- **No filters or exclusions:** 5 engines have no catalog filter and no exclusions, so they can recommend out-of-stock or already-bought items. Add an availability filter and exclude recent purchases.
- **Possibly too restrictive:** "Top sellers" has 4 catalog filters plus pinning; "Homepage test copy" looks back only 2 days.
- **Freshness unknown:** "Products-legacy" is a v1 catalog, so it has no job history.

### Clean up
- "Most popular items", "Shuffle picks", "Top sellers" and "Homepage test copy" weren't found in any active placement and haven't been edited for 6+ months: archive them after confirming the website doesn't call them through the API.

**Catalog hand-off:** Products (stale, failing imports) and Products-legacy (v1, freshness unknown): run `data-feed-health` on them.
**Not checked:** inactive and draft placements; API calls from the website or app; recommendation quality for real customers (no test customer supplied).
