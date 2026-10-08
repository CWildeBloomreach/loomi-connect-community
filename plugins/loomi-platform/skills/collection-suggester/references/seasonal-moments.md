# Seasonal collection ideas by moment and market

Read this in step 5 of the skill. It's a short list of collection ideas tied to retail moments, so suggestions can be timed. **For the full retail calendar by market, with exact dates, use the `campaign-planner` skill.** Dates below are typical and move from year to year; confirm them before you commit to a launch date.

## Choosing markets

- **No market given:** use **US, UK and EU** together and say so. Where a moment differs between them (Mother's Day, Father's Day, back to school), list each market's timing.
- **The user names a market:** use the rows for that market.
- **A market not listed here** (for example Australia, Japan, India, the Middle East): use the **Global** rows, say clearly that you have fallen back to global moments, and suggest the user checks local moments with the `campaign-planner` skill. Remember that in the southern hemisphere, summer falls in December–February.
- **EU** is not one calendar. Where countries differ, the row names the main ones.

## Lead time

Build a collection **4–6 weeks before** the moment: it needs time for the sync, navigation and ranking, and search demand usually starts rising 2–4 weeks before. In the output, put moments that start within the next 8 weeks first.

## Moments

| Moment | Markets and typical timing | Collection ideas | Rule ingredients to look for |
|---|---|---|---|
| New year, January sale | Global: 26 Dec – end of Jan (UK Boxing Day sales start 26 Dec) | Sale edit, "new year, new kit" activewear | `onSale = true`, activewear categories |
| Valentine's Day | US, UK, EU: 14 Feb | Gifts for her / him, red and pink edit, jewellery gifts | jewellery and accessory categories, `color IN (red, pink)`, price cap |
| Mother's Day | **UK:** Mothering Sunday, 3 weeks before Easter (March). **US:** 2nd Sunday of May. **EU:** mostly May (DE, IT, NL, BE: 2nd Sunday; ES, PT: 1st Sunday; FR: last Sunday of May, or early June) | Gifts for mum, jewellery, beauty sets, under-£40 / under-$50 / under-€50 gifts | jewellery, beauty, handbags; price cap in local currency |
| Easter, spring | Global: March–April (date moves) | Spring edit, pastels, kids' outfits | `season = spring` or `summer`, `color IN (pastels)` |
| Father's Day | **US, UK, FR:** 3rd Sunday of June. **DE:** Ascension Day (May). **IT, ES, PT:** 19 March | Gifts for dad, men's accessories, smart casual | men's accessories, belts, wallets, watches |
| Summer holiday | Northern hemisphere: June–August | Holiday edit, swim and beach, linen, sandals | `season = summer`, `material = Linen`, swimwear and shorts categories |
| Back to school | **US:** late July – August. **UK:** August – early September. **EU:** late August – September (varies by country) | School bags, kids' basics, student tech accessories | kids' categories, backpacks, price cap |
| Autumn / fall | Global (north): September–October | Layering, knitwear, boots | `season = winter` or `mid-season`, outerwear |
| Halloween | **US:** 31 Oct (strong). **UK:** growing. **EU:** limited | Costume-ready, black and orange edit | `color IN (black, orange)` |
| Singles' Day | 11 Nov: strong in parts of the EU and Asia, small in the US and UK | Deals edit | `onSale = true` |
| Black Friday / Cyber Monday | **US:** Friday after Thanksgiving (4th Thursday of Nov). **UK, EU:** same weekend, now standard | Doorbusters, best sellers on sale, gift deals | `onSale = true` with top sellers; price caps |
| Holiday party season | US, UK, EU: late November – December | Party dresses, sequins and metallics, formal menswear, party shoes and bags | `style = Formal`, `color IN (black, gold, silver, burgundy)`, dresses, suits, heels, clutches |
| Holiday gifting | US, UK, EU: mid November – 24 Dec | Gifts under $50 / £40 / €50, stocking fillers, gifts for him / her / kids | price cap in local currency, accessories, jewellery, beauty sets |
| Last-minute gifts | US, UK, EU: about 15–24 Dec | In-stock, fast-delivery gifts | in-stock attributes, gift categories |

## Global fallback moments

When a market isn't listed, use: New Year and January sales, Valentine's Day, local summer (check the hemisphere), back to school (check local term dates), Black Friday, year-end gifting and party season. Say that local moments such as Diwali, Ramadan and Eid, Lunar New Year or Golden Week are not covered here, and point to the `campaign-planner` skill.

## Matching a moment to the data

A seasonal idea is only worth suggesting if the account backs it up:

1. **Demand:** related queries are rising or were high in the same window last year. Last year's window comes from `get_discovery_query_performance` with explicit `start_date` and `end_date`.
2. **Stock:** a rule preview returns at least about 12 products from more than one brand.
3. **No duplicate:** no existing dynamic category already covers it (for example a "Valentine Premium Jewels" category that could be refreshed instead).

If demand exists but stock doesn't, list it under **assortment gaps**, not as a collection.
