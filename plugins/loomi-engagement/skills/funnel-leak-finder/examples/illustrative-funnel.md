# Example: funnel leaks (illustrative)

**This example is illustrative.** The method, the query shapes and the kinds of finding come from read-only runs against a real Engagement organisation, but the project name, segment values and every number have been invented. Real runs showed two of the situations below: a sandbox with no purchases at all, and a production project whose purchase step didn't link to browsing (see the second example).

## 1. A funnel with a measurable purchase step

**Prompt:** "Where are we losing shoppers between product page and checkout, and what's it worth?"

## Funnel leaks: example-retail-prod, last 30 days (conversion window 7 days)

**Verdict:** Most recoverable value sits in abandoned carts (about $12,000 a month at an assumed 5% recovery), and there's no active cart abandonment flow. iOS shoppers convert at half the rate of desktop.

| Step | Customers | Step conversion | Lost | Value walking away | Recoverable (assumed rate) |
|---|---|---|---|---|---|
| Viewed a product | 28,500 | — | | | |
| Added to cart | 4,100 | 14.4% | 24,400 | up to $561,000 | about $5,600 (1%) |
| Purchased | 1,150 | 28.0% | 2,950 | up to $242,000 | about $12,100 (5%) |

**Biggest gaps by OS:** iOS: 2.0% end to end vs 4.0% overall, up to $15,000. Its view-to-cart rate (10%) is the weak step, which points at the mobile product page rather than checkout.
**Abandoned carts:** 2,950 customers, average cart $95, about $280,000 left in carts (upper bound).
**Data caveats:** no `checkout` event is tracked, so cart and checkout abandonment can't be separated. Purchase step checked: the funnel's buyers are 88% of all purchasers in the window.

### Recovery flows
| Flow | Status | Evidence | Leak it addresses |
|---|---|---|---|
| Cart abandonment | Weak | "Basket reminder" triggers on `cart_update` but is **inactive** | about $12,100 |
| Browse abandonment | Missing | no scenario triggers on `view_item` | about $5,600 |
| Post-purchase | Active | "Order thank-you" triggers on `purchase`, email only, no cross-sell step | — |

### Next steps
1. **Reactivate and fix the cart abandonment flow**: first send 2 hours after the cart, with a purchase check before each send. Hand-off: `engagement-scenario-explainer` to audit "Basket reminder" before switching it on.
2. **Build a browse abandonment flow** for customers who viewed but didn't add to cart in 24 hours. Hand-off: `engagement-segment-builder` for the audience, with email consent.
3. **Look at the iOS product page** (add-to-cart button, image load). This is a site issue, not a messaging one.

## 2. When the purchase step can't be trusted

**Prompt:** "What's our cart-to-purchase conversion?"

**Verdict:** It can't be measured from this data. 5,000 customers added to cart in the last 7 days, but only 30 of them bought within a day, while 1,500 customers bought in the same week. Purchases are almost certainly recorded under a different customer identity from browsing (for example server-side orders not merged with the web visitor). Fix the tracking before trusting any cart-abandonment figure.

| Step | Customers | Step conversion |
|---|---|---|
| Viewed | 40,000 | — |
| Added to cart | 5,000 | 12.5% |
| Purchased | 30 | not reliable (2% of all purchasers) |

**Next step:** run `engagement-tracking-health`, and check which identifier the purchase events use and whether orders are imported. No recovery flows triggered by an event exist, so once purchases link up, a cart abandonment flow is the first thing to build.
