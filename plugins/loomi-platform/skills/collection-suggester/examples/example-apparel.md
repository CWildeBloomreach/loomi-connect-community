# Example: collection suggestions (demo apparel account)

The account name has been changed to a placeholder. The figures come from a real read-only run against a Bloomreach demo account on 8 October 2026. The demo account's traffic is partly synthetic (almost every query grew in line with the site), so treat the numbers as illustrative. The optional co-purchase step was checked against a separate test Engagement project, and no figures from it are shown.

About 30 Loomi Connect calls were made, one at a time.

**Prompt:** "What new collections should we build? Use our search and sales data."

---

## Collection suggestions: example_apparel (account level, no sites), last 30 days (7-day momentum), markets: US, UK, EU (default)

**Headline:** The strongest new collection is **Stone & Khaki Trousers for men**: 57 products are ready under a clean rule, and about 10,000 monthly searches ask for them, a third of which convert at half the site rate. Camo and party dressing have clear demand but not enough stock for a self-updating collection yet.

**Baselines:** search sessions **+56.9%** over 30 days and **−2.9%** over 7 days. Every query grew about 57% in 30 days, so the growth figures below are **against that baseline**. Top-20 query medians: conversion 21.4%, bounce 25.6%.

### 1. Stone & Khaki Trousers (men): neutral chinos and smart trousers in one place

- **Evidence:** "khaki pants" 6,329 sessions (+5.9% vs baseline), 21.1% conversion, $111k revenue. Related trouser searches convert at about half the median: "slacks" 2,289 sessions, 10.8%; "chinos" 1,459 sessions, 11.2%. Upper bound for closing that gap: about **$35k in 30 days** (sessions × conversion gap × AOV; not a forecast). 56 of the 58 products matching "khaki pants" are in /men/pants. Three of the top 15 rising products are men's trousers (a corduroy pant, a wool formal trouser and a grey checked formal trouser).
- **Rule:** `category = /men/pants AND color IN (beige, cream, taupe, khaki, olive)`
  Dashboard conditions (AND): `category_id ANY_MATCH [10200]` (product level); `color ANY_MATCH [beige, cream, taupe, khaki, olive]` (variant level).
- **Preview:** **57 products** (ok); 28 brands, top brand 12%; repeated titles 8% of the first 24 (two Blackberrys and Louis Philippe trousers appear twice).
  Top titles: Louis Philippe Men Beige Classic Regular Fit Solid Formal Trousers · United Colors of Benetton Men Beige Slim Casual Trousers · INVICTUS Men Beige Slim Fit Solid Regular Trousers · John Players Men Beige Slim Fit Solid Regular Trousers · Beige Solid Slim Fit Formal Trouser · Wills Lifestyle Men Beige Slim Fit Solid Formal Trousers · Blackberrys Men Beige Regular Fit Solid Trousers · Allen Solly Men Beige Smart Slim Fit Solid Regular Trousers · ESPRIT Men Beige Solid Slim Fit Shorts (off-theme) · Blackberrys Men Beige Tapered Fit Solid Formal Trousers
- **Overlap with existing:** only catch-all collections ("Under $200", "marketing campaign XYZ"). No duplicate.
- **Use it for:** navigation under Men; redirect target for "khaki pants", "chinos" and "slacks"; an autumn "smart casual" email.
- **Gaps it reveals:** **colour data**. No men's trousers carry "khaki" or "olive" as a colour; 52 of the 58 "khaki pants" matches are coloured `multi`, so they fall outside the rule. Fixing colour values in the feed would roughly double this collection. A pair of shorts is filed under /men/pants.

### 2. Camo: the print shoppers search for, which navigation can't show

- **Evidence:** the camo family has **8,432 sessions and $121k revenue** in 30 days. "camo pants" has 4,816 sessions and 22.0% conversion (above the median), and it was the **#2 riser** of the last 7 days (+10.4% vs baseline). "camouflage regular fit trousers" is +29.5% vs baseline. "camo tee tshirt" (941 sessions) is underserved: 6.9% conversion, 57% bounce.
- **Rule:** **none possible yet.** No facet carries the print. `colors` shows olive, blue or grey, `style` shows "Casual", and titles can't be filtered.
  Interim manual definition (won't update itself): the 10 products matching "camo"/"camouflage" in standard search, IDs 101328, 101291, 104983, 105501, 105699, 107811, 109696, 108026, 105596, 105241.
- **Preview:** **10 products: too thin.** 8 brands, men 4 / women 4 / kids 2. Only 3 are men's trousers, against 4,816 monthly "camo pants" sessions.
- **Use it for:** a redirect from "camo", "camo pants" and "camouflage trousers" to the search results page for "camo" (it already converts well); a "Utility" story in email once stock grows.
- **Gaps it reveals:** add a `pattern` attribute (camo, stripe, check, floral) to the product feed; that makes this and similar print collections rule-based. Raise **men's camo trousers** with buying: high, converting demand and 3 products.

### 3. Party Dresses and Occasion: holiday party season (US, UK, EU: late November–December)

- **Evidence:** "dress" 26,372, "black dress" 22,840, "cocktail dress" 14,376 and "v neck dress" 3,605 sessions: **67,193 sessions and $1.96M** in 30 days, all converting near or above the median. **5 of the top 10 rising products** are dresses (Baroque Print Midi Dress, Printed Long Dress with Windy Flowers, Mini Dress with Silver Heart, Asymmetric Ruffled Strapless Gown, Mirror Embellished Long Sleeved Dress). Jewellery and handbags are also rising (Love necklace, a bracelet, a tote and a handbag).
- **Rule tried:** `category = /women/dresses AND color IN (black, gold, silver, burgundy, maroon, navy blue)`. **Preview: 10 products, 1 brand: too thin.** The whole /women/dresses category has only **43 products**.
  Wider rule tried: `category IN (/women/dresses, /jewellery, /handbags/purses, /men/suits)`. **Preview: 729 products: too broad and unbalanced**, because suits are 56% of it.
- **Recommendation:** don't add a new dresses collection. **Extend the existing "Formal Dresses"** (16 products, dresses AND style = Formal; half of the party-colour preview is already in it) into a "Party Edit", and add a separate **"Party Edit: accessories"** for necklaces, bracelets and purses (about 82 products, from facet counts; not previewed). Build both in the next 2–4 weeks, ahead of the season.
- **Gaps it reveals:** the biggest in the account. Dress search demand is about 1,500 sessions a month per dress in stock. Bring it to buying before the holiday season.

### Fix these existing collections

| Collection | Problem | Fix |
|---|---|---|
| Back in Stock | **Empty.** Its only condition is `rating ≥ 40`, but ratings run from 0 to 5. Not in navigation. | Use a restock or in-stock attribute (or `rating ≥ 4` if a top-rated edit was meant), then add it to navigation |
| summer sale | **3 products.** `category = /shoes/sneakers AND gender = female`; check the gender values used in the feed | Fix the gender value, or widen it to all footwear; rename it if summer is over |
| Heritage | **Manual:** 16 fixed product IDs, no rules, so it won't update itself | Rebuild it on an attribute (for example `collection = Heritage`) if the feed has one |
| test_yellow_color_products | A test category that is **in the navigation tree** | Remove it from navigation |
| Formal Dresses | 16 products (one screen) | Extend as above |

### Seasonal ideas (next 8 weeks; US, UK, EU)

- **Holiday party season** (late Nov–Dec, all three markets): suggestion 3. Backed by data.
- **Holiday gifting under $50 / £40 / €50** (mid Nov–24 Dec): jewellery demand is strong ("wedding band" +8.3% vs baseline, "diamond necklace" +4.0% but 10.7% conversion), but most jewellery costs far more than these caps. **Not previewed;** check a price-capped preview before building it.
- **Black Friday / Cyber Monday** (27–30 Nov 2026, US, UK and EU): an "on sale and best-selling" edit. Existing "Pacific Specials" (`onSale = true`) already covers sale items; refresh it rather than duplicating it.
- **Halloween** (31 Oct; mainly US): no supporting search demand found. Skip it.
- For exact dates and other markets, use the `campaign-planner` skill.

### Assortment gaps (demand without enough stock)

- **Dresses:** about 67k sessions a month against 43 products.
- **Men's camo trousers:** 4,816 sessions against 3 products.
- **Casual trousers (not profiled in this run):** "cargo pants" 6,261, "linen pants" 6,128, "cotton pants" 6,074 and "wide leg pants" 6,001 sessions, each with about 12% conversion and 51–53% bounce. Run `discovery-query-diagnosis` on them before deciding whether this is a ranking, data or stock problem.

### How to set these up

No Loomi Connect tool creates dynamic categories, so set them up in the Discovery dashboard: create a dynamic category, add the conditions listed above (attribute, operator, values, product or variant level, AND), save, check the product count against the preview, then add it to navigation or point the listed queries at it with a redirect.

**Data caveats:** account-level reporting (the account has no sites). Demo traffic is partly synthetic. Co-purchase affinity was **not run**: the test Engagement project has a `purchase_item` event with category levels, so it's feasible, but `estimate_eql_cost` rated the affinity query `very_high`, and the demo Discovery account has no matching Engagement project.
