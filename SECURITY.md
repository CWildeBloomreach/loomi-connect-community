# Security

## Reporting a problem

**Do not open a public issue** for security problems. Examples:

- a skill that leaks data
- a skill that writes without asking first
- credentials committed by mistake

Report it privately through [GitHub private vulnerability reporting](../../security/advisories/new). <!-- TODO: or add a Bloomreach security contact -->

If you think a problem is in Loomi Connect itself rather than in this repository, report it through your normal Bloomreach support channel.

## If you committed a secret

Revoke or rotate it straight away. Removing it from the repository is not enough, because it stays in git history and forks. Then tell the maintainers.
