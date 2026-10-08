# Customer 360 lookup

Summarises one customer in a Bloomreach Engagement project for support and account teams. You give it an identifier (email, customer ID or another ID). It finds that one customer and returns a short customer card, a recent event timeline, prediction scores, current recommendations, and the things support should know: failed orders, bounces, unsubscribes and consent. It's built around privacy: one named customer at a time, sensitive data masked by default, nothing saved to files, and it never changes anything.

| | |
|---|---|
| **Products** | Engagement |
| **Access** | Read-only (reads personal data for one customer) |
| **Loomi Connect tools** | `list_cloud_organizations`, `list_projects`, `get_customer_schema`, `list_customers` (always with a query), `get_customer_properties`, `list_customer_events`, `search_predictions`, `get_customer_prediction_score`, `search_recommendations`, `get_customer_recommendations`, optionally `get_customer_property_schema`, `search_segmentations`, `get_consent_settings` (via `call_tool`) |
| **Tested with** | Claude Code, October 2026, read-only, against a sandbox project only: project resolution, `get_customer_schema`, `get_customer_property_schema`, `search_predictions` (returned 403), `search_recommendations` (no engines), `get_consent_settings` via `call_tool`, and `list_customers` with a single-row call and a no-match query to check the response shape. **Not run live:** `get_customer_properties`, `list_customer_events`, `get_customer_prediction_score` and `get_customer_recommendations`. Reading a full customer profile was deliberately not done during development, so those steps follow the tool schemas and descriptions. Not run end to end, and not tested in an OpenAI client. |
| **Maintainer** | Bloomreach |

## Example prompts

- "Look up the customer jamie.rivera@example.com in our production project."
- "Customer 360 for customer ID 0123456789abcdef01234567: why didn't they get the order confirmation?"
- "Has this customer unsubscribed from email? Their address is …"
- "What would our homepage recommendations show this customer?"

See [examples/illustrative-lookup.md](examples/illustrative-lookup.md) for an example output. The customer and everything in it are fictional.

In OpenAI clients (Codex, ChatGPT), implicit invocation is turned off in `agents/openai.yaml` because the skill reads personal data. It runs only when you call it by name: `$customer-360-lookup` in Codex, `@customer-360-lookup` in ChatGPT. In Claude clients it can load when a request matches its description.

## How it works

1. **Find the customer:** reads the project's identifier types with `get_customer_schema`, then searches `list_customers` for the exact identifier given (at most 5 results). If several match, it asks which one rather than showing them all.
2. **Profile:** picks the relevant properties from `get_customer_properties` and masks personal data. See [references/privacy-and-masking.md](references/privacy-and-masking.md).
3. **Timeline:** the last 90 days of events, plus targeted look-backs for orders, message delivery (`campaign`) and `consent` events, collapsed into one line per day for browsing activity.
4. **Predictions and recommendations:** scores for up to 3 prediction models, and the top 5 products from a recommendation engine the user picks.
5. **Things support should know:** failed or cancelled orders, bounces, complaints, unsubscribes, consent withdrawn, unreachable channels. See [references/support-signals.md](references/support-signals.md).

## Notes and limitations

- **Privacy:** the skill only looks up a customer the user identifies, never lists or exports customers, masks emails, phones, addresses and external IDs by default, never shows payment or special-category data, and doesn't write customer data to files. Every answer ends with a personal-data reminder.
- **Backend masking isn't enough.** Loomi Connect masks only fields marked as personal data, and only for users without the PII permission. In testing, emails came back unmasked and the property schema's `private` flag was off for email and name fields, so the skill masks values itself.
- **Segment memberships:** there's no tool that lists one customer's segments, and the skill won't list segment members to find out. If asked about a specific segment, it compares the segment's definition with the customer's data and labels the answer as an inference.
- **Recommendations need an external ID.** `get_customer_recommendations` takes the identifier value (for example the email) and its type, not the internal ID. Its default type, `registered`, doesn't exist on every project (the test project used `email_id`), so the skill passes the type from `get_customer_schema`.
- `search_predictions` returned HTTP 403 in testing. The skill reports predictions as unavailable and carries on.
- Event and property names vary by project. The support signals are common conventions, not guarantees.
- It can't fix, unsubscribe, merge, anonymise or delete customers. Use the Engagement UI or your data-protection process for that.
