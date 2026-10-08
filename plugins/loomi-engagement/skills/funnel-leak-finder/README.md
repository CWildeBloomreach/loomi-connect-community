# Funnel leak finder

Finds where revenue leaks between product view, add to cart, checkout and purchase in Bloomreach Engagement, and puts a figure on each leak. It:

- counts customers at each funnel step with aggregate EQL funnels, overall and by device, OS or traffic source;
- checks that the purchase step is trustworthy, so an identity or import gap isn't reported as a checkout leak;
- sizes abandoned carts and the value left in them;
- checks whether cart abandonment, browse abandonment and post-purchase scenarios exist and are active;
- ranks the leaks by recoverable revenue, with hand-offs to `engagement-segment-builder` and `engagement-scenario-explainer`.

It uses aggregate counts only and never changes anything.

| | |
|---|---|
| **Products** | Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_cloud_organizations`, `list_projects`, `get_event_schema`, `search_funnels`, `estimate_eql_cost`, `execute_analytics_eql`, `search_scenarios`, `search_scenario_nodes` (via `search_tools` and `call_tool`) |
| **Tested with** | Claude Code (manual read-only run, October 2026: event schema, saved funnels, funnel, filtered-funnel, value and purchaser-count EQL on a sandbox and a production project, aggregates only; scenario lists with trigger filters. Not run live: the traffic-source funnel (parsed only), the `campaign` send-count query, and reading an on-event trigger node, because neither project had an event-triggered scenario. `scripts/funnel_leaks.py` tested on fixtures) |
| **Maintainer** | Bloomreach |

## Example prompts

- "Where are we losing people between product page and purchase?"
- "How much revenue are abandoned carts costing us?"
- "Is mobile converting worse than desktop?"
- "Do we have an abandoned cart flow, and is it working?"

See [examples/illustrative-funnel.md](examples/illustrative-funnel.md) for an example output.

## Scripts

- `scripts/funnel_leaks.py` (Python 3 standard library, no network): reads the funnel counts, order value and optional segment funnels, and prints step conversion, customers lost, value walking away (an upper bound), recoverable value at a stated recovery rate, segment gaps and a purchase-step reliability check.

## Notes and limitations

- EQL funnels don't accept a `by` breakdown, so the skill runs one funnel per device or source value.
- Funnels and event-property breakdowns are rated "high" cost on most projects, so the skill asks once before running them.
- Many projects have no checkout event; the funnel then goes straight from cart to purchase.
- `total_price` on cart events is usually a running cart total, so the skill averages it rather than summing it.
- Default recovery rates are conservative assumptions, not benchmarks. Use your own flow results where you have them.
