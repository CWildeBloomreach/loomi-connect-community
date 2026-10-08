# Example: an 8-week Q4 plan (illustrative)

**This example is partly illustrative.**
- The **calendar dates** are real, from `scripts/retail_dates.py` and the reference file.
- The **Discovery figures** are real, from a demo account shown here as `example_apparel` (account level, no sites). Its traffic is synthetic: every query grew about 80% period on period, so only the **baseline-adjusted** changes are meaningful.
- The **Engagement figures, segment names, campaign names and sizes are invented**. The method and the response shapes were checked against a live production project, but its figures aren't shown. The join between the two products is illustrative.

## Prompt

> What campaigns should we run over the next 8 weeks? We launch a gifting capsule on 2 November.

The user didn't name a market, so the plan uses the defaults (US, UK and EU) and says so.

## Output

## Campaign plan: US, UK, EU (default markets), 8 Oct to 3 Dec 2026

**Headline:** Black Friday to Cyber Monday is the biggest window by far (last year about 2× a normal week), and gifting searches are already rising. Start the gift-led sequence the week of 2 November. Nothing is planned for Black Friday week yet.
**Basis:** Engagement project "Example Retail – Production" (last year: 13 Oct to 7 Dec 2025); Discovery `example_apparel` (account level); calendar US, UK, EU. Markets not specified, so defaults used.
**Data notes:** Diwali 2026 is checked (8 Nov). No email or SMS campaigns in last year's window (only A/B split events), so outcomes are estimated from purchase uplift, not past campaigns. History covers all markets combined (single currency).

### Moments in the window
| Date | Moment | Market | Start promoting | Status |
|---|---|---|---|---|
| Sat 31 Oct | Halloween | Global | now (3 Oct) | computed |
| Mon 2 Nov | Gifting capsule launch | brand | — | brand |
| Thu 5 Nov | Bonfire Night | UK | 26 Oct | computed |
| Sun 8 Nov | Diwali | Global | 11 Oct | verified |
| Wed 11 Nov | Singles' Day; Veterans Day (US); St Martin (DE, NL) | Global / US / EU | 1 Nov | computed |
| Thu 26 Nov | Thanksgiving | US | 5 Nov | computed |
| Fri 27 Nov | Black Friday | Global | 30 Oct | computed |
| Sun 29 Nov | First Sunday of Advent | DE, NL | 15 Nov | computed |
| Mon 30 Nov | Cyber Monday | Global | 23 Nov | computed |
| Sat 5 Dec / Sun 6 Dec | Sinterklaas (NL) / Nikolaus (DE) | EU | 7 Nov / 22 Nov | computed |
| Fri 25 Dec | Christmas | Global | 30 Oct | computed |

Dropped as off-category: Columbus / Indigenous Peoples' Day, All Saints' Day.

### Ranked campaign ideas
1. **Black Friday early access to Cyber Monday**: Black Friday
   - Send window: VIP early access Mon 23 Nov → Black Friday 27 Nov → Cyber Monday last chance 30 Nov (teaser from 16 Nov)
   - Channel: email; SMS for the Cyber Monday last-chance message only, if SMS consent exists
   - Audience: "VIP – high CLV" segment, about 38,000 (about 31,000 reachable by email, as of 8 Oct 10:20 UTC)
   - Angle / offer: early access to the gifting capsule and jewellery, then sitewide
   - Evidence: last year the week of 24 Nov ran at index 2.3 and the following week at 2.0; the gifts category's share rose from 9% to 16% in those weeks. Now: "wedding band" +7.8% and "diamond" +2.5% above the search baseline
   - Expected outcome (estimate): no comparable past campaign. The target is a share of a week that ran at about 2.3× normal; measure against a 10% holdout
   - Clashes: none found; the week is empty
2. **Gifting capsule launch, then a Christmas gift guide**: brand launch + Christmas
   - Send window: launch Mon 2 Nov → gift guide Thu 12 Nov → "order by" reminder before the shipping cut-off (about 18 Dec)
   - Channel: email
   - Audience: "Engaged 90 days" segment, size not computed (run engagement-segment-builder)
   - Angle / offer: gifts by recipient and price band; jewellery leads
   - Evidence: last year Discovery's top-revenue categories in this window were jewellery (bracelets, necklaces, rings); now jewellery searches are steady and wedding-band searches are rising
   - Expected outcome (estimate): no comparable history
   - Clashes: the weekly newsletter (Thursdays) lands on 12 Nov. Fold the gift guide into it rather than adding a send
3. **Singles' Day 24-hour offer**: 11.11
   - Send window: teaser Mon 9 Nov → 11 Nov (one day)
   - Channel: email
   - Audience: "Lapsed 6–12 months", size not computed
   - Angle / offer: one-day offer on core lines
   - Evidence: last year Discovery revenue on 11 Nov was about 1.15× a typical day in that window (real figure). Engagement purchases showed no 11.11 lift (index 1.01 for that week)
   - Expected outcome (estimate): small; a reactivation test rather than a revenue driver
   - Clashes: the gifting launch sequence is the same week. Use a different audience
4. **Men's formalwear for party season**: Christmas parties
   - Send window: from 16 Nov
   - Channel: email
   - Audience: plain-English definition "bought menswear in the last 12 months", size not computed
   - Angle / offer: suits, trousers, collared shirts
   - Evidence: now "mens pants" is the strongest riser (+13.4% above the baseline, 14,372 → 29,456 sessions in 28 days); "formal trouser" and "collared shirt" are steady
   - Expected outcome (estimate): no comparable history
   - Clashes: none
5. **Diwali (late start)**: Diwali, 8 Nov
   - Send window: now → 8 Nov (the promotion should have started 11 Oct)
   - Channel: email
   - Audience: only if the brand has a relevant audience. Ask the user
   - Evidence: calendar only
   - Expected outcome (estimate): no history
   - Clashes: none

### Calendar check
- Gaps: Black Friday week and Cyber Monday have no planned sends.
- Busy weeks: none above 3 sends.
- Planned but not active: one draft "Holiday teaser" email with planned times on 19 and 26 Nov. It would clash with idea 1 if activated.

### Demand signals (28 days, baseline +80.7% in search sessions)
- Rising: menswear tailoring ("mens pants" +13.4%), bridal and fine jewellery ("wedding band" +7.8%, "diamond" +2.5%)
- Falling: summer lines ("shorts" −16.9%, "bermuda shorts" −13.6%, "distressed jeans" −11.3%). Don't push summer clearance without a strong offer
- Flag: "joggers" bounce rose from 37% to 52%, and conversion fell from 16.9% to 11.6%. Fix search before sending traffic (discovery-query-diagnosis)

### Next steps
- Build and size the "bought menswear in the last 12 months" audience: `engagement-segment-builder`
- Check send collisions for the weeks of 9 Nov and 23 Nov: `engagement-send-collision-check`
- Turn rising "wedding band" searches into a targeted campaign: `search-demand-to-campaign`
