# Example: redirect audit (illustrative)

This example is illustrative. The account, rules, URLs and figures are made up to show the output format. They don't come from a real account.

**Prompt:** "Can you check our search redirects? Some searches seem to land on odd pages."

## Search redirect audit: example_home (account level, 8 Oct 2026; traffic: last 90 days)

**Headline:** The "sale" redirect is a phrase match, so about 6,400 product searches such as "sale sofas" go to a landing page instead of results. Switch it to exact match.

**Inventory:** 14 redirects (12 enabled; 9 exact match, 3 phrase match). Destinations checked by URL shape only (not loaded).

### Fix now
| # | Redirect | Queries (match) | Destination | Problem | Evidence | Fix |
|---|---|---|---|---|---|---|
| 1 | "Sale" | sale (phrase) | www.example-home.com/sale | Hijacks product searches | Grid: "sale sofas", "rugs sale" and 11 more redirect; 6,400 sessions on those searches in 90 days | Exact match; add "sales" and "on sale" |
| 2 | (unnamed) | return | https://staging.example-home.com/returns | Non-production host | Live shoppers sent to staging | Point at the production returns page |
| 3 | "Returns" and (unnamed) | returns / return | /help/returns and staging URL | Two redirects, two destinations, same intent | Both enabled, no audiences | Keep "Returns"; add "return" to it; delete the other |

### Add these redirects
| Query | Sessions (90 days) | Bounce | Revenue | What the grid shows | Suggested destination |
|---|---|---|---|---|---|
| store locator | 1,840 | 86% | $0 | Off-topic: lamps and storage boxes | Store finder page (URL needed) |
| track order | 1,210 | 91% | $0 | Off-topic: curtain tracks | Order status page |
| gift cards | 960 | 78% | $0 | No gift card products | Gift card page. "gift card" (singular) already redirects; add the plural |

### Clean up
| Redirect | Problem | Evidence | Fix |
|---|---|---|---|
| "Black Friday 2025" | Expired but enabled | `durationTag` expired | Disable or delete |
| "About" and "About Us" | Same destination | Both go to /about-us | Merge into one rule |
| Ranking rule on "catalog" | Rule on a redirected query | "catalog" redirects, so the rule never shows | Disable the ranking rule |

### Review
| Redirect | Problem | Evidence | Suggestion |
|---|---|---|---|
| "Linen" | May hide good results | Grid: 180 linen bedding and curtain products, all on-topic | Ask the merchandiser whether the lookbook is still wanted |
| "Refund" synonym | Points at a redirect query | "refund" → "returns" is a synonym, but "refund" doesn't redirect | Add "refund" to the returns redirect |
| 9 redirects | No scheme in URL | e.g. www.example-home.com/sale | Usually fine; check one in a browser |

**Healthy:** "about us", "careers", "app" and "contact us" redirect on exact match to production pages, and the grid confirms they fire.
**Not checked:** destination pages weren't loaded; check exits on them in web analytics.
**Next steps:** fix the three "Fix now" rows; add the three navigational redirects; run discovery-zero-results-triage for the non-navigational dead-end searches ("boucle armchair", "rattan headboard").
