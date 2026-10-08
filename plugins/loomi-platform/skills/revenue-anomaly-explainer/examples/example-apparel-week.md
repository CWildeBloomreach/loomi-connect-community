# Example: why did revenue fall last week? (demo apparel account)

This example comes from a real read-only run on 8 October 2026 against a Bloomreach demo account, renamed `example_apparel`. The figures are the real figures from that run. The demo account's conversion rate (about 50%) is much higher than a real store's.

**Prompt:** "Revenue's down almost 4% on last week. Why?"

**Calls made (one at a time):** 3 headline cards, 3 device cards, 2 daily trends (7 and 28 days), 4 contributor tables (plus a `search="shirt"` query lookup), 2 ranking rule lists, the experiment list, 2 pixel health checks (168 h and 336 h), the catalog list and the catalog job list.

---

## Why revenue changed: example_apparel (account level), 30 Sep to 6 Oct vs 23 to 29 Sep

**Answer:** Revenue fell $297k (−3.7%). Fewer visits explain 78% of it, and two days (30 Sep and 6 Oct) account for 90%, compared with the two strongest days of the week before. The comparison week was unusually strong; jewellery searches and categories were also softer. No rule change, A/B test, tracking fault or feed failure explains the drop.

### The change, broken down
| | This period | Previous | Change | Share of change |
|---|---|---|---|---|
| Revenue | $7.63M | $7.93M | −$297k (−3.7%) | 100% |
| ↳ Traffic (visits) | 103.5k | 106.6k | −2.9% | −$231k (78%) |
| ↳ Conversion | 50.58% | 50.52% | +0.06 pts | +$8k (−3%) |
| ↳ Order value (AOV) | $145.75 | $147.14 | −0.9% | −$74k (25%) |

**By channel:** search −$126k (43%; traffic −$119k), category −$94k (32%; traffic −$83k), other −$77k (26%, approximate because search and category visits overlap)
**By device:** desktop −$187k (63%; mostly traffic), mobile −$87k (29%; conversion −0.8 pts cost $24k and AOV $23k), tablet −$22k (7%)
**When:** concentrated on 30 Sep (−$153k against 23 Sep) and 6 Oct (−$116k against 29 Sep): 90% of the drop. The change is about twice normal day-to-day variation. Over 28 days, 23 to 29 Sep averaged $1.133M a day against $1.106M for 9 to 22 Sep; this week averaged $1.090M.

**Biggest contributors**
- Queries (top 100 cover −$121k of the −$126k search drop): "diamond" −$34.9k (28% of search; traffic −$19.5k, AOV $354 → $341 −$15.5k); "dress" −$17.3k (conversion 22.2% → 21.3%); "pants" −$17.1k (conversion 21.6% → 20.1%); "bags" −$16.0k
- Categories (all 73 rows, which sum exactly to the category card): pacific specials −$16.7k (conversion); rings −$14.6k (traffic); heritage −$8.8k; bracelets −$8.6k. Risers: jewellery +$11.8k, activewear +$7.3k
- Brands: Pacific −$110k (37% of the total, in line with its share of revenue); Pacific Style −$73k (25%; visits 8,304 → 7,833)
- Products: the top 100 (of 6,631) cover only −$49k (17%) of the drop: products are a long tail. Largest single faller: Short Sleeve Polo Tennis Dress (−$13.1k, fewer visits)

### Likely causes (ranked)
1. **A strong comparison week.** Explains about $183k (62%): the previous week's revenue was $183k above what 7 days at the 9 to 22 Sep average would give. Evidence: 23 and 29 Sep were the two best days of that week, and the gap sits almost entirely on the matching days this week. Confidence: **Medium** (size and timing fit; no single event found on those dates). Next: check whether a promotion or email ran on 23 and 29 Sep (`engagement-campaign-digest`).
2. **Softer jewellery demand and lower diamond order values.** About −$50k across search and category ("diamond", rings, bracelets, necklaces, partly offset by the jewellery category). Evidence: "diamond" visits −4.7% and AOV −3.7%; rings visits −4.7%. No jewellery rule changed in the window. Confidence: **Medium**. Next: `discovery-query-diagnosis` on "diamond" (check whether high-price pieces dropped in the ranking), and `discovery-category-health` for rings.
3. **Mobile conversion slip.** −0.8 pts, about −$24k (8%). Evidence: desktop and tablet conversion rose; mobile pixel issue rates are normal. Confidence: **Low** (within normal variation for one week). Next: watch next week; if it persists, check mobile checkout.
4. **Two ranking rules on "shirt" edited on 25 Sep.** About −$9k (3%): "collared shirt" −$6.8k (bounce 20.5% → 24.9%) and "shirt women" −$2.6k (conversion 12.8% → 9.8%). The edit fell inside the comparison week, so most of both periods ran with it. Confidence: **Low**. Next: `discovery-query-diagnosis` on "shirt women"; review the rules with `discovery-rule-audit`.
5. **A scheduled category rule on tops started on 30 Sep (22:00 UTC).** Tops moved −$0.6k. Confidence: **Low**: negligible.

**Not explained by a specific cause:** about $30k (10%), seen as visits down about 3% evenly across devices, search and category. Causes 2 and 3 partly overlap with cause 1 (some of the jewellery and mobile shortfall falls on 30 Sep and 6 Oct), so treat the shares as approximate.

**Checked and ruled out**
- A/B tests: none started or ended since early August.
- Tracking: order pixel events 51,956 vs 53,061 the week before (−2.1%), in line with orders (−2.8%). The search page pixel flags 100% of events (`catalogs_required`) in both weeks: a standing problem, not a cause of this change.
- Catalog: every feed and index job in the last five days succeeded; 8,183 products throughout. The daily product feed warns about null values (standing).

**Caveats:** account-level reporting (no sites). The 28-day trend has a data gap: 12 Sep is missing, and 26 Aug to 7 Sep show no data, so longer comparisons need care. Measured Monday to Sunday (28 Sep to 4 Oct against 21 to 27 Sep), revenue was flat (−0.1%): the choice of window changes the story.
