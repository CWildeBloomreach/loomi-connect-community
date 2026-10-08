# Action playbook

Turn the briefing's evidence into **three** actions for the week. Choose by money at stake, then by how easy the action is. Every action names the skill that does it.

## Signals and actions

| Signal in the briefing | Action | Skill |
|---|---|---|
| A core pixel type is RED, or the trend has missing or $0 days | Fix tracking before trusting the numbers | `data-feed-health` |
| Latest product feed or index failed, or product count fell 10%+ | Get the feed fixed and re-run | `data-feed-health` |
| Revenue moved more than about 5%, or the user wants to know why | Find out what drove it | `revenue-anomaly-explainer` |
| A high-revenue query fell (conversion, AOV or bounce got worse) | Diagnose the query | `discovery-query-diagnosis` |
| A query is rising fast but converts or bounces badly | Fix it while demand is high | `discovery-query-diagnosis` |
| Several related queries rising (a theme) | Act on the demand: merchandise it, or build an audience and campaign | `discovery-trending-searches`, then `search-demand-to-campaign` |
| Zero-result or no-revenue queries are among the movers | Triage dead-end searches | `discovery-zero-results-triage` |
| A category fell, or category conversion dropped against search | Check the category page | `discovery-category-health` |
| A brand or product fell sharply while its category held up | Check stock, price and ranking for it | `discovery-category-health` (buried products) or `discovery-query-diagnosis` on its main query |
| A rule was edited or a scheduled rule started or expired near a big move | Review the rule | `discovery-rule-audit` |
| An A/B test is running or just ended | Read it out and decide | `discovery-experiment-readout` |
| A ranking change looks worthwhile but risky | Test it first | `discovery-experiment-setup` |
| Email click rate fell, or a bounce or unsubscribe flag fired | Look at the campaigns | `engagement-campaign-digest` |
| Several sends to the same audience in the coming week | Check for over-messaging | `engagement-send-collision-check` |

## Estimating money at stake

Keep it simple and label it as an upper bound:

- **A falling query, category, product or brand:** its revenue change this week (from the movers table).
- **A rising query that converts badly:** sessions × (typical conversion of top queries − its conversion) × its AOV.
- **A data problem:** don't put a figure on it. Put it first, because it affects every other number.

## Writing the action

One line each: **what to do**, with the specific query, category, product, brand or campaign; the evidence in a few words; and the skill.

> 1. **Diagnose "diamond" search**: −$35k this week, AOV $354 → $341 while conversion held. → `discovery-query-diagnosis`

Avoid generic advice ("improve search relevance"). If fewer than three actions have real evidence behind them, list fewer and say the rest of the week looks steady.
