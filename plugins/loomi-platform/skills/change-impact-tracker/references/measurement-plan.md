# What to measure for each change type

For every change, record **visits, orders and revenue** for the treated group and at least one control, in the same before and after windows. Use the same four dates (`start_date`, `end_date`, `compare_start_date`, `compare_end_date`) in every call.

## Contents

- Discovery: synonym, search ranking rule, redirect, facet rule, media banner, category ranking rule, dynamic category, product boosts
- Engagement: campaign or scenario launch
- Choosing a control

## Discovery

### Synonym

- **Fires?** Product grid for the synonym's source term. In `data.debug["synonym.explain"].directSynonymsV3`, look for a step with `type: "dashboard"` and the synonym's ID in `ids`. Check direction in `synonyms_map[<id>].is_bidirectional`. For a two-way synonym, also check one target term.
- **Treated:** the source term and every target term the synonym touches, from `get_discovery_query_performance` with `search=<word>`. A one-way synonym mainly changes the source term's results; a two-way one changes all of them.
- **Primary metric:** `conversion` or `rpv` (a synonym changes what shoppers see, not how many search). Also report product views per visit (`product_page_views ÷ visits`) and bounce: a recall fix shows up there first.
- **Control:** the search card minus the treated rows; and 5–10 comparable untouched queries of similar size (for example the next queries in the same product type).
- **Watch for:** Bloomreach-generated synonyms and lemmas that already covered the wording (the user synonym then adds nothing); `numFound` changing far more than expected (over-expansion).

### Search ranking rule (boost, bury, pin, attribute boost)

- **Fires?** Product grid for the query: the rule ID is in `customizations_priority.value.ranking` and in `customizations.explain`; per-product `merchandisingRulesApplied` shows `hardBoost` and `productSlot`. To see the rule's effect on today's grid, call again with its ID in `disabled_customization_ids` and compare the top results.
- **Treated:** the rule's queries. `get_ranking_rule` shows `matchType` for each: `EXACT_MATCH` affects that query only; `PHRASE_MATCH` also affects longer queries that contain it. Sum the affected rows.
- **Primary metric:** `rpv` or `revenue`.
- **Also check the products:** `get_discovery_product_performance_table` with `search=<title>` for boosted and buried products (product rows are site-wide, not just from this query, so treat them as supporting evidence).
- **Audience rules:** if `audiences` is not empty, only that audience sees the rule. Account-level numbers dilute the effect; say so and expect "no clear effect" unless the audience is large.

### Redirect

- **Fires?** `search_redirects` with `rule_id`: enabled, in date, right URL and match type.
- **Treated:** redirected searches don't appear in query performance after the redirect. Measure the **destination**: the category row (category table) or the landing page (`get_discovery_page_performance` if available). The "before" for the query itself is its row in the before window.
- **Primary metric:** destination `visits` and `revenue`.
- **Control:** the category card (for a category destination) or the overall card.

### Facet rule

- **Fires?** `customizations.explain` in the product grid has an entry with `ruleType: "facet"` for the query or category. `isLive` is false even on enabled facet rules, so don't rely on it.
- **Treated / control:** as for a ranking rule on the same query or category.
- **Primary metric:** `conversion` (facets help shoppers narrow down; they rarely change traffic).

### Media banner (search or category)

- **Fires?** `get_discovery_media_rule`: enabled, in date. Banners don't change product ranking, so the grid won't show them in the ranking list.
- **Treated:** the query or category the banner is on.
- **Primary metric:** `rpv`, and bounce rate. If the banner links elsewhere, also measure the destination's visits.

### Category ranking rule

- **Fires?** Product grid with `search_by="category"` and the category ID as `query`. The rule ID is in `customizations_priority.value.ranking` and in `customizations.explain` with its `startedAt`, `endedAt` and items.
- **Treated:** the category row in `get_discovery_category_performance_table` (match on `cat_id`; names repeat, for example three "tops" categories for men, women and kids). Use `search=<name>` to keep the response small.
- **Control:** the category card minus the treated row (`subtract_treated`), and sibling categories with no change in the window (for example the other "tops" categories).
- **Primary metric:** `revenue` or `rpv`.

### Dynamic category

- **Fires?** `search_dynamic_categories` with `category_id` for its conditions (list mode returns empty `conditionConfig`), then the product grid with `search_by="category"` and its `brg_dyn_…` ID: `numFound` above 0 and on-topic titles.
- **Treated:** a **new** dynamic category has no "before". Measure its share instead: its visits and revenue in the after window against the parent or sibling categories it draws traffic from, and check whether those fell (cannibalisation) or whether total category revenue rose against the overall card. A **changed** dynamic category (conditions edited) can be measured like a category ranking rule.
- **Primary metric:** `revenue` for the group of categories it affects.

### Product boosts across queries or categories

- **Treated:** the boosted products in `get_discovery_product_performance_table`, filtered with `search=<title>` (one call per product, or one call sorted by revenue with `page_size=100` and a filter on `prod_id`).
- **Control:** similar products in the same category that weren't boosted, or the overall card.
- **Primary metric:** `visits` (a boost mainly moves views) and `revenue`. A boost that raises the product's views but lowers the query's RPV is shifting clicks, not adding sales.

## Engagement: campaign or scenario launch

Reuse the EQL patterns from the `engagement-campaign-digest` skill (`campaign` event; `since …Z until …Z` windows; `estimate_eql_cost` before every query; never `very_high`). Run one query at a time, at least 3 seconds apart.

- **What ran:** `get_campaign_calendar` for the after window (drop `draft` and `inactive` entries) or `search_scenarios` for the scenario. Event-triggered flows don't appear in the calendar; check the `campaign` event for them.
- **New campaign or scenario (no before):** there's nothing to compare for the campaign itself. Measure the **business outcome it targets** instead, for example purchases or revenue in the project, with the window before as the "before" and the Discovery overall card (or a group the campaign didn't reach) as the control. Purchases tagged with the campaign's UTM (pattern D in the digest skill's reference) are supporting evidence, not proof.
- **Replacement or change to an existing campaign:** compare the old and new versions on the `campaign` event: `visits` = delivered, `orders` = clicked (event counts, not people). Control: the project's other email campaigns over the same windows. The two-proportion test then compares click rates.
- **Audience size:** count with aggregate EQL only. Never list customers.
- If the project has no `campaign` events in a window (common in sandboxes), say so and stop.

## Choosing a control

A good control:

- is **not touched** by the change, and had **no other change** in either window;
- is **big enough** to be stable (a card is ideal), or is a group of several similar queries or categories;
- **moves with the treated thing normally.** The placebo (two pre-change windows) tests this: it should show no effect.

Use two controls when you can, one broad (the card minus the treated rows) and one close (comparable queries or sibling categories). If they disagree on direction, report "no clear effect".

Bad controls: the overall card for a search-only change when category traffic moved differently; a sibling category that had its own rule change; any group that includes the treated rows (subtract them).
