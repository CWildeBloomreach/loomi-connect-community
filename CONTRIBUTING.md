# Contributing

Thanks for helping. This guide explains how to get a contribution merged.

## What we accept

- **Skills**: the main thing this repo collects. See [docs/skill-authoring.md](docs/skill-authoring.md).
- **Subagents**: Claude Code agent definitions for a role, for example "CRM analyst". These are Claude-only today.
- **Scripts**: helpers that a skill uses. They live inside that skill's `scripts/` folder.
- **Docs**: guides, fixes and improvements.

If you're not sure something fits, [open an issue](../../issues/new/choose) before you start.

## How to contribute

**All submissions come in by forking the repository, making your changes in your fork, and opening a pull request.** This applies to everyone, including Bloomreach staff. Contributors don't get write access to this repository, and we can't accept changes sent any other way, such as by email, in an issue, or as a file attachment. Every change is reviewed in its pull request before it's merged.

1. **Fork** the repository on GitHub (the **Fork** button), then clone your fork and create a branch:
   ```bash
   git clone https://github.com/<your-username>/loomi-connect-community.git
   cd loomi-connect-community
   git checkout -b skill/campaign-digest
   ```
2. **Copy the template.** Copy [templates/skill-template/](templates/skill-template/) to `plugins/<plugin>/skills/<skill-name>/`. Choose `loomi-engagement`, `loomi-discovery`, `loomi-platform` (skills that span products) or `loomi-product-data`. If your skill fits none of them, propose a new plugin in an issue first.
3. **Write the skill**, following [docs/skill-authoring.md](docs/skill-authoring.md).
4. **Validate it locally:**
   ```bash
   python3 scripts/validate_skills.py
   claude plugin validate .        # if you have Claude Code installed
   ```
5. **Test it** against a real or sandbox Bloomreach project, in at least one Claude client and one OpenAI client if you can. Say which ones you used in the PR.
6. **Commit and push** to your fork:
   ```bash
   git add plugins/<plugin>/skills/<skill-name>
   git commit -m "Add <skill-name> skill"
   git push origin skill/campaign-digest
   ```
7. **Open a pull request** from your fork's branch to `main` in `bloomreach/loomi-connect-community`, and fill in the template. GitHub offers a **Compare & pull request** button after you push. With the GitHub CLI you can run `gh pr create` instead.
8. **Respond to review.** Push further commits to the same branch; the pull request updates automatically.

With the GitHub CLI, `gh repo fork bloomreach/loomi-connect-community --clone` does step 1's fork and clone in one go.

### Keeping your fork up to date

Before you start new work, sync your fork with the main repository:

```bash
git remote add upstream https://github.com/bloomreach/loomi-connect-community.git   # once
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

Or select **Sync fork** on your fork's GitHub page.

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
