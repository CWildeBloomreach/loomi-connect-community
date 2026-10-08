# Example: customer 360 lookup (fictional)

**This example is entirely fictional.** The project, the customer, every identifier, order, campaign, product and number are invented. It shows the output format only.

**Prompt:** "Can you look up the customer with email jamie.rivera@example.com in our production project? They say they never got their order confirmation and stopped getting our emails."

---

## Customer 360: j***@e***.com (Example Store, production)

**In one line:** A loyal Gold-tier customer whose last order failed on payment (so no confirmation was sent), and whose emails stopped after a hard bounce on 2026-09-14.

### Customer card

| Field | Value |
|---|---|
| Internal ID | 0123456789abcdef01234567 |
| Identifiers | email_id: j***@e***.com (hard) · cookie: present (soft) |
| First name | Jamie |
| Customer since | 2023-03-02 |
| Location | Leeds, United Kingdom |
| Membership | Gold (`loyalty_tier`) |
| Orders / lifetime value | 14 orders, £1,180 (`total_orders`, `lifetime_value`) |
| Last successful purchase | 2026-08-21 |
| Channels | Email: opted in, but address bouncing · SMS: not opted in · Push: no token |

### Things support should know

1. **Last order failed:** order EX-10482 (£86.40) on 2026-10-05 has status `failed` (payment declined). No `success` status followed, so no confirmation email was triggered.
2. **Email hard bounce:** the "September new arrivals" email on 2026-09-14 hard-bounced. No emails have been delivered since, including order and marketing emails. Ask the customer to confirm their address.
3. **Consent is fine:** latest `newsletter` consent is `accept` (2025-11-30, no expiry). The problem is deliverability, not consent.
4. **Two checkout attempts** on 2026-10-05 within 10 minutes, both before the failed purchase.

### Recent timeline (last 90 days, newest first, UTC)

| Date | What happened |
|---|---|
| 2026-10-05 | Purchase EX-10482 failed: payment declined, £86.40 |
| 2026-10-05 | 2 checkouts, 4 page visits, 6 product views |
| 2026-09-28 | Email "Autumn edit": not sent (`suppressed`, hard-bounced address) |
| 2026-09-14 | Email "September new arrivals": **hard bounce** |
| 2026-09-02 | Email "Gold member early access": delivered, opened, clicked |
| 2026-08-21 | Purchase EX-10211 successful: £42.00 |
| 2026-08-21 | Email "Your order is confirmed": delivered, opened |
| 2026-07-30 to 2026-08-20 | 9 sessions, 31 product views |

### Predictions

- Churn risk: 0.18 (low), updated 2026-10-07
- Purchase propensity (30 days): 0.71 (high), updated 2026-10-07

### Current recommendations (Personalised homepage engine)

1. Merino crew jumper, navy (SKU-0001)
2. Merino crew jumper, grey (SKU-0002)
3. Wool beanie (SKU-0107)
4. Cashmere scarf (SKU-0213)
5. Leather gloves (SKU-0300)

### Segments

Not requested.

*Masked by default. Ask if you need a specific full value for this task.*
*This contains personal data. Share it only with people who need it, and don't paste it into tickets or chats that don't need it.*
