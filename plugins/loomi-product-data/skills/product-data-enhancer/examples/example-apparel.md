# Example: product data suggestions (illustrative)

**Illustrative only.** The account, products, brands, URLs and numbers are invented. The joggers finding mirrors what the image check found on a real demo product: a title that says "Solid" on a product with a contrast stripe, and a vague "multi" colour. The matching input file is [example-suggestions.jsonl](example-suggestions.jsonl).

**Prompt:** "Improve the product data for EX-1001 and EX-2002 for SEO and AI search. Plain, friendly voice. Prices are in USD."

**Calls made (one at a time):** the product grid by product ID and `search_discovery_catalog_products` for each product; `get_discovery_query_performance` for "joggers" and for "necklace"; `list_synonyms_user`. Images: EX-1001's main image downloaded to a temporary folder and viewed; EX-2002's image host refused the download (HTTP 403), so it's text-only. One line per product appended to `suggestions_example_apparel_2026-10-08.jsonl`, then `scripts/suggestions_to_files.py`.

## Product data suggestions: example_apparel, 2 products (batch 1 of 1)

Images: viewed for EX-1001 (downloaded and viewed); **NOT viewed for EX-2002: text-only suggestions** (download refused).
Shopper language used: "joggers" (6,400 sessions), "men's joggers" (880), "jogger trousers" (370), "track pants" (210); "necklace" (2,100), "pendant necklace" (340). User synonym: "long dress" → "maxi dress" (not relevant here).

### Northwind Men Grey Melange Regular Fit Solid Joggers (EX-1001) · priority high

**Conflicts to check:** title says "Solid", but the image shows a black stripe down each leg and a printed panel near the ankle. Colour field says "multi"; image and title say grey melange.

| Field | Current | Suggested | Source | Confidence | Priority |
|---|---|---|---|---|---|
| title | Northwind Men Grey Melange Regular Fit Solid Joggers | Northwind Men's Grey Melange Joggers with Black Side Stripe, Regular Fit | seen in image | high | high |
| colors | multi | grey melange; black (stripe) | seen in image | high | high |
| pattern | — | side stripe | seen in image | high | medium |
| features | — | drawstring waist; ribbed cuffs; side pockets | seen in image | medium | medium |
| gender | — | men | from data | high | medium |
| material | — | *What is the fabric composition?* | needs a human | — | high |
| care | — | *Care instructions?* | needs a human | — | low |
| meta_description | — | Grey melange joggers from Northwind with a black side stripe, drawstring waist and ribbed cuffs. Regular fit. Shop men's joggers. | from data | high | high |
| long_description | "…, Buy Northwind joggers online at best price" | Easy everyday joggers in grey melange, finished with a contrast black stripe down each leg… | from data | medium | high |
| alt_text | — | Man wearing grey melange Northwind joggers with a black side stripe and ribbed cuffs, side view | seen in image | high | medium |
| search_terms | — | jogger trousers; track pants | from shopper searches | medium | low |

**Shopper questions (AEO):** Q: What fit are these joggers? A: Regular fit. · Q: Do they have an adjustable waist? A: Yes, a drawstring waist. · Q: What sizes are available? A: XXL is currently listed.
**AI summary (GEO):** Northwind men's joggers in grey melange with a black side stripe, drawstring waist and ribbed cuffs; regular fit; $34; currently listed in XXL.
**Needs a human:** fabric composition; care instructions; GTIN.

The script kept the current title in the JSON-LD, because the new one relies on the image: it goes in once a person confirms it.

### Halo pendant (EX-2002) · priority high

**Conflicts to check:** none found in the data. Images not viewed.

| Field | Current | Suggested | Source | Confidence | Priority |
|---|---|---|---|---|---|
| title | Halo pendant | Lumen Halo Pendant Necklace in 18K White Gold, 44 cm Chain | from data | high | high |
| meta_description | — | Lumen Halo pendant necklace in 18K white gold with an 8 mm inner diameter on a 44 cm chain. | from data | high | high |
| dimensions | — | pendant inner diameter 8 mm; chain length 440 mm | from data | high | medium |
| colors | white | *Confirm the metal colour against the image* | needs a human | — | low |
| alt_text | — | *Confirm what the main image shows, then write alt text* | needs a human | — | medium |

### Files

- `suggestions_example_apparel_2026-10-08.jsonl` (input, one line per product)
- `product_suggestions/suggestions.csv`, `suggestions.jsonl`, `review.md`, `jsonld/EX-1001.json`, `jsonld/EX-2002.json`

### Next steps

1. Review the suggestions, and check the EX-1001 conflicts against the product.
2. Answer the "needs a human" questions (fabric, care, GTIN, metal colour).
3. Import approved changes through your usual catalog process, and add the JSON-LD with the page changes.

**Caveats:** suggestions only; EX-2002 text-only; illustrative data.
