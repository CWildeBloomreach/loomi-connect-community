# Example: category health check (demo apparel account)

The account name has been changed to a placeholder. The figures come from a real read-only run against a Bloomreach demo account, from which the skill was developed. The demo account's traffic is partly synthetic, so treat the numbers as illustrative.

**Prompt:** "How are our category pages doing? Anything broken or underperforming?"

## Category health: example_apparel (account level, no sites), last 30 days

**Headline:** Category pages grew revenue 57% with steady conversion, but a cluster of apparel sub-categories converts at half the rate of their peers, and one dynamic category is completely empty.

| Metric | Value | vs previous |
|---|---|---|
| Category revenue | $11.88M | +57.1% |
| Conversion rate | 31.4% | +0.9% |
| Revenue / visit | $40.59 | +0.8% |
| AOV | $129.24 | −0.1% |
| Bounce rate | 36.0% | −1.1% |

**Top categories (by sessions):** Under $200 (dynamic): 27.3k sessions, 15.2% conversion · House Specials (dynamic): 22.2k, 15.7% · marketing campaign XYZ (dynamic): 15.8k, 16.3% · /men/pants: 10.3k, 18.0% · /women/tops: 10.2k, 9.6%.

### Underperforming against peers

Peer medians for sub-categories with 100+ sessions: conversion 20.3%, bounce 27.6%, 0.73 product views per visit.

| Category (path) | Peer group | Sessions | Conversion vs peers | Bounce vs peers | Likely cause |
|---|---|---|---|---|---|
| /women/tops | sub | 10,249 | 9.6% vs 20.3% | 60.8% vs 27.6% | Dead end; shared cause |
| /women/pants | sub | 9,623 | 9.4% vs 20.3% | 61.1% vs 27.6% | Dead end; shared cause |
| /women/shorts | sub | 8,724 | 9.6% vs 20.3% | 61.6% vs 27.6% | Dead end; shared cause |
| /women/jeans | sub | 7,628 | 10.3% vs 20.3% | 61.8% vs 27.6% | Dead end; shared cause |
| /women/skirts | sub | 7,381 | 10.9% vs 20.3% | 62.8% vs 27.6% | Dead end; shared cause |
| Products under $25 | dynamic | 15,213 | 8.5% vs 16.6% | 59.2% vs 28.2% | Dead end (judged on bounce, not AOV) |

The pattern is shared, not category-specific: /men/tops converts at 20.9% and /men/pants at 18.0%, while the women's equivalents sit near 9.5% with double the bounce and an AOV of about $44 against about $100. Men's accessories and several kids' categories show the same pattern. Women's activewear, dresses and shoes are normal.

### Dynamic categories
- **Empty: "Back in Stock"** returns 0 products. Its only condition is `rating ≥ 40`, but ratings in the catalog run from 0 to 5. It also has no path, so it isn't in the navigation tree.
- **Thin: "Heritage"** has 16 products (trousers, a suit, bags, scarves and tops) and 6.3k sessions. Conversion is 21.0%, above the dynamic-category median, so it works, but the page is under one screen.
- **New:** "Beauty Trends" has no previous-period data.
- **Big swing:** "Formal Dresses" revenue +879% after its definition was edited during the period. Confirm the change before calling it a win.
- A test category ("test_yellow_color_products") gets 6.4k sessions.

### Rules
- 29 category ranking rules; 12 are disabled. "Summer Beauty Sale" on /health & beauty is **enabled but expired**, alongside another enabled rule on the same category.
- The enabled rule on /women/tops targets the "Casual Style" audience only. It pins 12 products and boosts activewear, but the default page doesn't use it. The list view showed no audience; `get_ranking_rule` did.
- One media rule ("Honeymoon Edit Campaign" on /women/shoes) is enabled but expired.
- No A/B test is running.

### Buried products (/women/tops, 748 products)
- Positions 1–3 are the same "Cropped Letter Hoodie" listed three times, and hoodies lead a "tops" page.
- One brand has 6 of the first 24 slots, which is every product it has in the category. Brands with 39, 30 and 30 products in the category have none in the first 24.
- No high-earning product is buried: the ranking follows revenue closely down to position 37.

### Recommended fixes
1. **Investigate the low-converting women's apparel cluster as one problem** (page template, pricing and assortment, tracking). Evidence: five sibling categories at about half the conversion and double the bounce of the men's equivalents. Impact: up to about $200k over 30 days (sum of visits × conversion gap to the 20.3% peer median × each category's AOV). Effort: medium. Check by: comparing pixel data and page templates for /women/tops and /men/tops.
2. **Fix the "Back in Stock" condition** (for example `rating ≥ 4.0`, or better, an in-stock or restock attribute) and add it to the navigation. Effort: low. Check by: the product grid returns products.
3. **Group the hoodie variants and add brand variety on /women/tops.** Bury duplicate titles and A/B test a brand-diversity ranking rule. Effort: medium. Check by: A/B test.
4. **Tidy expired rules**: disable "Summer Beauty Sale" and "Honeymoon Edit Campaign". Effort: low.
5. **Fix the category pixel on one men's collection page**, which sends the page URL as the category name with no category ID. Run `data-feed-health`. Effort: low.

**Data caveats:** account-level reporting (no sites). Demo traffic is partly synthetic.
