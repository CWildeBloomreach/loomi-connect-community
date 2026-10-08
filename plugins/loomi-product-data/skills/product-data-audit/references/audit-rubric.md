# Product data audit rubric

Read this in steps 4–6 of the skill. `scripts/audit_products.py` applies these rules; if you can't run scripts, apply them by hand to a sample. The `product-data-enhancer` skill keeps its own copy of the same codes in `references/enhancement-rubric.md`. Keep the two consistent when you change either.

## Why each check matters

| Audience | What they need from product data |
|---|---|
| **SEO** (classic search engines, shopping listings) | A descriptive, unique title and description; correct price, availability and identifiers (GTIN, MPN, brand) for structured data and merchant listings; image alt text |
| **AEO** (featured snippets, voice, "answer" boxes) | Short, factual answers to the questions shoppers ask: fit, size, material, care, dimensions, compatibility |
| **GEO** (AI assistants, AI shopping answers) | Entity-rich, consistent facts an assistant can quote and compare: brand, product type, colour, material, size, key features. Conflicting or vague data makes an assistant skip or misdescribe the product |
| **Your own site search** | The words shoppers actually type, in the title, description and attributes |

## Scoring

Every product starts at **100** and loses points for each gap found. Bands: **good** 80+, **fair** 60–79, **poor** under 60.

### Title (T)

| Code | Gap | Points | Rule |
|---|---|---|---|
| T1 | Too short or too long | 8 | Under 25 or over 150 characters. 150 is the usual shopping-feed limit; 50–110 reads well in results |
| T2 | No product type | 6 | No product-type noun ("joggers", "necklace", "bronzer") in the title. Names like "Halo" or "Divine" alone don't say what the product is |
| T3 | Brand not in title | 3 | A brand is known but missing from the title. Skip for a store's own label if the user says so |
| T4 | Colour not in title | 3 | Apparel, footwear and bags only, when a specific colour is known |
| T5 | Promo words, shouting or repetition | 5 | "sale", "best price", "free shipping", ALL CAPS, or the same word three times |

### Description (D)

| Code | Gap | Points | Rule |
|---|---|---|---|
| D1 | No description | 15 | Empty after removing HTML |
| D1s | Thin description | 10 | Fewer than 150 characters of text |
| D2 | Boilerplate | 8 | With the product's own title and brand removed, the same text is shared by at least 5 products (or 1% of those audited). Typical: "Buy <title> online, buy <type> at best price" |
| D3 | Only repeats the title | 6 | Fewer than 8 words that aren't in the title or brand |
| D4 | Keyword-stuffed | 8 | "buy … online", "at best price", or long comma lists of keywords |
| D5 | Raw HTML or entities | 2 | Tags or `&nbsp;` in the text. Fine on your own site if rendered, but it leaks into feeds and AI answers |
| D6 | Claims to verify | 3 | "sustainable", "organic", "waterproof", "hypoallergenic", "SPF", "clinically", "rated 4.8 stars" and similar. Not necessarily wrong; a person must confirm each one |

### Attributes (A)

Expected attributes depend on the vertical, worked out from the category label or the product-type word in the title:

| Vertical | Required (A1, 5 points each, up to 15) | Recommended (A1r, 2 points each, up to 6) |
|---|---|---|
| Apparel | colour, material, size, gender (a "Men"/"Women" title counts) | fit, pattern, care |
| Footwear | colour, material, size, gender | — |
| Jewellery | material (metal), colour | dimensions (length, diameter) |
| Beauty | — | shade (colour), size or volume |
| Bags | colour, material | dimensions |
| Home | colour, material, dimensions | — |
| Electronics | MPN or model | dimensions |
| Other | — | colour, material |

| Code | Gap | Points | Rule |
|---|---|---|---|
| A2 | Vague value | 4 | Every colour value is vague: "multi", "light", "medium", "dark", "other", "NA" |
| A3 | Conflict | 6 each | The title names a colour the colour field doesn't contain (title "navy", field "black"), or the description names a different catalog brand from the brand field |
| A3x | Only in the description | 3 | A material (cotton, viscose, leather …) appears in the description but the material field is empty. Easy win: copy it into the attribute |

### Identifiers and offer (S)

| Code | Gap | Points | Rule |
|---|---|---|---|
| S1 | No GTIN or MPN | 4 | Neither identifier present. If no product has one, report it once as a catalog-wide gap |
| S2 | Price problem | 6 | No price, or sale price above the regular price |
| S3 | No availability | 3 | Only when other products have an availability field |

### Images (I) — text-only

The audit counts image URLs; it never opens images. Looking at images is the enhancer's job.

| Code | Gap | Points | Rule |
|---|---|---|---|
| I1 | No image | 15 | No image URL in any image field |
| I2 | Only one image | 2 | Only when other products have several (`large_image` lists) |
| I3 | No alt text | 2 | Only when the catalog has an alt-text field at all; otherwise report "no alt-text field" once |

### Shopper vocabulary (V)

| Code | Gap | Points | Rule |
|---|---|---|---|
| V1 | Not the words shoppers use | 5 | The title uses one term of a synonym group ("trousers") while shoppers search another at least twice as often ("pants"), and that term appears nowhere in the title or description |

Default groups: trousers/pants; joggers/track pants/sweatpants; sneakers/trainers; t-shirt/tee; hoodie/sweatshirt; jumper/sweater/pullover; necklace/pendant/chain; earrings/studs; sofa/couch; handbag/purse; moisturizer/moisturiser/face cream; blazer/sport coat; vest/waistcoat/tank top. Add account-specific groups with `--synonyms`, for example from the account's own user synonyms (`list_synonyms_user`).

## Catalog-wide signals

Report these once, not per product:

- **Inconsistent values:** the same colour spelled two ways ("grey"/"gray", "navy"/"navy blue"), brand names with trailing spaces, vague colour values. Facets and filters split, and AI assistants see two different products.
- **Fields absent everywhere:** no GTIN/MPN, no alt-text field, no availability.
- **Field misuse:** values that belong elsewhere, such as skincare ingredients in `material` or shade words ("light") in `colors`. Spot these in the facet call (step 2) and name them.
- **Boilerplate templates:** how many products share each template, with the first words of it.
- **Fill rates from facets:** a facet's counts summed against `numFound` give a rough fill rate (for example material values on about half the catalog). Facets count variants for some fields and are truncated to the top values, so call it approximate.

## Commercial weighting

- **Importance** = 0.6 × the product's revenue percentile + 0.4 × its visits percentile, from `get_discovery_product_performance_table` for the chosen window. Products missing from the table had no views: importance 0.
- **Priority** = (100 − score) × (0.2 + importance). A poor product with no traffic still ranks, but below a fair product that earns a lot.
- A product with **no views and poor data** may be invisible *because* of its data (no product type in the title, no category words). Call these out separately rather than letting them sink.

## Per-product result lines (JSONL)

With `--jsonl`, the script writes one JSON object per line, one line per product:

| Field | Meaning |
|---|---|
| `schema`, `version` | `"loomi-product-audit"`, `"1"` |
| `pid` | The catalog's stable product ID |
| `title`, `category`, `vertical` | As read; `category` is the file label, or the vertical if no label was given |
| `score` | 0–100 after deductions |
| `importance`, `priority` | As defined above |
| `revenue`, `visits`, `in_performance_report` | From the performance table for the window |
| `gaps` | `[{"code": "D2", "gap": "boilerplate description …", "detail": "template shared by 412 products"}]` |

Files from several runs can be concatenated. If a product appears in more than one, keep the latest run's line.

## Reading the results

- Lead with the 3–5 most common gaps and the revenue on the products affected.
- Name the categories with the lowest average score weighted by revenue.
- Separate quick wins (A3x: copy from description; D5: strip HTML; A2: replace vague colours) from work that needs content writing (D1–D4) or a person with the product in hand (missing material, care, dimensions).
- The score is a triage tool, not a grade. Say so.
