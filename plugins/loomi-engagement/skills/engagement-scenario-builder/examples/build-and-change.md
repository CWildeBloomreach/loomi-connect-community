# Example: build a flow, then change it

Illustrative. Names and numbers are made up.

## Prompt

> Build an abandoned cart flow: when someone updates their cart, wait 4 hours, and if they still haven't bought, email them.

## Before saving

```
## New scenario: Abandoned cart (draft)

**Starts:** when a customer tracks `cart_update` (30 seconds after the event)
**Who qualifies:** has an email address, and hasn't tracked `purchase` in the last day
**Steps:**
1. Wait 4 hours
2. Condition "Still not bought": matches → the cart reminder; doesn't match → the flow ends
**Messages:** "Cart reminder" email copied from the scenario "Cart reminder 2024" (design kept)

**Checks:** passed (5 steps, 4 connections)

Shall I create this as a draft in "Example Store (production)"?
```

## After "yes"

```
**Saved as:** 0123456789abcdef01234567. It's a draft: switch it on in Engagement when it's ready.
```

## Change

> Make the wait 6 hours instead.

The skill fetches the draft with its designs, checks it's still a draft and that no one else has edited it, changes the one wait (keeping every other step and id), shows "Changes the wait from 4 hours to 6 hours", and updates it after "yes".
