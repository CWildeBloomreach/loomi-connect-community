# Contributing

Thanks for helping. This guide explains how to get a contribution merged.

## What we accept

- **Skills**: the main thing this repo collects. See [docs/skill-authoring.md](docs/skill-authoring.md).
- **Subagents**: Claude Code agent definitions for a role, for example "CRM analyst". These are Claude-only today.
- **Scripts**: helpers that a skill uses. They live inside that skill's `scripts/` folder.
- **Docs**: guides, fixes and improvements.

If you're not sure something fits, [open an issue](../../issues/new/choose) before you start.

## How to contribute

1. **Fork** the repository and create a branch, for example `skill/campaign-digest`.
2. **Copy the template.** Copy [templates/skill-template/](templates/skill-template/) to `plugins/<plugin>/skills/<skill-name>/`. Choose `loomi-engagement` or `loomi-discovery`. If your skill fits neither, propose a new plugin in an issue first.
3. **Write the skill**, following [docs/skill-authoring.md](docs/skill-authoring.md).
4. **Validate it locally:**
   ```bash
   python3 scripts/validate_skills.py
   claude plugin validate .        # if you have Claude Code installed
   ```
5. **Test it** against a real or sandbox Bloomreach project, in at least one Claude client and one OpenAI client if you can. Say which ones you used in the PR.
6. **Open a pull request** and fill in the template.

## Review

- Every PR needs **one maintainer approval**.
- A skill that **writes** data needs **two approvals**. That covers creating campaigns or scenarios, changing Discovery rules, starting experiments, and similar actions.
- Reviewers check correctness, safety, clarity, and that the skill works across clients.
- CI runs `scripts/validate_skills.py` on every PR. It must pass.

Once a PR is merged, the contributor is credited in the skill's `metadata.author` and README.

## Hard rules

A PR that breaks any of these will not be merged:

- No credentials, tokens, API keys, real project or workspace IDs, customer data, or screenshots that show any of these. Use placeholders.
- Skills must not hard-code client-specific tool prefixes such as `mcp__loomi-connect-usa__...`. Refer to Loomi Connect tools by their plain names. See the authoring guide.
- Write operations must be labelled, and they must ask for confirmation before they run.

## Versioning

Bump `metadata.version` in the skill's frontmatter when you change a skill. Maintainers bump the plugin version in both manifests (`.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`) when they release.

## License

By contributing, you agree that your contribution is licensed under the [Apache 2.0 License](LICENSE).

## Code of conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md).
