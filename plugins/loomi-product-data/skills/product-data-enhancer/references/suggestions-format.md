# Suggestions format (JSON Lines)

Read this before writing suggestions in step 6 of the skill. The suggestions file is **JSON Lines** (`.jsonl`): **one product per line**, each line a complete JSON object. Append a line as soon as a product is finished. That way:

- a run that stops part-way can be **resumed**: read the product IDs already in the file and carry on with the rest;
- batches can be **combined** by concatenating files (`cat batch1.jsonl batch2.jsonl`);
- the format scales to a whole catalog, because nothing has to hold every product at once.

Write each line as compact JSON on a single line (no line breaks inside it). Use a file name that says what it is, such as `suggestions_<account>_<date>.jsonl`, in a working folder the user can see.

## One line

```json
{"schema": "loomi-product-suggestions", "version": "1", "product_id": "EX-1001", "account": "example_apparel", "currency": "USD", "title": "Current product title", "category": "men/pants", "images": ["https://images.example.com/EX-1001.webp"], "images_viewed": true, "image_method": "downloaded and viewed", "shopper_queries": ["joggers", "jogger trousers"], "brand_voice": "plain, friendly", "known": {"name": "...", "brand": "...", "price": 34, "availability": "in stock"}, "suggestions": [{"field": "title", "current": "...", "suggested": "...", "source": "seen in image", "confidence": "high", "priority": "high", "evidence": "..."}]}
```

(Shown on one line, as in the file. The skill's `examples/example-suggestions.jsonl` has two full lines.)

## Top-level fields

| Field | Required | Meaning |
|---|---|---|
| `schema` | yes | Always `"loomi-product-suggestions"`. Lines with any other value are skipped |
| `version` | yes | `"1"` for this format |
| `product_id` | yes | The catalog's stable product ID (`pid` in Discovery, `item_id` in Engagement). One line per product; if a product appears twice, the script keeps the first and reports the second with its line number. To redo a product, remove its old line |
| `account` | no | Account or catalog name, for the team's reference |
| `currency` | for JSON-LD | ISO 4217 code (`USD`, `EUR`). Ask the user if you don't know it |
| `title` | no | The current title, for the review table |
| `category` | no | Category path or name |
| `images` | no | The image URLs found in the data |
| `images_viewed` | yes | `true` only if you actually looked at at least one image for this product |
| `image_method` | no | How: `"downloaded and viewed"`, `"fetched and viewed"`, `"attached by user"`, or `"not viewed (<reason>)"` |
| `shopper_queries` | no | The shopper searches used for this product |
| `brand_voice` | no | The voice notes the user gave, if any |
| `known` | for JSON-LD | **Verified values only**, from the catalog data (or confirmed by a person): `name`, `description`, `brand`, `sku`, `gtin`, `mpn`, `price`, `sale_price`, `currency`, `availability`, `condition`, `color`, `material`, `size`, `pattern`, `category`, `url`, `image`, `rating`, `review_count`. Never put image-only or guessed values here. Never put internal fields (`margin`, `cost`) here |
| `suggestions` | yes | The list below |

## Each suggestion

| Field | Required | Meaning |
|---|---|---|
| `field` | yes | What it changes. Use the catalog's own attribute name where there is one (`colors`, `material`, `product_size`), or one of: `title`, `meta_description`, `long_description`, `bullets`, `alt_text`, `faq`, `ai_summary`, `comparison_attributes`, `search_terms`, `features` |
| `current` | yes | The value now (`""` if empty) |
| `suggested` | yes | The new value. A list for `bullets`, `alt_text` (one per image) and `faq` (`[{"q": "...", "a": "...", "source": "..."}]`); an object for `comparison_attributes`. For `needs a human`, write the **question** to ask, never an invented value |
| `source` | yes | `from data`, `seen in image`, `from shopper searches`, or `needs a human` |
| `confidence` | for `seen in image` | `high`, `medium` or `low` |
| `priority` | yes | `high`, `medium` or `low` (see the enhancement rubric) |
| `evidence` | yes | Where it came from: the field or sentence in the data, what the image shows, or the query and its sessions |
| `conflict` | no | `true` when the image and the data disagree. Say both values in `evidence` |

## What the script does with it

`scripts/suggestions_to_files.py` reads the lines one by one (from files or stdin) and writes, incrementally:

- `suggestions.csv`: one row per suggestion, with `status` = `suggestion - needs human review`, or `BLOCKED: …` for unverified claims and banned terms. `needs a human` rows have an empty `suggested` and the question in `evidence`;
- `suggestions.jsonl`: one output line per product (`"schema": "loomi-product-suggestions-review"`), with its rows, JSON-LD and checks;
- `jsonld/<product_id>.json`: the schema.org Product block;
- `review.md`: the review tables.

Malformed lines, a wrong `schema`, a missing `product_id` and repeated IDs are reported with file and line number and skipped; the rest of the run carries on.
