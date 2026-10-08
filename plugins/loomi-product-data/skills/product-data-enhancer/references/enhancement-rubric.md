# Enhancement rubric and writing guide

Read this before step 5 of the skill. The gap codes are the same as in `product-data-audit` (its `references/audit-rubric.md`), so a product flagged there can be fixed here. Keep the two consistent when you change either.

## 1. Gap codes (shared with the audit)

| Code | Gap | Fix here |
|---|---|---|
| T1–T5 | Title too short or long, no product type, brand or colour missing, promo words or repetition | New title (section 3) |
| D1, D1s | No or thin description | Meta description, long description and bullets |
| D2, D3, D4 | Boilerplate, title repeated, keyword stuffing | Replace with product-specific text |
| D5 | Raw HTML or entities | Clean text version |
| D6 | Claims to verify | `needs a human` for each claim, unless the data proves it |
| A1, A1r | Missing required or recommended attribute | Fill from data, image or a person |
| A2 | Vague value ("multi", "light") | Specific value, from image or a person |
| A3 | Conflict (title vs. attribute, brand vs. description, data vs. image) | Flag with `conflict: true`, high priority |
| A3x | Attribute only in the description | Copy into the attribute (`from data`) |
| S1–S3 | No GTIN/MPN, price problem, no availability | `needs a human` (identifiers can't be guessed) |
| I1–I3 | No image, one image, no alt text | Alt text per image; note missing images |
| V1 | Not the words shoppers search | Work the shopper's term into the description, bullets or `search_terms` |

## 2. Sources, confidence and priority

| Source | Use when | Confidence |
|---|---|---|
| `from data` | The value is in the product's own data: an attribute, the title, the description, the category | high, or medium when you reworded or inferred lightly (e.g. "Men" in the title → gender men) |
| `seen in image` | You looked at the image and it clearly shows it | **high**: unmistakable (a black side stripe); **medium**: visible but small or partly hidden; **low**: plausible but uncertain (lighting, AI-generated image). Prefer `needs a human` over low |
| `from shopper searches` | The term comes from Discovery query performance or synonyms, and it describes this product truthfully | medium |
| `needs a human` | Anything not in the data and not clearly visible: fibre content, care, dimensions, GTIN/MPN, certifications, origin, claims | — (write the question to ask) |

**Priority:**

- **high**: conflicts (A3), wrong facts, missing required attributes on a product with revenue, titles without a product type, boilerplate or stuffed descriptions;
- **medium**: missing recommended attributes, thin descriptions, alt text, AEO and GEO content;
- **low**: style improvements, extra search terms, nice-to-have attributes.

## 3. Titles

Aim for 50–110 characters (150 at most). Lead with what the shopper needs to recognise the product. Use the user's brand style if they give one. Patterns by vertical (leave out parts you don't know; never invent them):

| Vertical | Pattern | Example (invented) |
|---|---|---|
| Apparel | Brand + Gender + Colour + Material + Product type + Key feature + Fit | Northwind Men's Grey Melange Joggers with Side Stripe, Regular Fit |
| Footwear | Brand + Gender + Product type + Colour + Material + Key feature | Fernhill Women's Black Leather Chelsea Boots, Block Heel |
| Jewellery | Brand + Name + Product type + Metal + Stone + Size | Lumen Halo Pendant Necklace, 18K White Gold, 44 cm Chain |
| Beauty | Brand + Product name + Product type + Shade + Size | Petalwise Glow Cream Bronzer, Shade Sunlit, 8 g |
| Home | Brand + Product type + Material + Colour + Dimensions | Oakhurst Round Side Table, Solid Oak, 50 cm |
| Electronics | Brand + Product line + Model + Product type + Key spec | (brand) (line) (model) Wireless Earbuds, 30 h Battery |

Don'ts: promo words ("sale", "best"), ALL CAPS, repeated keywords, competitor names, claims the data doesn't support, internal codes nobody searches for.

## 4. Descriptions and bullets

- **Meta description**: 120–160 characters. What it is, who it's for, two or three distinguishing facts. No "Buy … online at best price".
- **Long description**: 60–150 words, product-specific, in the brand voice. Facts first (what it is, material, fit, features), then use (when or how to wear or use it). One shopper search term woven in naturally, not stuffed.
- **Bullets**: 3–6 short facts a shopper scans for: material, fit, key features, care, size or dimensions. Only facts with a `from data` or `seen in image` source.
- If the current description holds facts (material, care, model height and size worn), keep them and move them into attributes as well (A3x).

## 5. Image alt text

One per image, up to 125 characters. Describe what the image shows for someone who can't see it: product type, colour, key visible features, and the view ("front view", "worn by a model", "close-up of the clasp"). Don't start with "Image of". Don't stuff keywords. Only from an image you actually viewed.

## 6. AEO: shopper questions

3–6 questions a shopper would ask about this product (or ask a voice assistant), each with a short, factual answer of one or two sentences:

- Base them on the product type and on real queries ("are … stretchy", "what size …", "how long is the chain").
- Answer **only from verifiable facts** (`from data` or clearly `seen in image`). If the answer isn't known, either drop the question or make it a `needs a human` item ("What is the fabric composition?").
- No medical, safety or performance claims.
- FAQPage markup gets limited rich results in Google today; the value is mainly in the page content and in AI answers. The script emits FAQPage markup only with `--faq-jsonld`.

## 7. GEO: AI-quotable summary and comparison attributes

- **Summary**: one or two plain sentences an AI assistant could quote: brand, product type, key attributes, price, availability, standout features. Entity-rich (named brand, named material, specific numbers), no marketing adjectives, no claims.
- **Comparison attributes**: a small object of normalised, comparable facts: `{"product_type": "joggers", "colour": "grey melange", "fit": "regular", "waist": "drawstring", "price": "34 USD"}`. Use consistent value names across products in the batch, so an assistant can compare them.
- Consistency matters more than length: one colour name across title, attribute, alt text and summary.

## 8. SEO: schema.org Product JSON-LD

The script builds it from the line's `known` values. Include only known values:

- `name`, `description`, `image`, `sku`, `brand` (`{"@type": "Brand", "name": …}`), `gtin8/12/13/14` (validated), `mpn`, `color`, `material`, `size`, `category`, `url`;
- `offers`: `Offer` with `price` (the price the shopper pays now), `priceCurrency`, `availability` (`https://schema.org/InStock` …), `url`;
- `aggregateRating` **only** if real ratings are shown on the page (`--include-ratings`);
- never: invented identifiers, guessed availability, image-only values, internal fields.

The markup must match what's visible on the product page, so it's meant to be applied together with the content changes after review.

## 9. Hard rules

1. **Never invent facts.** Materials, fibre percentages, certifications, dimensions, weights, origins, and claims such as "sustainable", "organic", "waterproof", "hypoallergenic" or "non-toxic": if they're not in the data and not clearly visible, they're `needs a human`.
2. **No medical or safety claims**: nothing that says a product treats, heals, prevents, protects (UV, SPF) or is safe for babies or allergies, even if the current copy says so. Flag the existing claim for review instead.
3. **Respect the brand voice** if the user supplies one; otherwise plain, factual and friendly.
4. **No competitor names** in any suggestion. Pass the user's list to the script with `--banned-terms`.
5. **Everything is a suggestion** for human review. Nothing is written to any catalog.
6. **Conflicts are flagged, not resolved**: give both values and let a person decide.
7. **Ratings and reviews**: don't quote a rating ("rated 4.8 stars") in descriptions; it goes stale and must match the page.
