# Example: "mens belt" brand boost test (demo apparel account)

The account name has been changed to a placeholder. The checks, figures and preview come from a real read-only run against a demo account. **No writes were made.** The plan stops at the confirmation step, and the IDs in the payloads are placeholders.

**Prompt:** "For 'mens belt', I want to boost Tommy Hilfiger and Pacific and bury the duplicate listings. Can we A/B test that before it goes live?"

**Pre-flight checks:** no experiments are running. No ranking rule exists for "mens belt", and none applies in the live grid, so this is **Pattern 1** (rule vs default). The account has no sites, so everything runs at account level.

## A/B test plan: "mens belt" (example_apparel, account level)

**Why:** "mens belt" had 14,790 visits in the last 90 days. It converts at 10.5%, with 63% bounce and $4.83 revenue per visit. The general query "belt" converts at 21.3% with $27.08 per visit. Of 154 results, Tommy Hilfiger has 25 matching products and Pacific has 27. Yet no Tommy Hilfiger belt makes the top 24 (the best is at position 36), and Pacific has only one (position 10). The top 24 has 8 United Colors of Benetton listings, and one Benetton title appears 8 times across the full results.

**Rule (created disabled):** "TEST mens belt - boost TH and Pacific, bury duplicates"
- Applies to: "mens belt" (exact match)
- Boost: brand = Tommy Hilfiger, Pacific; strength 40/100
- Bury: 27 duplicate listings (every repeat of a title after its first appearance)

```json
{
  "account_name": "example_apparel",
  "name": "TEST mens belt - boost TH and Pacific, bury duplicates",
  "enabled": false,
  "queries": [{"query": "mens belt", "queryType": "sitesearch", "matchType": "EXACT_MATCH"}],
  "attribute_boost_bury": [
    {"name": "brand", "strength": 40, "type": "boost", "values": ["Tommy Hilfiger", "Pacific"]},
    {"name": "omni_score_atc_decayed", "strength": 0, "type": "boost"},
    {"name": "omni_score_conv_decayed", "strength": 0, "type": "boost"},
    {"name": "omni_score_revenue_decayed", "strength": 0, "type": "boost"},
    {"name": "omni_score_views_decayed", "strength": 0, "type": "boost"}
  ],
  "bury_product_ids": ["<27 product IDs from simulate_rerank.py>"]
}
```

**Preview (strongest case, from `scripts/simulate_rerank.py`):**
- Brand mix in the top 24 before: Benetton 8, BuckleUp 4, USPA 2, Swiss Military 2, Canary London 2, six others 1 each (including Pacific).
- After: Pacific 12, Tommy Hilfiger 12.

| New | Was | Brand | Title |
|---|---|---|---|
| 1 | 10 | Pacific | Pacific Gold Men Black Solid Belt |
| 2 | 28 | Pacific | Pacific Gold Men Black Solid Leather Belt |
| 3 | 36 | Tommy Hilfiger | Tommy Hilfiger Men Black Leather Solid Belt |
| 4 | 38 | Tommy Hilfiger | Tommy Hilfiger Men Black Solid Genuine Leather Belt |
| 5 | 47 | Pacific | Pacific Gold Men Brown Belt |

A hard sort leaves no room for other brands on the first page. A strength of 40, rather than 100, should keep some of today's best sellers in the mix. The Pacific brand also includes a wallet-and-belt set and a gift set, near the bottom of the results today. Watch that the boost doesn't lift them.

**Experiment (created as a draft):** "Search terms - mens belt"; Control (default ranking) 50%, "Brand boost" (new rule) 50%; 100% of traffic; success metric RPV.

```json
{
  "account_name": "example_apparel",
  "name": "Search terms - mens belt",
  "traffic_percentage": 100,
  "success_metric": "RPV",
  "note": "Boost Tommy Hilfiger and Pacific, bury duplicate listings",
  "buckets": [
    {"bucket_name": "Control", "traffic_percentage": 50, "control": true},
    {"bucket_name": "Brand boost", "traffic_percentage": 50, "control": false, "customization_id": "<rule ID from write 1>"}
  ]
}
```

**Duration (from `scripts/estimate_duration.py`):** about 82 visits per bucket per day.

| Lift to detect | Days |
|---|---|
| +20% conversion | about 45 |
| +10% conversion | about 170 |

Because "mens belt" converts at half the rate of "belt", a +20% target is realistic. Plan **7 weeks**, and read it out at the end, not before.

**Writes, each needing your "yes":**
1. Create the rule, disabled (no live effect)
2. Create the experiment as a draft (no live effect)
3. Start the experiment (LIVE: half of "mens belt" shoppers see the new ranking)

Shall I create the rule (disabled)?
