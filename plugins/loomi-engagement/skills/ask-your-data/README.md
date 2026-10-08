# Ask your data

Answers a plain-English analytics question about a Bloomreach Engagement project, such as "how many customers bought last month?", "what were the top search terms this week?" or "what share of visitors went on to buy?". It checks the project's event and customer schema so the query uses real names, asks when the question is ambiguous (which project, which dates, what counts as a purchase or an active customer), writes the EQL, estimates its cost, and asks before running anything rated high. It never runs a very high-cost query: it suggests a narrower one instead. The answer comes in plain English, with the exact EQL that ran and every assumption. It uses aggregate results only and never changes anything.

| | |
|---|---|
| **Products** | Engagement |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_cloud_organizations`, `list_projects`, `get_event_schema`, `get_customer_property_schema`, `estimate_eql_cost`, `execute_analytics_eql` (all listed directly; if a client doesn't show one, the skill finds it with `search_tools` and runs it with `call_tool`) |
| **Tested with** | Claude Code, October 2026, read-only against a sandbox project: project resolution, both schema tools, cost estimates for event counts, daily trends, customer counts and funnels, and four medium-rated queries run live (a one-step purchaser funnel, a customer count with a windowed `exists`, a two-step funnel with absolute dates, and a new-buyer count). No high-rated queries were run, so the sum, average, top-values and trend patterns are parsed or borrowed from other skills' testing and are labelled that way in [references/eql-patterns.md](references/eql-patterns.md). `scripts/summarise_eql.py` tested on synthetic responses. Not run end to end as one session, and not tested in an OpenAI client. |
| **Maintainer** | Bloomreach |

## Example prompts

- "How many customers bought something in the last 30 days?"
- "How many new customers did we get last month, and how many were returning?"
- "What's our average order value this month, by currency?"
- "What were the top 10 search terms last week?"
- "What share of people who started a session in September went on to buy within 7 days?"
- "Compare purchasers this week with last week."

See [examples/illustrative-answers.md](examples/illustrative-answers.md) for two example conversations, including one where the first query is too expensive. Their names and numbers are illustrative.

## How it works

1. **Project:** resolves the organisation and project, and asks if there's more than one.
2. **Question:** restates it as metric + event or property + filters + breakdown + date range, and asks about anything ambiguous, proposing defaults from [references/definitions.md](references/definitions.md) (for example "active customer = a session or purchase in the last 30 days").
3. **Schema:** checks every event and property name against `get_event_schema` and `get_customer_property_schema`, because the cost estimator doesn't check names.
4. **Query:** picks a pattern from [references/eql-patterns.md](references/eql-patterns.md), a library of tested EQL for counts, funnels, sums, averages, top values, trends, period comparisons, and new vs returning buyers, with the syntax traps.
5. **Cost:** `estimate_eql_cost` first. Low and medium run; high runs only after the user agrees; very high never runs, and the skill offers a narrower query.
6. **Answer:** a plain-English answer, a short table, the exact EQL, the as-of time and all assumptions. [scripts/summarise_eql.py](scripts/summarise_eql.py) totals every row (including null and "other"), sorts by value and works out funnel conversion (standard library only, no network).

It suggests hand-offs where they fit: `engagement-segment-builder` to turn an answer into a segment, `funnel-leak-finder` for multi-step funnel analysis, `engagement-tracking-health` when the data looks wrong, `engagement-campaign-digest` for campaign results, `engagement-report-explainer` for saved reports, and `winback-opportunity` for lapsed customers.

## Notes and limitations

- On large projects, most event-level metrics (event counts, sums, averages, top values, daily trends) are rated "high" by `estimate_eql_cost`, so expect the skill to ask before running them. Customer counts and funnels are often cheaper; the skill prefers them where they answer the question.
- EQL is limited to about one query every 3 seconds across the whole Engagement instance, shared with other users, so multi-query answers (period comparisons, several values) take a little while and may hit "Too many requests".
- Results are live, and today's data is usually incomplete. The skill gives the as-of time with every answer.
- Day and month breakdowns use the project's time zone; absolute dates in queries are UTC. The skill states which applies.
- It answers one question at a time. For a recurring report or a full analysis (funnel leaks, win-back sizing, campaign digests), use the dedicated skill.
- It never breaks down by personal or high-cardinality properties (email, phone, IDs, URLs), even if asked.
