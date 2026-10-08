# Redirect checks and priorities

These are the checks `scripts/redirect_checks.py` runs, plus the ones that need the product grid, so you can apply them by hand if scripts aren't available.

## Destination URL (shape only)

Loomi Connect can't load web pages. Unless the client has a web-fetch tool and the user agrees, judge the URL by its shape and say that it wasn't loaded.

| Sign | Why it matters | Priority |
|---|---|---|
| Empty URL, a space inside it, or `javascript:` / `data:` | Won't load | Fix now |
| Host contains `staging`, `stage`, `dev`, `qa`, `uat`, `test`, `preview`, `sandbox`, `localhost` or `example.com` | Sends live shoppers to a non-production site | Fix now |
| Placeholder text: `{`, `}`, `TODO`, `TBD`, `undefined`, `null` | Unfinished rule | Fix now |
| No scheme (`shop.com/returns` rather than `https://shop.com/returns`) | Works only if the front end adds one. Common and often fine; check one in a browser | Review |
| `http://` rather than `https://` | Extra redirect hop; mixed-content warnings | Review |
| A different host from the other redirects | Could be a retired domain, or deliberate (a help centre, a store locator service) | Review |
| A year, sale or holiday in the path (`/black-friday`, `/2024-gift-guide`) | Campaign pages are often removed after the campaign | Review |
| `utm_` or `gclid` parameters | Pollutes campaign attribution | Review |
| A category ID in the path | Check it still exists with `list_categories` (IDs there are lower-cased) | Review |
| Double slash in the path, or a trailing `.` `,` `;` `)` | Usually a copy-paste error | Review |

## Duplicates and overlaps

| Check | How to spot it | Priority | Action |
|---|---|---|---|
| Same query, different destinations | Two enabled redirects for the same query (ignoring case, punctuation and a plural "s") with different URLs and the same audience (or none) | Fix now | Keep one. Check `audiences` first: one default plus one audience-specific redirect is personalisation |
| Same query, same destination | As above, same URL | Clean up | Merge |
| Same destination, different rules | Several rules point at one URL | Clean up | Merge the queries into one rule, so it's maintained in one place |
| Phrase match inside another query | A phrase-match redirect's query appears inside another redirect's query | Review | Check in the product grid which one fires |
| Expired but enabled | `enabled: true`, `durationTag: "expired"` | Clean up | Disable or delete |
| Disabled | `enabled: false` | Clean up | Delete if nobody needs it |

## Broad queries (hijacking)

| Sign | Priority |
|---|---|
| `PHRASE_MATCH` on one word, especially a product word ("sale", "dress", "gift", "new") | Fix now if the grid shows longer product searches redirecting |
| `PHRASE_MATCH` whose query appears inside other tracked searches with traffic | Fix now if those searches are product searches |
| A query of three characters or fewer | Review |

Confirm with the product grid: run the longer searches and look for `keywordRedirect`. The fix is usually to switch to exact match and list the wordings shoppers use, or to choose a more specific query ("gift card" rather than "gift").

## Synonyms and other rules

| Check | Why it matters | Priority |
|---|---|---|
| The redirect query is a synonym's **source** | The synonym never applies while the redirect fires; one of them is dead config | Review |
| A synonym expands **to** the redirect query (e.g. "refund" → "returns") | Shoppers typing the synonym get products, not the redirect. Synonyms don't make other wordings redirect. If they mean the same thing, add the wording to the redirect | Review |
| An enabled ranking or banner rule on a redirected query | Shoppers never see that results page, so the rule does nothing | Clean up |

Confirm synonym behaviour in the grid before reporting it: run the synonym's source term and check whether `keywordRedirect` is present. Wider synonym problems belong to the discovery-synonym-review skill.

## Is the redirect still needed?

Redirected searches don't appear in query performance, so there's no click-through or exit rate for them in Loomi Connect. Use these signals instead:

- **Products behind the redirect.** Run the grid. If the top titles are good matches for the query as a product search, the redirect may be hiding results (for example "linen" redirected to a lookbook while the catalog has many linen products). Review it with the merchandiser. If the titles are off-topic, the redirect is doing its job.
- **Sessions on the redirect query.** If the redirect query itself has search-results sessions, it didn't fire for part of the window. Check the schedule and the grid.
- **Destination performance.** Not available in Loomi Connect. Suggest the user checks exits and bounces on the destination page in their web analytics.

## Searches that deserve a redirect

Navigational searches look for a page, not a product. Common ones:

returns, return policy, refund, exchange, store locator, stores near me, find a store, gift card(s), e-gift card, track order, order status, contact us, customer service, help, FAQ, shipping, delivery, size guide, size chart, login, sign in, my account, careers, app, about us, coupon, promo code, discount code, student discount, warranty, Klarna, Afterpay, financing, rewards, loyalty, catalog.

Flag one when it has meaningful sessions (default 50 in 90 days), no redirect, and the signs of a failing product search: high bounce, few product page views, no revenue. Confirm with the grid: off-topic or no products means it needs a redirect. Order by sessions.

Some are product searches on some sites. "Gift card" is a product if gift cards are in the catalog, and "app" can be part of "apple". Check the grid titles before recommending a redirect.

Dead-end searches that aren't navigational need products, synonyms or rules, not a redirect. Hand them to the discovery-zero-results-triage skill.

## Priority summary

1. **Fix now:** enabled redirects with a broken-looking or non-production URL; conflicting redirects for the same query; phrase-match redirects catching product searches with traffic.
2. **Add:** high-traffic navigational searches with no redirect.
3. **Clean up:** expired, disabled and duplicate rules; rules on redirected queries; merge candidates.
4. **Review:** URL shape warnings, possibly unnecessary redirects, synonym overlaps, redirects in a running A/B test.
