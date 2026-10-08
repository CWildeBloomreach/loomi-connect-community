# Example: tracking audit (illustrative)

**This example is illustrative.** The kinds of problem it shows were all found in a real run against a live Engagement project, but the project, event and property names have been replaced with placeholders, and every number has been changed.

**Prompt:** "Is our Engagement tracking healthy? Something feels off with the data."

## Tracking health: example-project (sandbox), last 7 days

**Verdict:** Web tracking is flowing normally, but purchase events have been silent for over 90 days, and the production schema is polluted by about 110 junk event types that look like injected scanner traffic.

### Event volumes (last 7 days vs previous 7 days)
| Event type | Last 7d | Prev 7d | Change | 90-day weekly avg | Status |
|---|---|---|---|---|---|
| purchase | 0 | 0 | — | 0 | **Silent**: nothing in 90 days |
| purchase_item | 0 | 0 | — | 0 | **Silent** |
| page_visit | 12,840 | 12,410 | +3% | 4,620 | **Spiked vs 90-day average**: tracking widened recently? |
| view_category | 71 | 118 | −40% | 112 | **Dropped** (low volume, so watch it) |
| session_start / session_end | 3,910 / 3,880 | 3,600 / 3,570 | +9% | — | OK, and the pair is balanced |
| 7 others | | | | | Healthy |

### Unexpected event types
- **About 110 junk event types**, almost all variants of one real event name with SQL-injection, shell or template-injection fragments appended (for example `session_ping' and '12'='12…`), plus a few random strings. The likely cause is a security scanner hitting the public tracking endpoint. Each is a real event type in the schema.

### Data quality
| Property | Fill rate | Issue |
|---|---|---|
| customer.country | **~82%** | ~16% are empty strings and ~2% null. Some values are postal or region codes, which suggests a column shift in an import |
| view_item.brand | 100% | A single value on every event, so it's useless for segmentation |
| conversational-widget event `search_text` | **0% in the last 7 days** | Marked `used` in the schema, but nothing recent |

### Schema oddities
- `price` is a **string** on view and purchase events, but a **number** on cart events. `purchase_id` and `variant_id` also have mixed types.
- `phone` and `postal_code` customer properties are **numbers**, so leading zeros and `+` are lost.
- Misspelt duplicates: `colour` / `color`, and `chat_id` / `chatid`.
- `propensity_score` is stored as a string.

### Recommended actions
1. **Confirm whether purchases should be arriving** (critical). Evidence: no purchase events in 90 days while sessions are healthy. Owner: integration owner (order import or API). Check by: rerunning step 3.
2. **Block and clean up the junk event types** (critical). Evidence: about 110 look-alike types. Owner: Engagement admin and security. Restrict the public tracking API where possible, then delete the types in the UI after checking nothing uses them.
3. **Fix the country import mapping** and convert empty strings to null (high). Owner: integration owner.
4. **Standardise `price` as a number** across events (high). Owner: web developers.
5. **Merge the misspelt duplicate properties**, and retype phone and postal code as strings (medium). Owner: Engagement admin.
