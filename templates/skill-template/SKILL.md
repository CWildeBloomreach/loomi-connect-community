---
name: skill-template
description: One sentence on what this skill does in Bloomreach (Engagement or Discovery) using Loomi Connect. Use when the user asks for X, Y or Z, in the words they would actually type.
license: Apache-2.0
compatibility: Requires the Loomi Connect MCP server (Bloomreach Engagement).
metadata:
  author: your-github-handle
  version: "0.1.0"
  products: engagement
  access: read-only
---

# Skill title

## What this does

One short paragraph: the job this skill does and what the user gets back.

## Before you start

- This skill uses these Loomi Connect tools: `list_cloud_organizations`, `list_projects`, ...
- If a tool you need isn't available, find it with the Loomi Connect `search_tools` tool and run it with `call_tool`.
- Ask the user for anything you can't work out yourself, such as the date range. Don't guess.

## Steps

1. **Resolve the project.** Call `list_cloud_organizations`, then `list_projects`. If there's more than one organisation or project, list them and ask the user which to use.
2. ...
3. ...

Make Loomi Connect calls one at a time. If a call returns a rate-limit error (HTTP 429), wait and retry.

## Output

Describe the exact format to return, for example:

- A one-line headline.
- A table with columns A, B, C.
- Up to three recommended next steps.

## Safety

This skill is **read-only**. It never creates, changes or deletes anything.

<!--
For a skill that writes, replace the section above with something like this:
This skill **writes** to Bloomreach. It can: <list exactly what>.
Before every write, show the user exactly what will change and wait for an explicit "yes".
Discovery changes are live immediately, and deletes cannot be undone.
-->
