# Product data audit

Answers "how good is our product data, and which products do we fix first?" for a Bloomreach Discovery catalog (or an Engagement catalog). It scores each product's title, description, attributes, identifiers, image count and vocabulary against a rubric built for classic search engines (SEO), answer engines and voice (AEO) and AI assistants and AI shopping answers (GEO). It weights every product by revenue and views, and checks the words shoppers actually search. It returns a catalog-wide summary of the most common gaps, the categories to fix first, and a prioritised product list to hand to [product-data-enhancer](../product-data-enhancer/). Text-only and read-only.

| | |
|---|---|
| **Products** | Discovery (Engagement catalogs as an alternative source) |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `search_discovery_product_grid_insights`, `search_discovery_catalogs`, `search_discovery_catalog_products`, `list_facet_attributes` (via `search_tools` / `call_tool`), `get_discovery_product_performance_table`, `get_discovery_query_performance`, `list_synonyms_user`; for Engagement catalogs `list_cloud_organizations`, `list_projects`, `search_catalogs`, `search_catalog_items` |
| **Tested with** | Claude Code, October 2026: individual read-only calls against a Discovery demo apparel account at account level (catalog facets, a 20-product grid page with text fields, a 3-product `pid` OR filter, one catalog record, the product and query performance tables, user synonyms). The script was tested on invented fixtures shaped like those responses, including JSONL input with a malformed line and stdin. **Not run end to end** on a full catalog; Engagement catalogs, site-level reporting and an OpenAI client weren't tested |
| **Maintainer** | Bloomreach |

## Example prompts

- "How good is our product data for SEO and AI search?"
- "Which products should we enrich first?"
- "Where are we missing attributes across the catalog?"
- "Audit the product content in men's pants and women's dresses."
- "Is our catalog ready for ChatGPT shopping and AI answers?"

See [examples/example-apparel.md](examples/example-apparel.md) for an illustrative output.

## How it works

1. **Catalog shape** from one product grid call with facets: catalog size, rough fill rates, inconsistent values ("grey" vs "gray"), misused fields, the category tree.
2. **Commercial weight and shopper language** from the product performance table (revenue, views) and query performance (what shoppers type).
3. **Product data** for the chosen scope: the top 500 products by revenue (fetched 50 at a time with a `pid` OR filter), named categories, or the whole catalog (200 per page).
4. **Scoring** with `scripts/audit_products.py`: every product starts at 100 and loses points for gaps in title (T), description (D), attributes (A), identifiers and offer (S), images (I) and shopper vocabulary (V). Priority combines the gap with revenue and views.
5. **Recommendations** in three groups: quick feed fixes, content work (hand-off to `product-data-enhancer`, up to 20 products per run), and facts only a person can supply.

## Scripts

`scripts/audit_products.py` uses only the Python standard library and never touches the network. It reads saved grid pages, catalog records, Engagement item lists, or JSONL (one product per line, from files or stdin), streams them in two passes (catalog-wide facts, then scoring), skips malformed lines with their line numbers, and writes one JSONL result line per product with `--jsonl`, plus a summary as JSON or Markdown.

## Notes and limitations

- **Text-only.** It counts image URLs but never opens images; [product-data-enhancer](../product-data-enhancer/) does the looking.
- The rubric is a triage tool, not a grade. Rules can misfire on unusual catalogs (for example a store's own label deliberately left out of titles), so check a few flagged products before reporting a catalog-wide gap.
- Fill rates from facets are approximate: colour facets count variants and facets are truncated. `fq="field:*"` doesn't count filled values (in testing it matched every product, including empty ones).
- The product grid's `fl` can't return `category_paths`; categories come from the category facet or `search_by="category"`.
- Engagement catalogs: `search_catalog_items` reaches at most 1,000 items (`skip` + `count` ≤ 1,000), and there's no performance table for Engagement-only catalogs.
- Hand-offs: [product-data-enhancer](../product-data-enhancer/) for the suggestions, `data-feed-health` for feed problems.
