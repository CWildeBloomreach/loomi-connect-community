# Example: "capris" zero-result demand → campaign brief

**About this example.** The Discovery figures come from a real run against a demo apparel account, renamed here to `example_apparel`. The Engagement side was tested against a **different business's** project, so **the join between the two is illustrative**. The Engagement counts below are made up, and they show the pattern found in testing, not real figures. No draft was created.

**Prompt:** "What are people searching for that we can't sell them, and can we turn that into a campaign?"

## Search demand → campaign: example_apparel (account level) → example-project, last 30 days

**Headline:** "capris" searches are up 77% and return nothing. Search pages are tracked in Engagement, but almost all searchers are anonymous, so the reachable email audience is tiny. The recommendation is a brief, plus identity capture, rather than a draft today.

### Demand (Discovery)
| Query | Sessions (prev → now) | Change | Results / product views | Conversion | Type |
|---|---|---|---|---|---|
| capris | 525 → 929 | +77% | **Zero results** | 0% | Unmet: catalog gap |
| swim trunks | 693 → 1,060 | +53% | 0 product views, 100% bounce | 0% | Unmet: catalog gap |
| sports bra | 562 → 950 | +69% | 0 product views, 100% bounce | 0% | Unmet: catalog gap |
| straw hat | 556 → 888 | +60% | 0 product views, 100% bounce | 0% | Unmet: catalog gap |

Only "capris" appears under the `no_search_results` preset. The others appear under `no_revenue` with 0 product views and 100% bounce, so they're effectively dead ends too.

### Engagement search tracking (illustrative)
**Tier:** B. The search results page is tracked as `page_visit` (path `/search`), with the term in the `q` URL parameter. There is no dedicated search event. A widget's `search_text` property is in the schema, but has had no values in the last 7 days.

| Term | Searchers (30d) | Reachable by email | Proxy: viewed matching products |
|---|---|---|---|
| capris | 410 | **0** | 0 (nothing to view) |
| swim trunks | 380 | **0** | 0 |

### Recommended campaign: "Capris are here" (back in stock)
- **Goal:** recover unmet demand for capris, a +77% rise worth an estimated ~930 sessions a month.
- **Audience:** people who searched for "capris" in the last 30 days and have an email address. Today that's 0, so first widen it to people who **viewed women's trousers or shorts** in the last 30 days and have an email address.
- **Channel:** email.
- **Timing:** only **after merchandising lists capris**. Check that `search_discovery_product_grid_insights` for "capris" returns products.
- **Message:** subject "Capris just landed". Body: three bestselling capri styles. Call to action: "Shop capris".
- **Landing page:** the new capris category, **not** the failing search.
- **Dependencies:** an assortment decision; a synonym or redirect "capris" → cropped trousers as a stop-gap (offer `discovery-query-diagnosis`); identity capture on search.
- **Measure:** the campaign's conversion, and the sessions, product views and revenue of "capris" in Discovery afterwards.

### Tracking to add
- Track a `search` event with `search_term`, `results_count` and `source`. Today the term exists only in the page URL.
- Ask for an email address on zero-result pages (for example, "Tell me when capris arrive"). This turns anonymous searchers into a reachable back-in-stock list.

**Draft:** not created. The reachable audience is 0 and the product isn't live yet.
