# Valuing and ranking opportunities

Every figure here is an **estimate built on stated assumptions**, not a forecast. Show the assumptions every time. Replace the defaults with the user's own numbers (their AOV, past campaign conversion rates) whenever they have them.

## Inputs

- **Size:** the aggregate count for the pattern.
- **Reachable:** the count that can actually be messaged (contact property has value and, where consent is tracked, has consent). Measure it with one extra count per pattern (see check C3 in opportunity-patterns.md). If you skip it, say "reachability not measured".
- **Value per conversion:** the store AOV by default (30-day AOV query, pattern V in `winback-opportunity`), or a better figure for the pattern: average cart value for P6 (pattern V2 in `funnel-leak-finder`), the category's AOV for P1 and P5 (from Discovery `get_discovery_query_performance` for matching queries, or ask).
- **Response rate:** the share of the reachable audience expected to convert from one programme cycle.
- **Coverage:** none, inactive (a flow exists but is off or draft), partial (some of the group, or one channel), covered.

## Default response rates (assumptions)

| Pattern | Default | Value basis | Why |
|---|---|---|---|
| P1 Browsed category, never bought | 2% | category AOV | Cold-ish intent; browse-abandonment programmes typically convert in low single digits |
| P2 One-time buyer in repeat window | 5% | AOV | Second-purchase campaigns to recent buyers convert well; falls fast after the window |
| P3 VIP slowdown | 10% | AOV × 1.5 | High-value customers respond better; their orders are larger |
| P4 Discount-led | 10% shifted | AOV × discount depth | **Margin protected**, not revenue: the share moved to a smaller or no discount |
| P5 Affinity × trending | 3% | category AOV | Timely relevance lifts a standard category promotion |
| P6 Cart abandoners not contacted | 5% | average cart value | Typical recovery for a first abandonment email; × 4.3 for a monthly figure from a 7-day audience |
| P7 New, no second purchase | 8% | AOV | Early nurture to first-time buyers |
| P8 No consent | 10% capture | 12-month value of a messageable customer (default 0.5 × AOV) | **Long-term**: consent collected, not orders |

## Formulas

    value            = size × response rate × value per conversion × period multiplier
    reach            = reachable ÷ size
    reachable value  = value × (reach + (1 − reach) × on-site factor, if on-site is possible)
    score            = reachable value × coverage factor

- On-site factor (default 0.2): a web layer converts at roughly a fifth of an email's rate, but it reaches anonymous visitors. Use it for P1, P5 and P6, where many people aren't contactable. For P8, "reachable" is the share that can be shown a consent prompt (active on site in the last 30 days).
- Coverage factor: none 1.0, inactive 0.9, partial 0.5, covered 0.1. A covered group isn't worthless (the flow can be improved), but it isn't a new opportunity.
- Keep P4 (margin) and P8 (long-term) in the ranking but label them, so nobody adds them to revenue.
- Don't add up opportunities that overlap (P2 and P7 if their windows overlap, P1 and P5 for the same category). Say which overlap.

## Running the script

Save the inputs as JSON (format in the script's docstring) and run:

```bash
python3 scripts/rank_opportunities.py opportunities.json
```

It prints the ranked table with value, reachable share, coverage and notes. Without Python, calculate by hand and show the working for the top opportunity.

## Worked example (illustrative numbers)

P6, cart abandoners not contacted: 6,000 customers in 7 days, 300 with an email address (5%), average cart $110, no abandonment flow.

- Value = 6,000 × 5% × $110 × 4.3 = **$141,900 a month** if everyone could be reached.
- Reach = 5%; on-site share = 95% × 0.2 = 19%; reachable value = $141,900 × 24% ≈ **$34,000**.
- Score = $34,000 × 1.0 (uncovered).

P2, one-time buyers 31–90 days: 14,000 customers, 13,300 with an email (95%), AOV $95, no flow.

- Value = 14,000 × 5% × $95 = $66,500. Reachable value ≈ **$63,000** (no on-site share added). Score ≈ $63,000.

The cart audience refills every week and looks bigger, but so few of its members can be messaged that the one-time buyers come first. That's the point of ranking by value × reachability: say it in the verdict.

## Sanity checks

- If a pattern is empty, check each condition alone (`engagement-segment-builder`'s "count is zero" method) before calling it "no opportunity". In testing, empty results came from: no recent data (sandbox), category formats that differed between events, an identity gap between browsing and purchases, and consent not being recorded at all.
- If reachability is near zero for buyers, check the contact property (some projects store email only as an identifier, not a property: see `get_customer_schema`).
- Under about 100 customers, give the count but not a value.
