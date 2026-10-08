# Recovery flows: what to look for

Three flows recover most funnel revenue. For each, this lists how to find it, what "active" looks like, and the signs of a weak one.

## Finding them

1. `search_scenarios` with `trigger_types=["onevent"]` returns scenarios with an on-event trigger, of any status. Add `status="active"` to see which are live. The list records **don't show the trigger type or event**: the filter is the only way to find them without opening each one.
2. Also try `trigger_types=["repeated"]`: some teams run abandonment as a daily batch against a segment ("added to cart in the last 24 hours and didn't buy").
3. Open each candidate with `search_scenario_nodes` (via `call_tool`): no `node_id` for the graph map, then the `on-event-trigger` node by `node_id` for its event type and filters. Use node types from the `engagement-scenario-explainer` skill.
4. Names help you shortlist, but confirm from the trigger. A flow named "Cart abandonment" that triggers on `session_start` isn't one.

In testing, a production project with several active scenarios had **none** triggered by an event, so no cart, browse or post-purchase flow existed. That is common enough to check first.

## Cart or checkout abandonment

| | |
|---|---|
| Trigger | On event `cart_update` (often filtered to `action` = `add`) or `checkout`; or a repeated trigger on a segment of recent cart adders |
| Shape | Wait (typically 1–4 hours) → condition: has the customer bought since? (an event condition on `purchase`) → if not, send → optional second wait and send |
| Active | Scenario `active`, trigger on the right event, at least one email, SMS or push node on a connected path |
| Weak | Inactive, draft or paused; first send more than about 24 hours after the cart; no purchase check before each send (people who bought still get reminders); one channel only; no consent category on the message |

## Browse abandonment

| | |
|---|---|
| Trigger | On event `view_item` (sometimes `view_category`), usually limited by a frequency cap or `limit` node |
| Shape | Wait (several hours to a day) → condition: no cart add and no purchase since → send with the viewed products |
| Active | As above |
| Weak | First send more than about 48 hours later; no limit, so heavy browsers get many messages; no check for cart or purchase |

## Post-purchase

| | |
|---|---|
| Trigger | On event `purchase` |
| Shape | Order confirmation or thank-you; then cross-sell or replenishment after days or weeks; review request after delivery |
| Active | As above |
| Weak | Only transactional confirmation (often sent by the shop platform, not Bloomreach); no follow-up for cross-sell or review |

Post-purchase flows don't fix a funnel leak, but they're where repeat revenue comes from. Report them as present or missing without a figure.

## Hand-offs

- **Define the audience for a new or better flow:** `engagement-segment-builder`, for example "added to cart in the last 24 hours, didn't buy, has email consent". It sizes the audience and asks before creating anything.
- **Explain or audit an existing flow:** `engagement-scenario-explainer`, which walks the nodes and checks for broken references.
- **Purchase step can't be measured:** `engagement-tracking-health`, to check purchase tracking and identity.
