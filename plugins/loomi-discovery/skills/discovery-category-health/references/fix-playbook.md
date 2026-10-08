# Category fix playbook

This table matches the evidence from a category health check to the most likely fix. Choose the smallest fix that explains the evidence.

| Evidence | Likely cause | Fix | Effort / risk |
|---|---|---|---|
| A dynamic category returns 0 products | Its conditions match nothing (impossible value, wrong attribute, a brand or tag no longer in the feed) | **Correct the conditions**, or retire the category and redirect its links. Check the catalog values with the product grid's facets first | Low / low |
| A dynamic category returns fewer than about 24 products, and some don't fit its purpose | Conditions too narrow, or too loose in the wrong direction | **Tighten or widen the conditions** so the page fills at least one screen with on-theme products | Low / low |
| A dynamic category gets traffic but isn't in `list_categories` | It has no place in the category tree | **Add it to the navigation**, or check which campaign links point to it | Low / low |
| A test or demo category gets real traffic | A test page linked from live navigation or campaigns | **Remove the links**, or turn it into a real collection | Low / low |
| One department's categories all sit far below the same categories in other departments | A shared cause: assortment, price points, page template or tracking | **Investigate the department as a whole** before tuning single categories. Compare page templates and pixel data for both | Medium / low |
| Bounce far above peers; few product views per visit | The first screen doesn't match what shoppers expect | Add a **category ranking rule** that boosts the core product type and best sellers, and buries off-topic items | Medium / medium |
| The same title appears several times near the top | Variants (sizes, colours) listed as separate products | **Group variants** into one product in the feed (the lasting fix). Meanwhile, bury duplicates or boost a mix of brands with a ranking rule | Medium / low |
| Brands with many products in the category have none in the first 24 | Ranking concentrates on a few brands | **A/B test a ranking rule** that boosts those brands, or diversifies by brand | Medium / medium |
| Products ranked below 48 earn as much per visit as the top 24 | Ranking signals lag (new products, little traffic) or a rule holds them down | **Boost those products** for the category, or remove the rule that buries them. Check with the grid before and after | Low / medium |
| A rule pins products, and disabling it in the grid improves the first screen | An outdated pin or boost | **Edit or turn off** that rule | Low / medium |
| A ranking or media rule is enabled but expired, or several enabled rules target one category | Rule clutter that makes behaviour hard to predict | **Tidy up**: disable expired rules and merge overlapping ones | Low / low |
| A rule targets an audience | It applies only to that audience, so the default grid doesn't show it | **Check the audience rule separately** before judging the category's ranking | — |
| Product views and add-to-cart near peers, conversion low | After the click: price, stock, product page or checkout | **Not a category fix.** Hand it to the merchandising or product-page team, with the category and top product IDs | — |
| Revenue changed by several hundred percent between periods | The category's definition or tracking changed | **Confirm what changed** before reporting it as a win or loss | — |
| Category rows with a URL as the name, or a missing category ID | The category page pixel sends the wrong fields | **Fix the pixel** on those pages. Run the `data-feed-health` skill | Medium / low |

## Notes

- **Compare like with like.** Judge dynamic collections against other collections, and leaf categories against their siblings in other departments. Judge price-capped collections ("under $25") on bounce and conversion, not on order value.
- **Name categories by path.** Many names repeat across departments.
- **Preview before you recommend.** Where you can, show the effect of a fix in the product grid, for example by disabling a rule with `disabled_customization_ids`.
- **Prefer an A/B test for ranking changes** on high-traffic categories. Fixing an empty dynamic category can usually be applied directly, after confirmation.
