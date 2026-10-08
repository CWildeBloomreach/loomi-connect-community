# Example: weekly digest (illustrative)

**This example is illustrative.** The project, campaign names and all figures are invented to show the output format. They do not come from a real project. The method was tested live, but the test projects had too little campaign volume to make a meaningful example.

**Prompt:** "How did our emails and texts do last week?"

## Campaign digest: example_retail_prod, 21–27 Sep (vs 14–20 Sep)

**Headline:** Email volume rose 6% and clicks held steady, but the Spring Sale launch had a 5% bounce rate and above-normal unsubscribes.

| Channel | Sent | Delivered | Delivery % | Opens* | Clicks* | Click % | Unsubs | Bounces | Change in sends |
|---|---|---|---|---|---|---|---|---|---|
| Email | 87,400 | 84,336 | 96.5% | 31,800 | 3,050 | 3.6% | 339 | 2,540 | +6% |
| SMS | 12,200 | 11,950 | 98.0% | — | 610 | 5.1% | 44 | — | -3% |

*Event counts, not unique customers.

**Best campaigns:** 1. Welcome Series 1: 10.2% click rate on 4,040 delivered (up 30% on the week before). 2. Spring Sale Launch: 4.1% on 29,200. 3. Weekly Newsletter: 2.8% on 50,800.
**Worst campaigns:** Weekly Newsletter: click rate down 11% week on week, on the largest send.
**Issues to look at:**
- High bounce: Spring Sale Launch, 5.0% of sends (1,300 hard bounces). It went to a newly imported audience. Check the list source and suppress hard bounces before the next send.
- High unsubscribe: Spring Sale Launch, 0.72% of delivered. It's likely to be the same audience. Consider a softer re-permission email for it.
- Low volume: Back in Stock (296 delivered) is not ranked, because its rates are noisy.
**Revenue:** Not available from Loomi Connect for this project. See the campaign evaluation dashboard in Engagement.
**Coverage notes:** 7 EQL queries (all scored "high"), no saved campaign report found, and the per-campaign comparison covers email only.
