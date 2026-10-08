# Product data enhancer

Improves the data of specific products so they're found and described well by search engines (SEO), answer engines and voice (AEO), and AI assistants and AI shopping answers (GEO). For each product it reads the catalog data, **looks at the product images with the assistant's own vision**, and checks the words shoppers search in Bloomreach Discovery. It then suggests a better title, descriptions and bullets, missing or wrong attributes (each marked *from data*, *seen in image* with confidence, *from shopper searches*, or *needs a human*), conflicts between image and data, alt text, shopper questions with factual answers, an AI-quotable summary, and schema.org Product JSON-LD. Suggestions only: nothing is written to any catalog.

| | |
|---|---|
| **Products** | Discovery (Engagement catalogs as an alternative source) |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `search_discovery_product_grid_insights`, `search_discovery_catalogs`, `search_discovery_catalog_products`, `get_discovery_product_performance_table`, `get_discovery_query_performance`, `list_synonyms_user`, `list_synonyms_br_generated`; for Engagement catalogs `list_cloud_organizations`, `list_projects`, `search_catalogs`, `search_catalog_items`. If any isn't listed, `search_tools` / `call_tool` |
| **Tested with** | Claude Code, October 2026, against a Discovery demo apparel account at account level: fetched a product by ID from the grid and the catalog, its image URLs, query performance for its product type and user synonyms; downloaded two product images and **viewed them** with the file-reading tool (and once via web fetch, which saved the image for viewing). The vision check found real issues (a "Solid" title on a product with a contrast stripe; a vague "multi" colour). The script was tested on the example JSONL plus malformed, wrong-schema and duplicate lines, via files and stdin. **Not run end to end** as a full batch; Engagement catalogs, `list_synonyms_br_generated`, chat apps with attached images and OpenAI clients weren't tested |
| **Maintainer** | Bloomreach |

## Example prompts

- "Improve the product content for these 10 jackets for SEO and AI search."
- "Look at the images for product 12345 and tell me what attributes are missing or wrong."
- "Write alt text and schema markup for our top 20 sellers."
- "Enrich the products the audit flagged in men's pants."
- "Make these product descriptions better for ChatGPT shopping, in our brand voice."

See [examples/example-apparel.md](examples/example-apparel.md) for an illustrative review, and [examples/example-suggestions.jsonl](examples/example-suggestions.jsonl) for the file format.

## How it works

1. **Products**: IDs, a category, a search, top sellers, or the audit's list. Up to **20 per run**: each product means viewing up to three images and writing a dozen suggestions, and beyond about 20 the conversation runs out of room and the result can't be reviewed properly. Larger lists run as batches.
2. **Data and image URLs** from the product grid (`thumb_image`, `large_image` list) and the catalog record.
3. **Shopper language** from query performance and synonyms, per product type.
4. **Images**: the assistant fetches each image from the catalog's own image host and looks at it. In Claude Code that means downloading to a temporary folder and opening the file (tested); in chat apps, the user attaches the images; otherwise a clearly labelled text-only fallback. Images and data are never sent to any third-party service.
5. **Suggestions** following the rubric's hard rules: no invented facts or claims, no medical or safety claims, brand voice respected, no competitor names, conflicts flagged rather than resolved.
6. **One JSONL line per product**, appended as each product is finished, so runs can be resumed and batches combined.
7. **Review files** from `scripts/suggestions_to_files.py`.

## Scripts

`scripts/suggestions_to_files.py` uses only the Python standard library and never touches the network. It reads the suggestions JSONL line by line from files or stdin (so batches can be concatenated), skips and reports malformed, wrong-schema and repeated lines with their line numbers, and writes incrementally: `suggestions.csv` (one row per change), `suggestions.jsonl` (one line per product), `jsonld/<id>.json` (schema.org Product) and `review.md`. It blocks unverified claims and banned terms, checks lengths and GTIN check digits, and keeps image-only values out of the JSON-LD.

## Notes and limitations

- **Vision has limits.** It can confirm product type, colour family, pattern and visible features, and spot conflicts. It can't establish fibre content, metal or karat, sizes, care, certifications or claims; those become "needs a human" questions.
- **Image fields vary by account.** On the demo account, `thumb_image` was a single URL and `large_image` a list present only on some products; no alt-text or swatch fields were returned. Demo images can be AI-generated, which lowers confidence.
- **Web fetch tools** may not return pixels: in Claude Code the fetch summary couldn't read an image, but the saved file could be opened and viewed.
- **JSON-LD** uses only verified (`known`) values, and must match what's on the page, so apply it together with the content changes after review. FAQ markup is optional (`--faq-jsonld`).
- Hand-offs: [product-data-audit](../product-data-audit/) to choose which products to enhance; the team's own catalog or feed process to apply approved changes.
