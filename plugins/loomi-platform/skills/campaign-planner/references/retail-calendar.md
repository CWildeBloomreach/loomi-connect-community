# Retail calendar

Retail and cultural moments that campaigns are planned around, organised by market. Each moment has a **rule**, explicit dates for **2026 and 2027**, how far ahead to **start promoting**, and the **categories** it suits.

> **Owner should update yearly.** Every January, add next year's lunar and announced dates (Lunar New Year, Ramadan and the Eids, Diwali, Holi, Hanukkah, Amazon Prime Day events) to `LOOKUP` in `scripts/retail_dates.py`, regenerate the tables, and recheck anything marked "verify". Last full review: October 2026.

## How to read the dates

| Status | Meaning |
|---|---|
| *(no label)* | Computed from a fixed rule by `scripts/retail_dates.py`, e.g. "4th Thursday of November" or the Easter algorithm. Reliable. |
| **(verified)** | A lunar or announced date, checked against published sources in October 2026. |
| **(verify)** | Provisional. Islamic dates depend on moon sighting and can move by a day and differ between countries; some Hindu dates differ between regional calendars; retailer events can be moved. Check before committing a send date. |
| **look up** | Not known yet. Search for it, or ask the user, and label what you use "unverified". |

For any other year, run `python3 scripts/retail_dates.py --year <year> --market <codes>`. If this file and the script disagree, trust the rule, fix whichever is wrong, and note it in the PR.

**Start promoting** is a typical lead time for the first teaser or early-access send, not a rule. Most moments follow tease → launch → reminder → last chance. Gift moments also have a **shipping cut-off**, usually 3–7 days before the day, that should get its own "last order date" send.

## Adding a market

Adding a market is just adding a section:

1. Add a `## <CODE>` section below, with the same columns: moment, rule, 2026 and 2027 dates, start promoting, suits. Include public holidays that affect shopping (long weekends), the local Mother's and Father's Day, sales seasons (and whether they are regulated), back to school, and local shopping events.
2. Add the same moments to `M` (fixed rules) or `LOOKUP` (lunar or announced dates) in `scripts/retail_dates.py`, and add the code to `KNOWN_MARKETS`.
3. Mark anything you couldn't check against a primary source as "verify".
4. Open a pull request following [CONTRIBUTING.md](../../../../../CONTRIBUTING.md).

## Markets without a section

The skill still works for any market. It uses the **Global** moments, adds public holidays it can look up (with web search, if the client has it), **asks the user to confirm local shopping moments**, and labels all of those dates **"unverified"**. Watch for these differences:

- **Southern hemisphere** (for example AU, NZ, BR, ZA, AR): seasons are reversed. Summer sales fall around December and January, and back to school around late January and February. Don't recommend "winter coats for Black Friday".
- **Local Mother's and Father's Day** dates vary widely by country. Never assume the US date.
- **Fiscal-year-end sales** (for example end of June in AU) and **national shopping festivals** are often bigger than imported moments.
- **Black Friday and Singles' Day** are adopted to very different degrees. Check last year's evidence before leading with them.

## Global

Moments that apply in every market, though their weight varies by audience.

| Moment | Markets | Rule | 2026 | 2027 | Start promoting | Suits |
|---|---|---|---|---|---|---|
| Valentine's Day | GLOBAL | 14 February | Sat 14 Feb 2026 | Sun 14 Feb 2027 | 3 weeks before | jewellery, gifts, lingerie, fragrance, dining |
| Lunar New Year | GLOBAL | new moon between 21 Jan and 20 Feb (lunisolar) | Tue 17 Feb 2026 (verified) | Sat 06 Feb 2027 (verified) | 4 weeks before | gifts, red/gold apparel, food, travel; shipping cut-offs |
| International Women's Day | GLOBAL | 8 March | Sun 08 Mar 2026 | Mon 08 Mar 2027 | 2 weeks before | womenswear, beauty, purpose-led |
| Ramadan begins | GLOBAL | 1 Ramadan (moon sighting); about 11 days earlier each year | Wed 18 Feb 2026 (verify) | Mon 08 Feb 2027 (verify) | 3 weeks before | modest fashion, home, food, gifting for Eid |
| Eid al-Fitr | GLOBAL | 1 Shawwal (moon sighting) | Fri 20 Mar 2026 (verify) | Tue 09 Mar 2027 (verify) | 4 weeks before | new outfits, gifts, jewellery, home |
| Eid al-Adha | GLOBAL | 10 Dhu al-Hijjah (moon sighting) | Wed 27 May 2026 (verify) | Sun 16 May 2027 (verify) | 3 weeks before | apparel, gifts, travel |
| Holi | GLOBAL | Phalguna full moon (Hindu calendar) | Tue 03 Mar 2026 (verify) | Mon 22 Mar 2027 (verify) | 2 weeks before | white apparel, colour, beauty |
| Easter Sunday | GLOBAL | first Sunday after the paschal full moon (computed) | Sun 05 Apr 2026 | Sun 28 Mar 2027 | 3 weeks before | spring fashion, kids, confectionery, home |
| Halloween | GLOBAL | 31 October | Sat 31 Oct 2026 | Sun 31 Oct 2027 | 4 weeks before | costumes, kids, home decor, beauty |
| Diwali | GLOBAL | Kartika new moon (Hindu calendar; regional calendars can differ by a day) | Sun 08 Nov 2026 (verified) | Fri 29 Oct 2027 (verify) | 4 weeks before | jewellery, ethnic wear, home, gifts, electronics |
| Singles' Day (11.11) | GLOBAL | 11 November | Wed 11 Nov 2026 | Thu 11 Nov 2027 | 10 days before | everything, deep discounts; strongest in APAC, growing in EU |
| Black Friday | GLOBAL | day after US Thanksgiving (4th Thursday of November) | Fri 27 Nov 2026 | Fri 26 Nov 2027 | 4 weeks before | everything; electronics, fashion, beauty, home |
| Cyber Monday | GLOBAL | Monday after Black Friday | Mon 30 Nov 2026 | Mon 29 Nov 2027 | 7 days before | online-first offers, electronics, fashion |
| Hanukkah begins (evening) | GLOBAL | 25 Kislev (Hebrew calendar), 8 nights | Fri 04 Dec 2026 (verified) | Fri 24 Dec 2027 (verified) | 3 weeks before | gifts, home, kids |
| Double 12 (12.12) | GLOBAL | 12 December | Sat 12 Dec 2026 | Sun 12 Dec 2027 | 7 days before | last-chance holiday deals; APAC |
| Christmas Day | GLOBAL | 25 December | Fri 25 Dec 2026 | Sat 25 Dec 2027 | 8 weeks before | gifting across all categories; party wear |
| New Year's Eve | GLOBAL | 31 December | Thu 31 Dec 2026 | Fri 31 Dec 2027 | 2 weeks before | party wear, beauty, drinks |
| New Year / January reset | GLOBAL | 1 January | Thu 01 Jan 2026 | Fri 01 Jan 2027 | 7 days before | activewear, wellness, organisation, sale clearance |

## US

| Moment | Markets | Rule | 2026 | 2027 | Start promoting | Suits |
|---|---|---|---|---|---|---|
| Martin Luther King Jr. Day | US | 3rd Monday of January | Mon 19 Jan 2026 | Mon 18 Jan 2027 | 7 days before | long-weekend sales, winter clearance |
| Super Bowl Sunday | US | 2nd Sunday of February since 2022 (confirm each season) | Sun 08 Feb 2026 (verify) | Sun 14 Feb 2027 (verify) | 2 weeks before | TVs, snacks, team apparel, home |
| Presidents' Day | US | 3rd Monday of February | Mon 16 Feb 2026 | Mon 15 Feb 2027 | 7 days before | mattresses, furniture, appliances, winter clearance |
| Mother's Day (US, DE, NL, IT) | DE, IT, NL, US | 2nd Sunday of May | Sun 10 May 2026 | Sun 09 May 2027 | 3 weeks before | jewellery, flowers, beauty, apparel, gifts |
| Memorial Day | US | last Monday of May | Mon 25 May 2026 | Mon 31 May 2027 | 10 days before | summer kick-off, outdoor, furniture, apparel |
| Father's Day (US, UK, FR, NL) | FR, NL, UK, US | 3rd Sunday of June | Sun 21 Jun 2026 | Sun 20 Jun 2027 | 3 weeks before | menswear, grooming, tech, tools, outdoor |
| Amazon Prime Day (summer) | EU, UK, US | announced by Amazon, usually June or July | Tue 23 Jun 2026 (verify) | look up | 7 days before | counter-programme: electronics, home, fashion |
| Independence Day | US | 4 July | Sat 04 Jul 2026 | Sun 04 Jul 2027 | 10 days before | summer apparel, outdoor, BBQ, red/white/blue |
| Back to school (US peak start) | US | mid-July to Labor Day; peaks 2 weeks before local term | Wed 15 Jul 2026 | Thu 15 Jul 2027 | 3 weeks before | kids apparel, shoes, bags, stationery, laptops |
| Labor Day | US | 1st Monday of September | Mon 07 Sep 2026 | Mon 06 Sep 2027 | 10 days before | end-of-summer clearance, mattresses, appliances |
| Prime Big Deal Days (October) | EU, UK, US | announced by Amazon, usually early October | Tue 06 Oct 2026 (verified) | look up | 7 days before | early holiday deals, electronics, home |
| Columbus / Indigenous Peoples' Day | US | 2nd Monday of October | Mon 12 Oct 2026 | Mon 11 Oct 2027 | 7 days before | fall sales, outerwear |
| Veterans Day | US | 11 November | Wed 11 Nov 2026 | Thu 11 Nov 2027 | 7 days before | early holiday sales, mattresses, outdoor |
| Thanksgiving | US | 4th Thursday of November | Thu 26 Nov 2026 | Thu 25 Nov 2027 | 3 weeks before | home, hosting, food; launches Black Friday week |
| Small Business Saturday | US | Saturday after Thanksgiving | Sat 28 Nov 2026 | Sat 27 Nov 2027 | 7 days before | independent and local brands |
| Giving Tuesday | US | Tuesday after Thanksgiving | Tue 01 Dec 2026 | Tue 30 Nov 2027 | 7 days before | charity tie-ins, purpose-led |
| Green Monday | US | 2nd Monday of December | Mon 14 Dec 2026 | Mon 13 Dec 2027 | 7 days before | last reliable shipping for gifts |
| Super Saturday | US | last Saturday before Christmas | Sat 19 Dec 2026 | Sat 18 Dec 2027 | 7 days before | last-minute gifts, BOPIS, gift cards |

Notes: Black Friday week now runs from Thanksgiving week to Cyber Monday, and early "Black Friday" offers often start in early November. Amazon's two Prime events (summer and October) pull demand forward; counter-programme them rather than compete on price. Back to school varies by state: southern states start in early August, the north-east after Labor Day.


## UK

| Moment | Markets | Rule | 2026 | 2027 | Start promoting | Suits |
|---|---|---|---|---|---|---|
| New Year's Day bank holiday | UK | 1 January, or next weekday | Thu 01 Jan 2026 | Fri 01 Jan 2027 | 7 days before | January sales |
| Pancake Day (Shrove Tuesday) | UK | 47 days before Easter | Tue 17 Feb 2026 | Tue 09 Feb 2027 | 10 days before | food, kitchen |
| Mothering Sunday (UK) | UK | 4th Sunday of Lent (3 weeks before Easter) | Sun 15 Mar 2026 | Sun 07 Mar 2027 | 3 weeks before | flowers, jewellery, beauty, gifts |
| Good Friday bank holiday | UK | 2 days before Easter | Fri 03 Apr 2026 | Fri 26 Mar 2027 | 7 days before | Easter weekend sales, garden, DIY |
| Easter Monday bank holiday | UK | day after Easter (England, Wales, NI) | Mon 06 Apr 2026 | Mon 29 Mar 2027 | 7 days before | garden, DIY, spring fashion |
| Early May bank holiday | UK | 1st Monday of May | Mon 04 May 2026 | Mon 03 May 2027 | 7 days before | garden, outdoor, spring sales |
| Spring bank holiday | UK | last Monday of May | Mon 25 May 2026 | Mon 31 May 2027 | 7 days before | summer kick-off, garden, travel |
| Summer sales (UK, typical start) | UK | late June; most retailers start around the last week of June | Mon 29 Jun 2026 (verify) | Mon 28 Jun 2027 (verify) | 7 days before | fashion clearance, home |
| Back to school (UK) | UK | late July to early September (England term starts early Sep) | Sat 25 Jul 2026 | Sun 25 Jul 2027 | 4 weeks before | school uniform, shoes, bags, stationery |
| Summer bank holiday | UK | last Monday of August (England, Wales, NI) | Mon 31 Aug 2026 | Mon 30 Aug 2027 | 7 days before | end-of-summer sales, back to school |
| Bonfire Night | UK | 5 November | Thu 05 Nov 2026 | Fri 05 Nov 2027 | 10 days before | outerwear, home, food |
| Christmas Day bank holiday (observed) | UK | 25 December, or substitute weekday | Fri 25 Dec 2026 | Mon 27 Dec 2027 | 7 days before | store hours and delivery planning |
| Boxing Day (sales start) | UK | 26 December (bank holiday may be substituted) | Sat 26 Dec 2026 | Sun 26 Dec 2027 | 7 days before | biggest UK sale day; fashion, home, electronics |
| Boxing Day bank holiday (observed) | UK | 26 December, or substitute weekday | Mon 28 Dec 2026 | Tue 28 Dec 2027 | 7 days before | store hours and delivery planning |

Notes: bank holidays are for England and Wales (Northern Ireland adds 17 March and 12 July; Scotland has 2 January, St Andrew's Day on 30 November, and its summer bank holiday on the first Monday of August). Mothering Sunday is tied to Easter, so it moves every year and is **not** the US date. Father's Day is the same as the US. Black Friday is fully adopted in the UK; Boxing Day is the biggest sale day and many sales now start online on Christmas Eve or Christmas Day.


## EU

Black Friday and Cyber Monday (see Global) are widely adopted across the EU, on the US dates, and often stretch to a "Black Week". Prime Day events run in DE, FR, IT, ES and NL. Sales are **regulated** in some countries (FR fixed dates; IT dates set by region) and deregulated in others (DE, NL, ES by custom).

### Country differences that matter

| Moment | DE | FR | NL | ES | IT |
|---|---|---|---|---|---|
| Mother's Day | 2nd Sunday of May | last Sunday of May (1st of June if Pentecost) | 2nd Sunday of May | 1st Sunday of May | 2nd Sunday of May |
| Father's Day | Ascension Day (Vatertag) | 3rd Sunday of June | 3rd Sunday of June | 19 March | 19 March |
| Main gift day besides Christmas | Nikolaus (6 Dec) | — | Sinterklaas (5 Dec) | Reyes (6 Jan) | Befana (6 Jan) |
| Summer sales | by custom, late June/July | regulated, fixed dates | by custom | by custom, about 1 July | regional dates, usually early July |
| Back to school | August–September, by state | about 1 September | August–September, by region | early–mid September | mid-September, by region |

| Moment | Markets | Rule | 2026 | 2027 | Start promoting | Suits |
|---|---|---|---|---|---|---|
| Epiphany / Three Kings (ES Reyes, IT Befana) | ES, IT | 6 January | Tue 06 Jan 2026 | Wed 06 Jan 2027 | 3 weeks before | ES: the main gift day; IT: kids, sweets |
| Winter sales start (FR soldes) | FR | 2nd Wednesday of January, or 1st if the 2nd is after the 12th (some departments differ) | Wed 07 Jan 2026 | Wed 06 Jan 2027 | 7 days before | fashion, home clearance |
| Carnival / Rosenmontag (DE) | DE, ES, IT, NL | Monday 48 days before Easter | Mon 16 Feb 2026 | Mon 08 Feb 2027 | 2 weeks before | costumes, party, beauty |
| Father's Day (ES, IT) | ES, IT | 19 March (St Joseph) | Thu 19 Mar 2026 | Fri 19 Mar 2027 | 3 weeks before | menswear, grooming, gifts |
| King's Day (NL) | NL | 27 April, or 26 April when the 27th is a Sunday | Mon 27 Apr 2026 | Tue 27 Apr 2027 | 2 weeks before | orange apparel, party, outdoor |
| Labour Day (most of EU) | EU | 1 May | Fri 01 May 2026 | Sat 01 May 2027 | 7 days before | long weekend, spring sales |
| Mother's Day (ES) | ES | 1st Sunday of May | Sun 03 May 2026 | Sun 02 May 2027 | 3 weeks before | jewellery, beauty, gifts |
| Ascension Day / Vatertag (DE) | DE, EU | 39 days after Easter (public holiday in DE, FR, NL and others) | Thu 14 May 2026 | Thu 06 May 2027 | 2 weeks before | DE: menswear, outdoor, BBQ; elsewhere a long weekend |
| Fête des Mères (FR) | FR | last Sunday of May, or 1st Sunday of June if that clashes with Pentecost | Sun 31 May 2026 | Sun 30 May 2027 | 3 weeks before | jewellery, beauty, gifts |
| Whit Monday | DE, FR, NL | 50 days after Easter | Mon 25 May 2026 | Mon 17 May 2027 | 7 days before | long weekend, garden, travel |
| Summer sales start (FR soldes) | FR | last Wednesday of June, or the one before if after the 28th (some departments differ) | Wed 24 Jun 2026 | Wed 23 Jun 2027 | 7 days before | fashion, home clearance |
| Summer sales (ES, typical start) | ES | 1 July by custom (deregulated; many start earlier) | Wed 01 Jul 2026 (verify) | Thu 01 Jul 2027 (verify) | 7 days before | fashion clearance |
| Bastille Day (FR) | FR | 14 July | Tue 14 Jul 2026 | Wed 14 Jul 2027 | 7 days before | summer sales week, travel |
| Back to school (FR rentrée, DE/NL vary by region) | DE, EU, FR, NL | FR: about 1 September; DE/NL: staggered by region, August to September | Tue 01 Sep 2026 (verify) | Wed 01 Sep 2027 (verify) | 4 weeks before | school supplies, kids apparel, bags, laptops |
| German Unity Day (DE) | DE | 3 October | Sat 03 Oct 2026 | Sun 03 Oct 2027 | 7 days before | long weekend, autumn sales |
| All Saints' Day | DE, ES, FR, IT | 1 November (public holiday in FR, IT, ES and parts of DE) | Sun 01 Nov 2026 | Mon 01 Nov 2027 | 7 days before | long weekend, autumn |
| St Martin's Day (DE, NL) | DE, NL | 11 November | Wed 11 Nov 2026 | Thu 11 Nov 2027 | 7 days before | kids, lanterns, baking |
| First Sunday of Advent | DE, EU, NL | 4th Sunday before Christmas | Sun 29 Nov 2026 | Sun 28 Nov 2027 | 2 weeks before | advent calendars, Christmas decor, gifting start |
| Sinterklaas / pakjesavond (NL) | NL | 5 December | Sat 05 Dec 2026 | Sun 05 Dec 2027 | 4 weeks before | the main NL gift day: toys, gifts |
| Nikolaustag (DE) | DE | 6 December | Sun 06 Dec 2026 | Mon 06 Dec 2027 | 2 weeks before | small gifts, sweets, kids |
