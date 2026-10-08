# Example: rule audit (demo apparel account)

The account name has been changed to a placeholder. The findings come from a real read-only run against a demo account. Rule IDs and user names are left out. This is an abridged version of the output: the full list has about 50 rows.

**Prompt:** "Can you audit our merchandising rules and tell me what to clean up?"

## Discovery rule audit: example_apparel (account level, 8 Oct 2026; traffic: last 90 days)

**Summary:** 150 rules: ranking 76 (34 search, 29 category, 13 global), media 67 (42 search, 22 category, 3 global), facet 4, redirect 3. 17 experiments: none running, 2 drafts. 5 rules need fixing now, about 30 can be cleaned up, and a handful need review.

### Fix now
| Rule | Type | Query / category | Issue | Evidence | Action |
|---|---|---|---|---|---|
| "Summer Beauty Sale" | Category ranking | 100000 (health & beauty) | Expired but still on | Ended 20 Sep 2026; enabled; another enabled rule targets the same category | Disable, then delete |
| "28 Oct to end Nov rule TEST DO NOT DELETE" | Search ranking | luxury evening dress | Expired but still on; protected name | Ended Nov 2025; query has no searches | Ask the owner, then disable |
| "dress CK example" | Search media | dress | Expired but still on | One-day banner from Jul 2026 | Delete |
| "dresses low value" | Search media | dresses | Expired but still on | Ended May 2026 | Delete |
| "Honeymoon Edit Campaign" | Category media | 20800 (shoes) | Expired but still on | Ended Feb 2026 | Delete |

### Clean up
| Rule | Type | Query / category | Issue | Evidence | Action |
|---|---|---|---|---|---|
| (unnamed) | Search ranking | backpack | Targets a wording nobody uses | Exact match; "backpack" has 0 searches, "backpacks" has 1,196 | Retarget to "backpacks" |
| "Linen boost" and 5 more | Search ranking | long dresses, purses, kids shoes, motion shoes, … | Enabled on queries with no searches | Not in the 860-query table | Check match type; retarget or delete |
| "Skins", "Barbour", "KG - Personalized In Grid" and 4 more | Search media | bb cream, bag, … | Banners on queries with no searches | Not in the query table | Delete, or move to a query with traffic |
| "Skirts black Friday" | Search media | skirts | Seasonal name, no end date | Enabled since Aug 2026; 17 searches in 90 days | Add an end date |
| 2 rules | Category ranking | 80000 (handbags) | Two enabled rules, same category | Created minutes apart by the same person | Fetch both; merge if the same audience |
| 2 rules each | Category ranking | 21000, 90000, 90200 | Two enabled rules per category | As above | Fetch both; merge if the same audience |
| 2 rules | Category facet | 90200 (necklaces) | Two enabled facet rules | Created 12 seconds apart | Fetch both; keep one |
| 6 rules | Search and category ranking | shirts, clothes, categories 90000, 10600, … | Disabled and never synced | `syncStatus` null | Delete |
| "Search terms - pretty blue shirt" | Experiment (draft) | pretty blue shirt | Can't start | Its rule returns 404 (deleted); draft for 17 months | Delete the draft in the Dashboard |

### Review
| Rule | Type | Query / category | Issue | Evidence | Action |
|---|---|---|---|---|---|
| 2 rules | Search ranking | dress | Two enabled rules | Checked: one default, one targets an audience. This is personalisation, not a conflict | None |
| 2 rules | Search ranking | shirt | Two enabled rules | One targets "High Value" shoppers; check the other | Confirm the audiences |
| 4 rules | Global ranking | * (global) | Four enabled global rules | Only one may be un-targeted; the list doesn't show audiences | Confirm each one's audience |
| "Search terms - casual tops", "test" | Experiment (completed) | casual tops, category 30100 | Ran for 9 and 30 seconds | Trial runs | Archive |

**Protected rules (ask the owner):** 16 rules are named "do not delete", "do not change or remove please" or similar, including both "dress" ranking rules and 7 disabled global rules. Two of them ("panthere jewelry", and the long "tote bag" query) also get no searches.
**A/B tests:** none are running, so nothing is blocked. Completed tests match their declared winners: the backpacks rule (winner) is on, and the shirt rule (loser) is off. The [readout skill](../../discovery-experiment-readout/) shows the backpacks win wasn't statistically conclusive, though.
**Healthy:** 3 redirects (about us, download app or mobile app, and tryin). Their destinations weren't checked in this run. Redirects don't appear in search traffic, so they weren't judged on it. The single global facet rule is fine.
