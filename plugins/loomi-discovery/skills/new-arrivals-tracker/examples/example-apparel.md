# Example: new arrivals (demo apparel account)

The account name has been changed to a placeholder. The figures come from a real read-only run against a Bloomreach demo account on 8 October 2026, at account level (no sites). The demo account's release attributes and traffic are synthetic, and the skill's release data check caught that. The run is a good example of what the skill reports when the feed's release dates can't be trusted.

**Prompt:** "Are our new arrivals from the last 30 days getting seen? What should we boost or fix?"

**Calls made (one at a time):** product grid `*` with facets (catalog size and the `released_since` facet); the grid with `fq="released_since:\"New this week\""`, `fq="days_since_release:[0 TO 30]"` and `fq="is_new:\"Yes\""` (counts); `search_discovery_catalogs`; `search_discovery_catalog_products` for one product; `list_facet_attributes` through `call_tool`; `search_dynamic_categories` (by name, the full list, and one by ID); `list_categories`; `get_discovery_product_performance_table` (30 days, one page of 7,000; also 7 days, and 1 day with `page_size=1`); 11 pages of the filtered grid (`rows=200`); the filtered grid with facets (new arrivals per category); grids for /men/suits (200 rows), "suit" (200 rows) and /women/dresses (43 rows). Then `scripts/new_arrivals.py`, `scripts/new_by_category.py` and `scripts/new_in_grid.py` on the saved files. Two calls with `rows=500` and `rows=1000` returned HTTP 500 and were redone with `rows=200`.

## New arrivals: example_apparel (account level, no sites), released in the last 30 days

**Headline:** The release data can't be trusted: every one of the 2,000 "new" products with a release age already had views in the previous 30 days, so fix the feed first. Judged on the whole month, the group gets its fair share of views (index 1.08), but a handful of high-converting new suits are missing from the first 200 results for /men/suits and "suit".

**How new products were found:** `days_since_release:[0 TO 30]` in the product grid: 2,081 of 6,631 products (31%). This is the same set as `is_new = Yes` and as the `released_since` buckets "New this week" (720) plus "1-4 weeks" (1,361). `start_date` is not a release date here: it was May 2025 on a product marked "New this week".

**Release data check: UNRELIABLE.** 2,000 of 2,000 new products with a release age had views in the previous period, before their supposed release. New arrivals held 33.9% of views in both periods. Release ages were ignored, so every product is judged on the whole 30 days. The 7-day and 30-day fallbacks (views now, none before) found no products either: every product in the catalog had views in both periods.

| | New arrivals | Rest of catalog |
|---|---|---|
| Products (share) | 2,081 (31.4%) | 4,550 (68.6%) |
| Share of views (previous period) | 33.9% (33.9%) | 66.1% (66.1%) |
| Share of revenue | 34.2% | 65.8% |
| ATC / conversion / RPV | 39.5% / 26.3% / $30.76 | 39.0% / 25.9% / $30.39 |

Visibility index: 1.08 (no age adjustment, because the release data failed the check). As a group, "new" products are seen and convert just like the rest of the catalog, which is what you'd expect if they aren't really new.

### New-arrivals collection

None. The account has 19 dynamic categories; none uses a release attribute. "New Radiance Collection" is named like one, but its rule is `collection ANY_MATCH "Radiance"`.

### Breakout (327)

| Product | Brand | Visits | Conversion (typical 22.2%) | Revenue | Rank (category) | Action |
|---|---|---|---|---|---|---|
| Linen Checked Casual Shirt (106755) | Lacoste | 12,904 | 33.8% | $495.0k | not checked | Promote; check stock (145 orders a day) |
| Jersey Solid Body Contouring Midi Dress (110726) | Pacific | 7,902 | 29.2% | $382.3k | /women/dresses: 3 of 43 | Protect its slot; check stock |
| X9000L3 Shoes (101358) | Adidas | 8,889 | 30.2% | $325.0k | not checked | Promote; check stock |
| Point Collar Denim Dress (110722) | Pacific | 4,784 | 26.2% | $258.9k | /women/dresses: 9 | As above |
| Crystal Embellished Dotted Dress (110735) | Pacific | 4,441 | 28.5% | $235.0k | /women/dresses: 11 | As above |

327 is a long list because the account's traffic is concentrated: the top products earn far more per day than the median. On a real launch window, expect a handful.

### Buried (34, up to $7.7k)

| Product | Brand | Visits (typical 64) | Conversion (typical 22.2%) | Rank | At stake (working) | Action | Hand-off |
|---|---|---|---|---|---|---|---|
| Blue Slim Euro Fit Party Suit (110071) | Peter England | 45 | 33.3% | /men/suits and "suit": not in the first 200 | $697 ((64 − 45) × 27.8% × $132.00) | One boost rule for new suits on /men/suits and "suit" | `discovery-experiment-setup` |
| Navy Neo Slim Fit Formal Suit (109874) | Peter England | 47 | 34.0% | not in the first 200 of either | $653 ((64 − 47) × 28.1% × $136.56) | As above | As above |
| Navy Slim Fit Tuxedo Suit (109749) | Van Heusen | 45 | 35.6% | not in the first 200 of either | $576 ((64 − 45) × 28.9% × $105.00) | As above | As above |
| Blue Urban Fit Tuxedo Suit (109945) | Parx | 50 | 40.0% | /men/suits: 60 | $488 ((64 − 50) × 31.1% × $112.00) | As above | As above |
| Navy Straight Fit Jeans (107379) | GAS | 52 | 36.5% | not checked | $391 | Check its rank on "jeans" | `discovery-experiment-setup` |

On /men/suits, new products are 30% of the 406 suits but 21% of the first 24 (placement index 0.70; 5 of 24). On "suit", 27% of the first 200 but 17% of the first 24 (0.63). No ranking rules apply to either page, and no A/B test is running. The amounts are small because the demo account's typical product gets only 64 visits a month.

### Slow start (274, up to $81.8k)

| Product | Visits | ATC / conversion (typical 34.2% / 22.2%) | At stake (working) | What to check |
|---|---|---|---|---|
| Panthère de Pacific Style necklace (110695) | 106 | 30.2% / 15.1% | $6.8k (106 × (22.2% − 15.1%) × $900.00) | Add-to-cart normal, conversion low: price at checkout, stock, delivery |
| Tank Française ring (110440) | 545 | 34.3% / 16.2% | $6.4k (545 × (22.2% − 16.1%) × $193.00) | As above: sizes and stock first |
| Louis Philippe White Formal Shirt (108968) | 888 | 32.1% / 13.7% | $4.3k (888 × (22.2% − 13.7%) × $57.00) | As above |

Across all 274, 203 have low add-to-cart (product page or price) and 71 have normal add-to-cart with low conversion (checkout, stock or delivery).

### Invisible (0)

Every new product had views. The product table had a row for all 6,631 products, the same number as the grid. 24 products had fewer than 30 visits: too few to judge.

### Where new products sit

New arrivals make up 24–53% of most categories, close to the catalog's 31%. /women/dresses (21 of 43, 49%) and /handbags/purses (8 of 15, 53%) are mostly new; /kids/activewear (4 products) has none. The category counts suggest every new product sits under a top-level category, so none is reachable by search alone.

### Recommendations

1. **Fix the release data before acting on "new".** Every "new" product had views before its release date, and 31% of the catalog is marked as released in the last 30 days. Check how the feed sets `days_since_release`, `released_since` and `is_new`. Hand-off: catalog owner and `data-feed-health`.
2. **Then build a rule-based New Arrivals collection**: `days_since_release LESS_THAN_OR_EQUAL 30`, or `released_since ANY_MATCH ["New this week", "1-4 weeks"]`. None exists today. Hand-off: `collection-suggester` for the preview and set-up steps.
3. **Test a "new suits" boost on /men/suits and "suit".** Three new suits converting at 33–36% are missing from the first 200 results, and new products are under-placed on both pages (index 0.70 and 0.63). Up to about $2.4k a month for the four suits checked. Hand-off: `discovery-experiment-setup`.
4. **Send the slow-start list to the product and pricing teams**, starting with the necklace, the ring and the white formal shirt (up to $17.5k for those three).
5. **Protect and restock the breakout dresses.** Four are already in the first 15 on /women/dresses. Pass them to `search-demand-to-campaign` for a "new in" email once the release data is fixed.

**Caveats:** demo account with synthetic traffic and release data; account-level reporting; the release check failed, so the groups are judged on the whole window rather than the days each product has been live; revenue at stake is an upper bound for the period, not a forecast.
