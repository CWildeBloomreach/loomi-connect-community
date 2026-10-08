# On-site experience audit

Audits the on-site and in-app experiences in a Bloomreach Engagement project: web layers (banners), in-app messages, surveys and web experiments. It flags experiences still active after their end date or with no end date, overlapping experiences on the same pages and audiences, experiences never A/B tested, poor performers (where banner events are tracked), and drafts and test copies left lying around. It returns a prioritised cleanup and test list, and it never changes anything.

| | |
|---|---|
| **Products** | Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_cloud_organizations`, `list_projects`, `search_banners`, `search_in_app_messages`, `search_surveys`, `search_experiments`, optionally `search_scenarios`, `search_scenario_nodes` (via `call_tool`), `get_event_schema`, `estimate_eql_cost`, `execute_analytics_eql`, `get_discovery_weblayer_customizations` |
| **Tested with** | Claude Code: banner list, `serving_status` filters and banner details read live from a sandbox and a production project; `search_surveys` ran (no surveys); `search_in_app_messages` and `search_experiments` returned HTTP 403 in both projects, so their checks are untested; banner EQL patterns estimated and partly run (no `show` events found). The script was tested on synthetic responses. Not tested in an OpenAI client. |
| **Maintainer** | Bloomreach |

## Example prompts

- "Audit our web layers. What's still live that shouldn't be?"
- "Which pop-ups overlap on the product pages?"
- "Give me a cleanup list for old banners and test copies."
- "Which on-site experiences have never been A/B tested?"

See [examples/illustrative-audit.md](examples/illustrative-audit.md) for an example output. Its names and numbers are illustrative.

## How it works

1. Lists every experience, and uses `search_banners`' `serving_status` filter to find active web layers past their end date.
2. Fetches details only for the active ones, keeping the schedule, page rules, audience and variant split, and **dropping all HTML, CSS and JavaScript**.
3. Applies the checks in [references/audit-checks.md](references/audit-checks.md). [scripts/audit_experiences.py](scripts/audit_experiences.py) does this from saved responses (standard library only, no network, never prints content).
4. Optionally measures unique viewers, clickers and closers per web layer with aggregate EQL. See [references/eql-patterns.md](references/eql-patterns.md).

## Notes and limitations

- Banner details are very large (full code per variant). The skill fetches them only for active experiences.
- Banners have only `active` and `inactive` statuses, so "drafts" are found by staleness and naming (draft, test, copy, old, dev, POC, QA...).
- The shape of a banner's schedule (`date_filter`) wasn't observed in testing, because no tested banner had one. The skill relies on `serving_status="after_schedule"` to confirm expired-but-active banners.
- Event-level banner breakdowns are rated `very_high` beyond 7 days, so performance uses per-banner customer counts. The standard `show`/`click`/`close` action values weren't confirmed in testing; some web layers track a custom event instead.
- A web layer can also be shown by a scenario or placed through Discovery. The skill checks these only when asked.
