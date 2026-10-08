# Creating campaign drafts

`create_email_campaign` and `create_sms_campaign` **always create a draft**. A person has to activate it in the Engagement UI before anything is sent. Even so, a draft is a real object in the customer's project. Create one only after the user has seen the full payload and said yes.

These payload shapes come from the tools' own descriptions. **This skill's authors have not tested creating campaigns.** Before building a payload, load the tool's schema and description again, and follow it if it differs from this page.

## Before you build anything

1. **Consent:** call `get_consent_settings`. If it isn't listed, find it with `search_tools` and run it with `call_tool`. If `general_consent.email` is `false`, an email campaign **must** include a `consent_category` (one of the category `id`s), or the call fails with HTTP 400. Do the same check for `sms`.
2. **Audience:** campaigns take an inline `customer_filter` with `filters` and `formula` keys. The API **can't reference a saved filter by ID**. The safe way to build one:
   - ask the user to create the audience as a saved **customer filter** in the Engagement UI (for example, "searched for capris in the last 30 days, has email");
   - fetch it with `search_customer_filters` and the `customer_filter_id`;
   - copy its `filters` and `formula` into the payload unchanged.

   **Never create a draft without a `customer_filter`** unless the user explicitly accepts that it would target everyone when activated. If you do, put "NO AUDIENCE SET" in the campaign name.
3. **Content:** read the guide resource `loomi://guides/email-template-best-practices` (or `loomi://guides/sms-template-best-practices`) if the client can read MCP resources. It covers Jinja personalisation, subject lines, SMS length and the opt-out wording.
4. **Schedule:** prefer `{"type": "datetime", "datetime": <unix seconds>}` at a time agreed with the user. `{"type": "now"}` sends the moment someone activates the draft.

## Email skeleton

```json
{
  "name": "[Search demand] capris – now in stock – DRAFT",
  "schedule": {"type": "datetime", "datetime": 1767225600},
  "customer_filter": {"filters": ["<copied from saved filter>"], "formula": "<copied>"},
  "consent_category": "<category id, if required>",
  "split": {
    "type": "off",
    "variants": [{
      "design": {
        "type": "raw",
        "data": {
          "sender_name": "<brand>",
          "sender_email": "<verified sender address>",
          "subject": "Capris are here",
          "jinja_html": "<html>…Hi {{ customer.first_name | default('there') }}…</html>"
        }
      }
    }]
  }
}
```

## SMS skeleton

```json
{
  "name": "[Search demand] capris – now in stock – DRAFT",
  "schedule": {"type": "datetime", "datetime": 1767225600},
  "customer_filter": {"filters": ["<copied>"], "formula": "<copied>"},
  "split": {"type": "off"},
  "action": {
    "variants": [{
      "type": "sms",
      "translations": {
        "": {
          "message": "<Brand>: capris just landed. Shop: <link> Reply STOP to opt out",
          "sender": {"name": "<Brand>", "sender": "<Brand>"}
        }
      }
    }]
  }
}
```

- Use the empty-string language key `""` for the default language.
- `sender.sender` must be 1–11 alphanumeric characters, or a phone number.
- Leave out `sender.sms` to use the project's default provider.

## Event-triggered alternative (not tested)

An ongoing "you searched for X" message can be triggered by an event rather than sent once: `schedule: {"type": "event", "event": <EventFilter>}`, using `type` (not `event_type`) for the event name. The EventFilter format isn't documented in the tool's description. Unless the user knows it, suggest building triggered flows as a **scenario** in the Engagement UI.

## After creating

Report the returned campaign ID and tell the user it's a **draft**. Before activating it in the UI, they should check the audience size, the preview and the consent.
