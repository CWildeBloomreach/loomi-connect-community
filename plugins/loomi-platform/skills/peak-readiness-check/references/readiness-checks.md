# Readiness checks, statuses and owners

The full list of checks, with the rule for each status and who usually owns the fix. `scripts/check_rule_windows.py` applies the merchandising-rule rows; the rest are applied by the assistant.

## Owner types

| Owner type | Usually means |
|---|---|
| Web developers | The site's front-end team: tracking pixel, SDK, page templates |
| Feed or catalog owner | Whoever produces the product feed (e-commerce platform, PIM, integration team) |
| Merchandiser | Discovery rules, redirects, dynamic categories, banners in Discovery |
| Search admin | Synonyms, spell-correction keywords, search settings |
| Buyer or trading team | Stock depth and assortment for the event |
| CRM or email marketer | Engagement campaigns, scenarios, weblayers |
| CRM analyst | Segments, customer filters, audience sizes |
| Engagement admin | Frequency policies, consent, project settings |
| Test owner | Whoever started a running A/B test |

## Data

| Check | RED | AMBER | GREEN |
|---|---|---|---|
| Pixel, core types | 20%+ issues, no events, or count below half the 7-day daily average | 1–20% issues, or a 25–50% drop | under 1%, steady |
| Product feed and index | latest failed, or no success in 48 h | success with a warning; earlier failures; 24–48 h old; daily feed for a flash sale | recent successes on cadence |

## Merchandising rules (per rule)

Times are `startedAt` and `endedAt` in Unix milliseconds. "Event rule" means its name or one of its queries matches the event vocabulary.

| Check | How to spot it | Status |
|---|---|---|
| Event rule starts late | enabled event rule, `startedAt` after the event start | RED if it's the only event rule on that query or category; else AMBER |
| Event rule ends early | enabled event rule, `endedAt` before the event end | RED if only one; else AMBER |
| Event rule disabled | event rule with `enabled: false` | RED if only one for that query; else AMBER |
| Event rule never ends | enabled event rule, `durationTag: "unscheduled"` | AMBER: will run after the event |
| Expires mid-event | any enabled rule with `endedAt` inside the window | RED for an event rule, AMBER otherwise |
| Starts mid-event | any enabled rule with `startedAt` inside the window, after the start | AMBER: confirm it's intended |
| Leftover from a past event | enabled, `durationTag: "expired"` | AMBER |
| Never synced | `syncStatus: null` on an event rule | RED: it was saved but never published |
| In a running test | `isAbTestLive: true` | AMBER, or RED if the rule still needs changing before the event |
| No event rules at all | nothing matches the vocabulary | AMBER; RED if the user says rules were planned. Confirm the vocabulary first |

Notes:

- Use `durationTag` and the timestamps. `syncStatus` doesn't reliably show expiry.
- The list's `audienceName` can be null even for targeted rules. Two event rules on the same query may be personalisation, not a conflict: check with `get_ranking_rule` or `get_discovery_media_rule` before flagging.
- Facet rules have no dates; skip them unless the event needs a "sale" facet pinned.
- Redirects use the same fields. A redirect is the cleanest fix for generic event queries ("black friday" → the event landing page).

## Experiments

| Check | Status |
|---|---|
| RUNNING test whose end date is after the event start | RED if event rules in its scope still need changing; else AMBER |
| RUNNING test with no end date | AMBER: ask the test owner when it ends |
| DRAFT test due to start during the event | AMBER: a test starting on peak day muddies the results |

## Landing pages and grids

| Check | RED | AMBER | GREEN |
|---|---|---|---|
| Event dynamic category | `numFound` 0 | fewer than ~24 products, or misfit top results | full page of relevant products |
| Top categories (by visits) | empty grid | thin, or top results out of stock or duplicated | normal |

Preview with `search_discovery_product_grid_insights`, `search_by="category"` and the category ID (dynamic categories use their `categoryId`, such as `brg_dyn_…`).

## Search for event queries

| Signal in the product grid response | Meaning | Status |
|---|---|---|
| Redirect rule exists, dates cover the window | Shoppers go straight to the event page | GREEN |
| `numFound` 0 | Dead end | RED |
| `data.autoCorrectQuery` set, or `metadata.query.modification.mode` is `autoCorrectQuery` | The engine rewrote the query, often into something else | RED for event terms |
| `modification.mode` is `relaxedQuery` (`data["relaxed.query"]` shows what was kept) | Words were dropped | AMBER |
| Very high `numFound` with off-topic top results | Broad semantic or keyword match, not shaped by rules | AMBER |
| Relevant top results, event rules applied | Fine | GREEN |

## Marketing (Engagement)

| Check | RED | AMBER | GREEN |
|---|---|---|---|
| Event sends on the calendar | none on key event days | sends still in draft or inactive | active or scheduled |
| Clashes | same audience, same channel within 24 h and no frequency cap | overlapping sends, busy days (3+), email and SMS within 4 h | none |
| Target segments | missing or archived segmentation; zero or tiny audience | much smaller than expected | sized and plausible |
| Frequency caps | — | default `unlimited-policy` with several event sends; or a strict cap that would drop a key send | a cap set and sized for the event |
| Always-on flows | — | no abandoned-cart or browse flow active | active |

## On-site engagement

| Check | RED | AMBER | GREEN |
|---|---|---|---|
| Event weblayer or banner | already ended (`after_schedule`) | exists but inactive; none and one is expected | active, scheduled to cover the window |

`search_banners` list mode doesn't return schedules. Use the `serving_status` filter values `serving`, `before_schedule`, `after_schedule` and `inactive` to classify, and fetch a single banner only when you must read its dates.
