# Example: project access review (illustrative)

**This example is fictional.** The method, fields and tool behaviour come from a live, read-only test run, but the organisation, projects, every person, every email address and every number are invented. Nothing was changed.

**Prompt:** "Run our quarterly access review across our Bloomreach Engagement projects. Our domain is example.com, and Northwind Agency (northwind.example) runs our campaigns."

---

## Project access review: Example Store, 2026-10-08

> Confidential: this review lists people's names and email addresses. Keep it internal, share it only with the people running the review, and delete working copies when the review is closed.

**Verdict:** 23 people can access 3 projects. Production has a shared `marketing@` login and one personal Gmail account; 5 actions are recommended.

**Scope:** Example Store - PROD, Example Store - SANDBOX, Example Store - EU PROD; company domain example.com; vendor domains northwind.example and the Bloomreach domain (you confirmed both); checked against the leavers list you pasted (4 names).

### Summary by project
| Project | Category | Users | Company | Vendor | External | Shared or test | Role labels |
|---|---|---|---|---|---|---|---|
| Example Store - PROD | prod | 17 | 10 | 6 | 1 | 2 | none 11, Marketing Manager 3, Developer 2, Other 1 |
| Example Store - SANDBOX | sandbox | 14 | 6 | 8 | 0 | 3 | none 9, Developer 4, Internal User 1 |
| Example Store - EU PROD | prod | 6 | 5 | 1 | 0 | 0 | none 5, Marketing Manager 1 |

### Access review
| User (email) | Domain type | Projects | Role label(s) | Flags |
|---|---|---|---|---|
| marketing@example.com | company | PROD, SANDBOX | none | shared account; no name |
| jo.rivera.design@gmail.example | external (webmail) | PROD | Other | personal webmail |
| chris.okafor@example.com | company | PROD, EU PROD | Marketing Manager | on leavers list |
| qa.tester+1@example.com | company | PROD, SANDBOX | Developer | test alias |
| dana.wells@northwind.example | vendor | PROD, SANDBOX, EU PROD | Developer | 3 projects |
| lee.park@northwind.example | vendor | PROD, SANDBOX | none | vendor in prod and sandbox |
| api-sync@example.com | company | SANDBOX | none | shared account |

The other 16 users are named company or vendor accounts with no flags (PROD 11, SANDBOX 9, EU PROD 4, counting each project). Ask for the full table if you need it for your records.

### Recommended actions (for a human, in the Bloomreach UI)
| # | Action | User(s) | Project | Why |
|---|---|---|---|---|
| 1 | Remove | chris.okafor@example.com | PROD, EU PROD | On your leavers list |
| 2 | Remove, or replace with a company account | jo.rivera.design@gmail.example | PROD | Personal webmail in production; nobody at Example Store vouches for it |
| 3 | Replace with named accounts, then remove | marketing@example.com | PROD, SANDBOX | Shared login: changes can't be traced to a person. Check first that no integration signs in with it |
| 4 | Remove from PROD | qa.tester+1@example.com | PROD | Test alias in production |
| 5 | Confirm with Northwind that production access is still needed | dana.wells@northwind.example, lee.park@northwind.example | PROD, EU PROD | Vendor access to every production project |

### Couldn't check
- Permission levels: `role` is a job-role label (mostly empty), not an access level, so the number of administrators isn't known. Check access levels in each project's access management in the UI.
- Last login: not returned by Loomi Connect. Nobody has been called inactive; export last-login dates from the UI if you want that check.
- `api-sync@example.com` in the sandbox looks like an integration account; ask its owner whether it should be an API key instead.
