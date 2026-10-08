# Example: did the Halloween kids tops rule work? (demo apparel account)

This example comes from a real read-only run on 8 October 2026 against a Bloomreach demo Discovery account with no sites, renamed `example_apparel`. The figures are the real figures from that run. The demo account's conversion rates are higher than a real store's.

**Prompt:** "We changed some merchandising rules recently. Did any of them work?"

**Calls made (one at a time, 14 in all):** site search and category ranking rule lists (sorted by `lastModifiedAt`), user synonyms, two `get_ranking_rule` lookups, the 45-day search trend (for data gaps), the category trend with the exact windows, query performance (`search="long dress"`, `search="shirt"`), the category table and category card for the windows, the same two again for the placebo windows, one category product grid call, two product table lookups, and the experiment list.

## Step 2: recent changes found (shown to the user to choose from)

1. **Category ranking rule "Halloween Kids top rule"** on kids tops (category 30100). Created 24 Sep, but **scheduled**: `startedAt` 30 Sep 22:00 UTC, ends 31 Oct. Its `lastModifiedAt` is still 24 Sep, so a list sorted by edit date alone would date it wrongly.
2. Two ranking rules on "shirt", edited 25 Sep. Both target an **audience** ("High Value"), so account-level numbers would dilute any effect, and the edit's content isn't recoverable. "shirt" (exact match) had only 95 visits in 11 days.
3. "Linen boost" on "long dresses", created 15 Sep. `get_discovery_query_performance` with `search="long dress"` returned **no rows**: nobody searches that exact wording, so it can't be measured. The before window would also have hit a data gap (26 Aug to 7 Sep and 12 Sep have no data).
4. The newest user synonym was last edited in April 2026: too old to measure against recent data.

The user picked the Halloween rule.

## Step 3: does it fire?

Product grid, `search_by="category"`, `query="30100"`: the rule ID is in `customizations_priority.value.ranking` and in `customizations.explain` (with its start and end times). "Kids Girls Yellow Printed Top" is first with `merchandisingRulesApplied.hardBoost`, and "CACA CINA Girls Red Georgette Polka Dot Top" sits at slot 3 with `productSlot: true`. **It fires.**

## Step 6: script input and output

Change day: 30 Sep (went live at 22:00 UTC, so 30 Sep was almost all "before", but it's excluded anyway). Data ends 6 Oct, so the after window is 1 to 6 Oct (6 days) and the before window 24 to 29 Sep. The category trend for these dates returned exactly those 12 `cdate`s, and its daily values summed to the card.

`change.json`:

```json
{"change": "Category ranking rule 'Halloween Kids top rule' on kids tops (30100): boosts one product to the top and pins one to slot 3. Scheduled; started 30 Sep 22:00 UTC",
 "metric": "revenue", "days_before": 6, "days_after": 6,
 "window_before": "24-29 Sep 2026", "window_after": "1-6 Oct 2026", "aov_cv": 1.0,
 "treated": {"label": "kids tops (30100)",
             "before": {"visits": 1370, "orders": 157, "revenue": "$6964.00"},
             "after": {"visits": 1358, "orders": 144, "revenue": "$6471.00"}},
 "controls": [
   {"label": "all category pages, excluding kids tops", "subtract_treated": true,
    "before": {"visits": 63425, "orders": 20107, "revenue": "$2602615.00"},
    "after": {"visits": 62589, "orders": 19695, "revenue": "$2559335.00"}},
   {"label": "men's and women's tops (10100 + 20100)",
    "before": {"visits": 3624, "orders": 532, "revenue": 34507},
    "after": {"visits": 3681, "orders": 518, "revenue": 32901}}]}
```

The placebo file used 18 to 23 Sep against 24 to 29 Sep (both before the rule started).

`python3 scripts/did_effect.py change.json --placebo placebo.json`:

```
DIFFERENCE-IN-DIFFERENCES vs control: all category pages, excluding kids tops
  metric                 treated   control    effect   95% range          p
  Visits                   -0.9%     -1.3%     +0.5%     -6.9% to +8.4%    0.906
  Orders                   -8.3%     -2.0%     -6.4%    -25.4% to +17.4%   0.567
  Revenue                  -7.1%     -1.6%     -5.5%    -31.5% to +30.2%   0.729
  Conversion rate          -7.5%     -0.7%     -6.8%    -24.8% to +15.4%   0.517
  Revenue per visit        -6.3%     -0.3%     -6.0%    -31.2% to +28.5%   0.700
  Order value (AOV)        +1.3%     +0.4%     +0.9%    -19.6% to +26.7%   0.935

DIFFERENCE-IN-DIFFERENCES vs control: men's and women's tops (10100 + 20100)
  Revenue                  -7.1%     -4.7%     -2.5%    -32.2% to +40.1%   0.889
  ...
CONVERSION NOISE CHECK (treated, two-proportion z-test, before vs after)
  11.46% -> 10.60% (-0.86 pts, range -3.21 to +1.50); z = -0.71, p = 0.4755
REVENUE IMPACT (vs first control)
  Per 30 days: -$1.9k (range -$14.9k to +$7.5k)
PLACEBO: Revenue -2.3% (range -28.9% to +34.1%): clean
VERDICT: TOO EARLY TO TELL
```

---

## Did it work? Halloween kids tops ranking rule

**Verdict: Too early to tell.** Kids tops revenue is down 5.5% against other category pages, but the 95% range (−32% to +30%) is far too wide to separate that from noise after 6 days and about 150 orders.

**The change:** category ranking rule "Halloween Kids top rule" on kids tops (30100): boosts "Kids Girls Yellow Printed Top" to the top and pins "CACA CINA Girls Red Georgette Polka Dot Top" to slot 3. Scheduled; live from 30 Sep 22:00 UTC to 31 Oct. **Fires:** yes, both products are in place in today's grid.
**Windows:** 24 to 29 Sep vs 1 to 6 Oct (6 days each; 30 Sep excluded). No data gaps.

| | Before | After | Change | Control change | Effect (DiD) | 95% range |
|---|---|---|---|---|---|---|
| Visits | 1,370 | 1,358 | −0.9% | −1.3% | +0.5% | −7% to +8% |
| Conversion rate | 11.46% | 10.60% | −7.5% | −0.7% | −6.8% | −25% to +15% |
| Revenue | $6,964 | $6,471 | −7.1% | −1.6% | −5.5% | −32% to +30% |
| Revenue per visit | $5.08 | $4.77 | −6.3% | −0.3% | −6.0% | −31% to +29% |

**Control:** all other category pages (the category card minus kids tops). Second control, men's and women's tops: −2.5% (range −32% to +40%). Both point the same way, both are inconclusive.
**Noise check:** conversion 11.46% → 10.60%, p = 0.48 (within noise). Placebo (18 to 23 Sep vs 24 to 29 Sep): −2.3%, range includes zero, so the control tracked kids tops before the change. With this much data, only revenue changes larger than about 58% could be reliably detected (the script's `detectable_pct`).
**Revenue impact:** about −$1.9k a month (range −$15k to +$7.5k): small either way, because the whole category makes about $32k a month.
**Product check:** the boosted top had 45 product visits against 64 (−30%) and the pinned top 41 against 45. Both are tiny numbers, and these counts are site-wide, not just from this category.
**Caveats:** Halloween demand for kids tops should rise through October regardless of the rule, which the site-wide control doesn't remove; 6-day windows (not whole weeks); account-level reporting (no sites); no A/B test or other rule on this category started in either window.
**Next steps:** re-run on 16 October with 14-day windows (1 to 14 Oct vs 16 to 29 Sep). The rule ends on 31 Oct, so if a clean answer matters for next year, A/B test it now with `discovery-experiment-setup`: observational data on a category this size won't detect a realistic effect of 5–10%.
