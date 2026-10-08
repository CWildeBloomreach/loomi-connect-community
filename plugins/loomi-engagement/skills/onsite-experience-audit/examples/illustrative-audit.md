# Example: on-site experience audit (illustrative)

**This example is illustrative.** The method and the tool behaviour come from a live, read-only test run, but the project, every experience name and every number have been invented or changed. Nothing was changed in the project.

**Prompt:** "Can you audit our web layers and on-site stuff? I think there's a lot of junk in there."

---

## On-site experience audit: Example Store (production), 2026-10-08

**Verdict:** Only 3 of 64 web layers are live, but one of them is an expired promotion that's still showing, and two pop-ups compete for the same product-page visitors. The other 61 are clutter: archive about 40 of them.

**Inventory:** web layers 3 active / 64 total (12 archived); in-app messages not checked (no access, HTTP 403); surveys 0; experiments not checked (no access, HTTP 403)

### Fix now
| Experience | Type | Problem | Evidence | Do this |
|---|---|---|---|---|
| Summer sale pop-up | Pop-up | Expired but still active | End date 2026-09-01; listed under "after schedule" | Deactivate it, or extend the date on purpose |
| Summer sale pop-up + Newsletter sign-up | Pop-ups | Collide on product pages | Both target URLs containing "/p/"; neither has a customer filter | Exclude newsletter subscribers from the sign-up, or give the sign-up a delay and exclude product pages from the promo |

### Test next
| Experience | Placement | Why test | Suggested test |
|---|---|---|---|
| Newsletter sign-up | Every product page, everyone | One variant at 100% for 14 months | 90/10 split against no pop-up; measure sign-ups and product-page bounce |
| Free-shipping bar | Every page, everyone | One variant, never tested | Threshold message vs none; measure average order value |

### Review
- **Free-shipping bar:** active with no end date. Fine if it's always on; confirm the threshold is still current (last edited 400 days ago).
- **Performance:** no `banner` events in the last 7 days for any active web layer. The free-shipping bar and the pop-ups may track a custom event, or may not be firing. Check with the web team before judging results.

### Clean up
- 31 inactive per-category embedded blocks last edited 5–10 months ago ("Category block - Mens shoes" and similar). Archive them in bulk.
- 9 inactive test or draft copies ("[TEST] ...", "[DRAFT] ...", "... - copy", "[OLD] ... v1").
- 4 named "[ARCHIVED] ..." but not actually archived.
- 6 groups of near-duplicates ("[NEW] Product Q&A" / "Product Q&A" / "[V2] Product Q&A"): keep one source of truth.

**Performance:** one 7-day `banner` event count (rated high, run with your agreement) returned no rows. Per-banner customer counts weren't run. 30- and 90-day event breakdowns were rated very high and skipped.
**Not checked:** in-app messages and experiments (access denied); web layers served from scenarios; Discovery placements (`get_discovery_weblayer_customizations` can confirm whether Discovery still uses any web layer before you archive it).
