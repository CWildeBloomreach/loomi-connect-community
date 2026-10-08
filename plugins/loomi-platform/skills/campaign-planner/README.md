# Campaign planner

Suggests which campaigns to run in an upcoming window (default: the next 8 weeks). It combines a curated retail and cultural calendar for any market with last year's purchases, category peaks and campaign results for the same window in Bloomreach Engagement, rising and falling searches in Bloomreach Discovery, the campaign calendar's gaps and clashes, and existing segments. It returns ranked campaign ideas, each with a send window, channel, audience and size, angle, evidence, an estimated outcome and any clashes. It never creates or sends anything.

| | |
|---|---|
| **Products** | Engagement, Discovery (optional) |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_cloud_organizations`, `list_projects`, `get_event_schema`, `estimate_eql_cost`, `execute_analytics_eql`, `get_campaign_calendar`, `search_scenarios`, `search_segmentations`, `search_predictions`, `list_discovery_accounts`, `list_discovery_sites`, `get_discovery_search_performance`, `get_discovery_query_performance`, `get_discovery_trend`, `get_discovery_category_performance_table` |
| **Tested with** | Claude Code: each data step run live and read-only against a Discovery demo account and an Engagement sandbox and production project (aggregate queries only). Not yet run end to end as a single prompt, and not yet tested in an OpenAI client. |
| **Maintainer** | Bloomreach |

## Example prompts

- "What campaigns should we run over the next 8 weeks?"
- "Plan our UK and DE campaigns for Black Friday to Christmas."
- "We launch a gifting capsule on 2 November. What else should we send around it?"
- "What should we send in Australia between now and the end of January?"

See [examples/q4-plan.md](examples/q4-plan.md) for a full, partly illustrative, example output.

## Markets

- With no market given, it plans for **US, UK and EU** and says so.
- You can name **any market or several** (for example AU, DE, JP, IN, BR, UAE).
- [references/retail-calendar.md](references/retail-calendar.md) has a **Global** section plus sections for US, UK and EU (with DE, FR, NL, ES and IT differences). Each moment has its rule, 2026 and 2027 dates, a lead time and the categories it suits.
- For a market without a section, it uses the Global moments, looks up public holidays (if the client has web search), asks you to confirm local shopping moments, and labels those dates "unverified".
- **Adding a market** means adding a section to the calendar file and the matching rules to `scripts/retail_dates.py`. See "Adding a market" in the calendar file, and [CONTRIBUTING.md](../../../../CONTRIBUTING.md).

## Scripts

Both use the Python standard library only, with no network access.

- `scripts/retail_dates.py`: computes the calendar for any year and market from the rules (Easter, "4th Thursday of November", UK bank holiday substitutes, French sales dates and so on), filters to a planning window including promotion start dates, and handles unknown markets gracefully. Lunar and announced dates come from a lookup table that **should be updated yearly**.
- `scripts/weekly_peaks.py`: rolls a daily EQL breakdown, or a Discovery trend, into weeks, indexes each week against the median week, and tags the moments in each week.

## Notes and limitations

- **Expected outcomes are estimates.** They come from a similar past campaign where one exists, otherwise from last year's purchase uplift. With no history, the skill says so rather than inventing a number.
- **Audience sizes** need an aggregate EQL count per audience, because segmentations don't carry sizes. The skill sizes only the top 2–3 ideas, with your agreement.
- **EQL cost:** on large projects most event queries score "high". The skill runs only bounded, single-breakdown queries (usually 5–12), and never "very high" ones.
- **Moving dates** (Ramadan and the Eids, Diwali, Holi, Lunar New Year, Hanukkah, Amazon events) are marked "verified" or "verify" in the calendar. Islamic dates depend on moon sighting and can differ by a day between countries.
- The campaign calendar doesn't show event-triggered flows, and does show planned times for drafts. The skill lists drafts separately.
- With thin data (no purchase or campaign history, or no Discovery), it says so plainly and leans on the calendar and current demand.
- Hands off to `engagement-segment-builder`, `engagement-send-collision-check` and `search-demand-to-campaign` for building audiences, checking collisions and turning demand into a draft.
