# Example: Black Friday readiness

**The Discovery half is real; the Engagement half is illustrative.** The Discovery findings come from a read-only run on 8 Oct 2026 against a Bloomreach demo account, renamed `example_apparel`. The Engagement findings are modelled on a run against a real organisation, so the project, campaign and segment names are placeholders and every number has been changed.

**Prompt:** "Are we ready for Black Friday? Event runs Fri 27 Nov to Mon 30 Nov, US Eastern."

## Peak readiness: Black Friday, 27 Nov 00:00 to 30 Nov 23:59 (US Eastern)
Checked 8 Oct 2026; 50 days to go. Scope: example_apparel (Discovery, account level, no sites), example-retail-prod (Engagement).

**Verdict:** NO-GO: nothing is scheduled for the event yet. Shoppers searching "black friday" get black clothing, there are no Black Friday rules, redirects or sends, and the search page pixel is broken.

### Blockers (fix before the event)
| # | Area | Check | Evidence | Fix | Owner |
|---|---|---|---|---|---|
| 1 | Data | Search page pixel | 100% of 26.1k search page views in 24 h flagged `catalogs_required` | Add the `catalogs` parameter to the search results page pixel, so event-day search reporting works | Web developers |
| 2 | Search | "black friday" | Auto-corrected to "black frisky"; 42 results, top ones are a black tie and black shirts. No redirect | Add a redirect to the event page, scheduled 27–30 Nov, and add "black friday" as a keyword so it isn't spell-corrected | Merchandiser / search admin |
| 3 | Marketing | Event sends | No customer email, SMS or push on the calendar for 24 Nov – 3 Dec. Only an internal report webhook and a draft internal email | Schedule the event sends now; template approval needs lead time | CRM or email marketer |

### Amber (fix or accept)
| # | Area | Check | Evidence | Fix | Owner |
|---|---|---|---|---|---|
| 1 | Merchandising | Event rules | None of 34 search ranking, 22 category media or 3 redirect rules is scheduled; the only Black Friday rule ("Skirts black Friday", banner on "skirts") has no end date | Create and schedule event ranking and banner rules; give the skirts banner an end date of 30 Nov | Merchandiser |
| 2 | Merchandising | Leftover rule | "Honeymoon Edit Campaign" category banner ended Feb 2026 but is still enabled | Disable it | Merchandiser |
| 3 | Landing pages | "summer sale" dynamic category | Only 3 products (it requires category 70300 and gender female) | Retire it, or build a Black Friday dynamic category from a sale flag | Merchandiser / feed owner |
| 4 | Search | "gifts for him" | Relaxed to "gifts": 27 results, the top three are the same belt gift set | Add a gift guide redirect or a ranking rule for gift queries | Merchandiser |
| 5 | Search | "sale" | 2,056 results (about a quarter of the catalog), top results a tie and full-price tops; no rule or redirect | Redirect "sale" to the event page, or boost on-sale products | Merchandiser |
| 6 | Data | Product feed | Daily full feed succeeded at 00:06 UTC but warns "Feed data contains null values" | Fix the null fields; ask whether the feed can run several times a day during the event | Feed owner |
| 7 | Marketing | Frequency cap | Default policy is unlimited | Set an event cap, and check which send it would drop | Engagement admin |
| 8 | Marketing | Always-on flows | No abandoned-cart or browse-abandonment scenario is active | Build one before peak (see `funnel-leak-finder`) | CRM or email marketer |
| 9 | On-site | Event weblayer | The only active weblayer is a chat widget; nothing for Black Friday | Create and schedule an event weblayer, or confirm none is planned | CRM or web marketer |

### Green
- **Data:** product, category, conversion and add-to-cart pixels under 0.1% issues; index job 8 h old, 8,183 products, steady.
- **Merchandising:** no A/B test is running, so nothing blocks changes (two old drafts exist).

**Not checked:** event segment sizes (no event sends to size yet); top category grid previews beyond the event pages.
**Lead times:** pixel fix (a front-end release); event sends (template build and approval); feed cadence (feed owner).
