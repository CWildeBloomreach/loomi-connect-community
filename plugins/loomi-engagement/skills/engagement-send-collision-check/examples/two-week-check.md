# Example: two-week collision check (illustrative)

**This example is illustrative.** The project, campaign names, segments, times and figures are invented to show the output format. The method and the calendar, scenario, segmentation and frequency-policy response shapes were checked against a live project, but that project had too few scheduled sends to make a meaningful example.

**Prompt:** "Are any of our sends clashing over the next two weeks?"

## Send collision check: example_retail_prod, 21 Sep – 4 Oct (UTC-4)

**Verdict:** One likely collision and one channel conflict, both on Tuesday 22 Sep. The project's default frequency policy is unlimited, so nothing stops them stacking up.

| Day | Sends | Email | SMS | Flag |
|---|---|---|---|---|
| Tue 22 Sep | 5 | 3 | 2 | busy day, email + SMS |
| Tue 29 Sep | 1 | 1 | 0 | |
| Thu 1 Oct | 2 | 2 | 0 | |

### Collisions
1. **Weekly Newsletter → Autumn Sale / Launch email**: 4 h apart, both email, overlap. Audience: all email subscribers vs RFM "Engaged". Reach: 50,000 / 30,000. Cap: unlimited. Suggest: move the sale launch to Wednesday, or feature the sale in the newsletter.
2. **Autumn Sale / Launch email → Autumn Sale / Launch SMS**: 2 h apart, email and SMS, same audience (RFM "Engaged"). Reach: 30,000 / 9,000. Suggest: send the SMS only to people who haven't opened the email by the next morning.
3. **VIP Preview → Weekly Newsletter**: 1 h apart, both email, overlap, because the newsletter goes to everyone. Reach: 2,000 / 50,000. Suggest: exclude VIP Preview recipients from this week's newsletter.

**Background load (always-on flows):** Welcome Series (on event: registration, email), Abandoned Cart (on event: cart_update, email and SMS), Birthday (on date attribute, email).
**Planned but not active:** "Old Draft", a repeating email planned for Tue 22 Sep 03:00, would add a fourth email that day if activated.
**Frequency caps:** Default policy is `unlimited-policy`. Newsletter and sale sends use it too. A "Smart Newsletter" policy exists but isn't used here.
**Not checked:** SMS campaigns outside scenarios (SMS not enabled for standalone campaigns: HTTP 403). Also flagged: "Late SMS" at 21:00 local time, at the edge of quiet hours.
