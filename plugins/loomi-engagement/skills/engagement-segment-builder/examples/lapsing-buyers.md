# Example: lapsing buyers with consent (illustrative)

**This example is illustrative.** The method and the tool behaviour come from a live, read-only test run, but every project name, segment name and number has been changed or invented. No filter was created.

**Prompt:** "Build a segment of customers who bought in the last 90 days but not in the last 30, and who have newsletter consent. How big is it?"

## Audience: Lapsing buyers (newsletter consent)

**Definition**
- Made a purchase in the last 90 days
- AND NOT made a purchase in the last 30 days
- AND has consent for the *newsletter* category

**Mapped to:** event `purchase`; consent category `newsletter` (from the project's consent settings). There's no consent property on the customer profile, so the consent check uses the consent category, not a property.
**Reuses / overlaps:** The segmentation *Purchase recency* has a "31–90 days" segment that matches the first two conditions, so the new definition builds on it. Nothing similar exists for consent.

**Estimated size:** about 48,000 customers (as of 2026-10-08 10:15 UTC; EQL cost: medium)

**EQL**

    select count customers by customer.country grouping top 3 with null
      customers matching exists[event purchase in last 90 days]
        and not exists[event purchase in last 30 days]
        and has consent newsletter

**Build it in the UI**
1. Go to **Analyses → Segmentations → + Create new** and name it "Lapsing buyers (newsletter consent)".
2. Add a segment called "Lapsing, consented".
3. Add the condition **Segmentation → Purchase recency → equals "31–90 days"**.
4. Add **Consent → newsletter → granted**.
5. Combine them with **AND**, save, and compare the count with the estimate (about 48,000).

**Assumptions and gaps:**
- "Bought" is taken as the `purchase` event. The project also tracks an item-level purchase event, which isn't used here.
- The shape of the consent condition in the API couldn't be copied from an existing filter, so creating this through Loomi Connect would leave consent out. Build it in the UI instead, or create it without consent and add consent in the UI.

---

### What happened when the count was zero (from testing, numbers changed)

In a sandbox project, the same query returned an empty `rows` list. Counting `exists[event purchase]` on its own (lifetime) returned about 900 customers, so the definition was fine: the sandbox simply had no purchases in the last 90 days. The skill reports this as "no recent data", not as a broken definition.
