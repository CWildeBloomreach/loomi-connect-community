# On-site experience audit checks

Apply these to each experience. Report a finding only when the evidence supports it, and say what you couldn't check.

## Severity

- **Action:** probably wrong now (showing something it shouldn't, or clashing). Fix this week.
- **Test:** live without evidence that it works. Add an A/B test or a control group.
- **Review:** may be intended; a person should confirm.
- **Cleanup:** not live, but clutter. Archive it.
- **Info:** worth knowing.

## What the tools return (as seen in testing)

| Tool | List fields | Detail adds | Notes |
|---|---|---|---|
| `search_banners` | `_id`, `name`, `status` (`active`/`inactive`), `archived`, `tags`, `initiative_id`, `created`, `edited` | `variants[]` (with full content), `trigger.include_pages` / `exclude_pages`, `customer_filter`, and `date_filter` when scheduled | `archived=null` returns live and archived together. `serving_status` filters (`serving`, `before_schedule`, `after_schedule`, `inactive`) are computed client-side from the schedule |
| `search_in_app_messages` | name, status, tags, archived, initiative | variants, trigger, customer filter | Returned HTTP 403 in testing |
| `search_surveys` | name, status, tags, archived, initiative | questions, trigger, customer filter | Returned an empty list in testing; detail fields not verified |
| `search_experiments` | name, status, tags, archived, initiative | variants (control + treatment), traffic allocation, goals, customer filter | Returned HTTP 403 in testing |

In testing, banner details with no schedule had **no `date_filter` key at all**. The shape of `date_filter` on a scheduled banner wasn't observed; it's expected to match the customer-filter date filter (`enabled`, `absolute`, `from_date`, `to_date`, as Unix timestamps). Treat a missing or disabled `date_filter` as "no end date", and confirm a past `to_date` with `serving_status="after_schedule"`.

## Checks

### Schedule

| Check | Rule | Severity | Suggested action |
|---|---|---|---|
| Expired but active | `status` = `active` and (`date_filter.to_date` < now, or listed under `serving_status="after_schedule"`) | Action | Deactivate, or extend the end date on purpose |
| Not started yet | active and listed under `before_schedule` | Info | Confirm the start date |
| Active, no end date | active and no `date_filter`, or `date_filter.enabled` false | Review | Fine for always-on experiences (chat widget, cookie or consent layer, newsletter sign-up). For promotions and seasonal messages, add an end date |
| Old and active | active and `edited` more than 365 days ago | Review | Check the content, prices and offer are still current |

### Overlap

Compare every pair of **active** experiences of the same kind (web layers with web layers; in-app messages with in-app messages).

1. **Pages overlap** when either includes `{"type": "any"}`, or one URL rule contains the other (for example `/p/` and `/p/sale`), or both match the same page type. Remove pages that appear in the other's `exclude_pages`.
2. **Audiences overlap** when either has `customer_filter: null` (everyone), or both reference the same segmentation or filter. If both filters exist and differ, call it "possible overlap" unless they're clearly exclusive (for example "new visitors" and "returning customers").
3. **Format matters.** Two pop-ups, overlays or slide-ins on the same page: **Action** (they collide). An embedded block plus a pop-up: **Review**. Two embedded blocks in different slots: **Info**.

Suggested action: give them a priority or mutual exclusion (a shared customer filter or segmentation split), or schedule them apart.

### Testing

| Check | Rule | Severity |
|---|---|---|
| Never A/B tested | exactly one variant with `enabled: true`, at `percentage` 100, and no control variant | Test |
| Test with no end | two or more variants, active for 60+ days since `edited`, and no winner picked | Review: pick a winner and stop splitting traffic |
| Uneven split, no control | several variants but no control or holdout | Review: you can compare variants but not prove lift |
| Possibly split in code | name, tags or variant names mention test, split, control or holdout, but there's only one variant | Info: some web layers assign a control group in their own script; confirm with the owner |

Prioritise **Test** findings by reach: experiences on every page or on high-traffic pages (home, product, category, cart) first.

### Performance (only if banner events exist)

| Check | Rule | Severity |
|---|---|---|
| Low click-through | unique clickers ÷ unique viewers below about 1% (pop-ups) or 0.3% (embedded) over 30 days | Review |
| Annoying | unique closers ÷ unique viewers above about 60% | Review |
| Active but silent | active, serving, but no banner events in 7 days | Review: tracking may be custom or broken, or the page rules match nothing |
| A variant losing | in a test, one variant's click-through is less than half another's with at least 1,000 viewers each | Test: end the losing variant |

These are rough benchmarks. Compare with the project's own median when you have several banners.

### Drafts and clutter

| Check | Rule | Severity |
|---|---|---|
| Stale inactive | `status` = `inactive`, not archived, `edited` more than 90 days ago | Cleanup |
| Draft or test copy | name contains draft, test, testing, copy, old, backup, dev, POC, QA, sandbox, "do not use", "v1" where a "v2" exists | Cleanup (Review if active) |
| Labelled archived but isn't | name starts with "[ARCHIVED]" or similar but `archived` is false | Cleanup |
| Near-duplicates | names that differ only by a prefix such as "[NEW]", "[OLD]", "[V2]", "(copy)" | Review: keep one source of truth |
| Active test copy | an active experience whose name says test, dev, QA or POC | Action: it may be showing test content to real visitors |

When there are many, group them ("31 inactive web layers last edited more than 90 days ago, mostly per-category embedded blocks") rather than listing each one.

## Before recommending removal

- A web layer can be shown by a scenario (`serve-banner-action` node) even if the banner itself is inactive. Check active scenarios if the user wants certainty.
- A web layer can be placed through Discovery. `get_discovery_weblayer_customizations` with its ID shows whether Discovery still references it.
- Aggregates or segmentations can list a banner in their `used_by` (for example `banner_<id>`), which shows dependencies the other way.
