## What this adds or changes

<!-- One or two sentences. -->

**Type:** New skill / Skill update / Subagent / Docs / Other
**Plugin:** loomi-engagement / loomi-discovery / other
**Access:** Read-only / **Writes**: list exactly what it can change

## Testing

<!-- Which clients you tested in, and against what kind of project (sandbox or test). -->

- [ ] Claude (Claude Code / claude.ai / API): ...
- [ ] OpenAI (Codex / ChatGPT / API): ...

## Checklist

- [ ] `python3 scripts/validate_skills.py` passes
- [ ] No credentials, tokens, real project or workspace IDs, or customer data, including in examples and screenshots
- [ ] Tools are referred to by plain name, with no `mcp__` prefixes
- [ ] If more than one project or workspace exists, the skill asks the user which to use
- [ ] Writes (if any) show exactly what will change and wait for confirmation
- [ ] README.md is filled in, and `metadata.version` is bumped
- [ ] I agree that my contribution is licensed under Apache 2.0
