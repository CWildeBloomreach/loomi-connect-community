# Project access review checks

Apply these to each user in each project. Report a finding only when the evidence supports it, and say what you couldn't check.

## Severity

- **Action:** likely a risk now. Remove, or replace with a named account, at this review.
- **Confirm:** may be fine; the project owner must say why the access is needed.
- **Review:** worth a least-privilege look.
- **Info:** worth knowing; no action on its own.

Raise the severity one step for **production** projects and lower it one step for **sandbox** projects (`category` from `list_projects`), but never below Info.

## What the tools return (as seen in testing)

| Tool | Fields | Notes |
|---|---|---|
| `list_project_users` | `_id`, `email`, `username`, `first_name`, `last_name`, `role` | Wrapped in `{"success": true, "data": [...]}`. No pagination; 60+ users came back in one call. `username` matched `email` in every record seen. `role` is a job-role label (Developer, Marketing Manager, E-commerce Manager, Internal User, Other) and is `null` for most users. No permission level, last login, invitation date or status |
| `list_projects` | `id`, `name`, `category` (`prod`, `sandbox`...), `url`, `url_slug`, `workspace_id`, `workspace_name` | Use `category` to weight findings |
| `get_cloud_organization_details` | `id`, `name`, `domain`, `enabled_modules`, `supervisor_email`, `internal_supervisor_email`, `salesforce_id` | `domain` was empty in testing. `enabled_modules` can include `SSO_LOGIN`. Never repeat the supervisor emails |
| `list_cloud_organizations` | `id`, `name`, `admin_panel_url`, `enabled_modules` | `admin_panel_url` is where an administrator manages users |

The organisation and project tools are limited to about 1 request per second; Engagement tools to about 3.

### Role labels

`role` describes what the person does, as chosen on their profile. It doesn't grant or limit anything. "Internal User" appeared only on Bloomreach-domain accounts in testing, so it probably marks Bloomreach staff; don't rely on it. Report the distribution of labels per project, and never present a label as a permission.

### Inferred account age

`_id` is a 24-character hex object ID. Its first 8 hex characters, read as a Unix timestamp, gave plausible dates (2021–2026) in testing. That's the creation time of the **user account**, not of the project membership, and it isn't documented. Use it only as context ("account created about 4 years ago, never named"), never as evidence of inactivity.

## Checks

### Domains

| Check | Rule | Severity | Suggested action |
|---|---|---|---|
| Personal webmail | domain is gmail.com, googlemail.com, outlook.com, hotmail.com, live.com, yahoo.com, icloud.com, me.com, aol.com, proton.me, protonmail.com, gmx.* or similar | Action | Remove, or replace with a company or vendor account |
| External | domain isn't a company or vendor domain (subdomains count as their parent) | Confirm | Ask the project owner who this is and why they need access |
| Vendor | domain is in the user's vendor list | Confirm (Review in sandbox) | Confirm the contract or support case is still open |
| Company | domain is a company domain | - | Only other flags apply |

When the organisation has `SSO_LOGIN` enabled, note that external and vendor users may sign in outside SSO, so leavers aren't removed automatically when your identity provider disables them. Say this as a possibility, not a fact.

### Shared, generic and test accounts

| Check | Rule | Severity |
|---|---|---|
| Shared or generic | local part (before @) is a function rather than a person: admin, administrator, api, automation, bot, crm, data, demo, dev, digital, ecommerce, email, hello, info, integration, it, mail, marketing, newsletter, noreply, ops, qa, sales, sandbox, service, shared, support, team, tech, test, user, web, webmaster, possibly followed by a number or suffix | Action (production), Review (sandbox) |
| Test or alias | local part contains test, qa, dev, demo, sandbox, tmp, temp, dummy as a separate word, or a `+tag` | Review (Action in production) |
| Single-word local part | a first name only, such as `sam@` | Info: often a real person at a small company; don't flag as shared on its own |

Shared logins mean nobody can tell who changed what, and the password is usually known to people who've left. API access should use project API keys, not a user login.

### Profile

| Check | Rule | Severity |
|---|---|---|
| Incomplete profile | `first_name` or `last_name` empty or `null`, or a name field contains `@` | Info: often an invitation never completed, or a service account. Combine with other flags |

### Spread of access

| Check | Rule | Severity |
|---|---|---|
| Many projects | the same email has access to N or more of the reviewed projects (default 3) | Review: confirm each project is still needed |
| Vendor in production and sandbox | a vendor user in both | Review: production access is often only needed during go-live |
| Only user with a company domain | a project where every user is vendor or external | Confirm: someone at the company should own the project |

### Activity and leavers

| Check | Rule | Severity |
|---|---|---|
| Leaver | email is on a leavers list the user supplied | Action: remove |
| No recent login | only if the user supplied a last-login export: last login more than 90 days ago (or the user's own threshold) | Review (Action if 180+ days, or in production) |
| No activity data | always, unless an export was supplied | State "can't tell" in the "Couldn't check" section |

## Before recommending removal

- A shared account may be used by an integration. Ask the owner before removing it, and replace it first.
- A vendor may be mid-project. Confirm with the project owner rather than removing outright.
- Removing a user from one project doesn't remove them from the organisation. Say which level the action is at.
