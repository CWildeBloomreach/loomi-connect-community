# Discovery experiment readout

Summarises running and completed Bloomreach Discovery A/B tests. It covers the variants, traffic split, success metric, results, lift, confidence and the declared winner. It then says in plain English whether the result is real, and recommends **Ship it**, **Keep running** or **Stop**. It also checks whether a declared winner was actually supported by the data. It never changes anything.

| | |
|---|---|
| **Products** | Discovery |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `search_discovery_experiments`, `get_discovery_experiment_report`, `get_ranking_rule` (optional), `search_redirects` (optional) |
| **Tested with** | Claude Code (manual run of the method against a demo account with completed, archived and draft experiments; no running experiment was available) |
| **Maintainer** | Bloomreach |

## Example prompts

- "How is our A/B test on 'dresses' doing?"
- "Read out our completed experiments. Did the winners really win?"
- "Is the backpacks ranking test significant yet? Should we ship it?"

See [examples/completed-tests.md](examples/completed-tests.md) for a full example output.

## Notes and limitations

- The report response is very large, so the skill includes `scripts/summarise_report.py` (Python standard library, no network) to summarise the saved file.
- The success metric and winner only appear when an experiment is fetched by ID, not in the list.
- Confidence is a "chance to be best" from 0 to 1, per bucket. When there's too little data it comes back as 0 for every bucket; the skill treats that as "not calculated".
- Reports for older experiments (about 8 months or more) can come back empty. The report can also start later than the requested date. The skill reports the period actually covered.
- Readouts of a RUNNING experiment follow the same method but were not tested live, because none was running.
