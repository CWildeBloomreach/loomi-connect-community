#!/usr/bin/env python3
"""Validate every skill in this repo against the Agent Skills spec and our contribution rules.

Uses only the standard library so it runs anywhere. Frontmatter parsing is
deliberately simple: top-level `key: value` pairs plus one level of `metadata:`.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_GLOBS = ["plugins/*/skills/*/SKILL.md", "templates/*/SKILL.md"]
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ACCESS_VALUES = {"read-only", "writes"}
PRODUCT_VALUES = {"engagement", "discovery", "datahub"}
MAX_BODY_LINES = 500


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    raw, body = text[4:end], text[end + 4:]
    fields, current = {}, None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            if current is None:
                raise ValueError(f"indented line outside a mapping: {line!r}")
            k, _, v = line.strip().partition(":")
            fields[current][k.strip()] = v.strip().strip('"\'')
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if v:
            fields[k], current = v.strip('"\''), None
        else:
            fields[k], current = {}, k
    return fields, body


FENCE_RE = re.compile(r"```[^\n]*\n(.*?)```", re.S)
PY_RE = re.compile(r"\bpython3?\s")
COMMAND_RULES = [
    (re.compile(r"\\$|\\ "), "continues over several lines"),
    (re.compile(r"python3?\s+-"), "passes flags to Python before the script"),
    (re.compile(r"[;`]|\$\(|\$\w"), "uses ;, backticks, $(...) or a shell variable"),
    (re.compile(r"(^|\s)\w+=\S*\s*(;|&&)"), "sets a shell variable"),
    (re.compile(r"(^|\s)[<>]{1,2}\s*\S"), "uses a redirect"),
    (re.compile(r"\|\|"), "uses ||"),
]


def documented_commands(body):
    """Script commands a SKILL.md tells the assistant to run: fenced lines and inline code that call python."""
    cmds = []
    for block in FENCE_RE.findall(body):
        cmds += [line.strip() for line in re.sub(r"\\\n\s*", "\\ ", block).splitlines() if PY_RE.search(line.strip())]
    outside = FENCE_RE.sub("", body)
    cmds += [m.strip() for m in re.findall(r"`([^`\n]*\bpython3?\s[^`\n]*)`", outside)]
    # <placeholders> are fine in the docs; they aren't shell redirects.
    return [re.sub(r"<[^<>]+>", "x", c) for c in cmds]


def command_problem(cmd):
    for rule, problem in COMMAND_RULES:
        if rule.search(cmd):
            return problem
    return None


def check_skill(path):
    errors = []
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    try:
        fm, body = parse_frontmatter(text)
    except ValueError as e:
        return [f"{rel}: bad frontmatter: {e}"]
    if fm is None:
        return [f"{rel}: missing YAML frontmatter"]

    name = fm.get("name", "")
    if not name:
        errors.append("missing `name`")
    elif not NAME_RE.fullmatch(name) or len(name) > 64:
        errors.append(f"`name` {name!r} must be 1-64 chars of a-z, 0-9 and single hyphens")
    elif name != path.parent.name:
        errors.append(f"`name` {name!r} must match folder name {path.parent.name!r}")
    if re.search(r"claude|anthropic", name):
        errors.append("`name` must not contain 'claude' or 'anthropic'")

    desc = fm.get("description", "")
    if not desc:
        errors.append("missing `description`")
    elif len(desc) > 1024:
        errors.append(f"`description` is {len(desc)} chars (max 1024)")
    elif re.search(r"[<>]", desc):
        errors.append("`description` must not contain < or >")

    extra = set(fm) - SPEC_FIELDS
    if extra:
        errors.append(f"non-portable frontmatter fields {sorted(extra)}; see docs/skill-authoring.md")

    meta = fm.get("metadata")
    if not isinstance(meta, dict):
        errors.append("missing `metadata` block")
    else:
        for key in ("author", "version", "products", "access"):
            if not meta.get(key):
                errors.append(f"missing `metadata.{key}`")
        if meta.get("access") and meta["access"] not in ACCESS_VALUES:
            errors.append(f"`metadata.access` must be one of {sorted(ACCESS_VALUES)}")
        products = {p.strip() for p in meta.get("products", "").split(",") if p.strip()}
        if products - PRODUCT_VALUES:
            errors.append(f"unknown `metadata.products` {sorted(products - PRODUCT_VALUES)}")

    if body.count("\n") > MAX_BODY_LINES:
        errors.append(f"SKILL.md body is over {MAX_BODY_LINES} lines; move detail into references/")

    for f in path.parent.rglob("*"):
        if f.is_file() and f.suffix in {".md", ".yaml", ".yml", ".py", ".sh", ".json"}:
            if "mcp__" in f.read_text(encoding="utf-8", errors="ignore"):
                errors.append(f"{f.relative_to(path.parent)} hard-codes an `mcp__` tool prefix; use plain tool names")

    for cmd in documented_commands(body):
        problem = command_problem(cmd)
        if problem:
            errors.append(f"script command {cmd[:80]!r} {problem}; see docs/skill-authoring.md#scripts")
    if (path.parent / "scripts").is_dir() and "### Running the scripts" not in body:
        errors.append("has scripts/ but no 'Running the scripts' subsection; see docs/skill-authoring.md#scripts")

    if not (path.parent / "README.md").exists():
        errors.append("missing README.md")

    return [f"{rel}: {e}" for e in errors]


def check_manifests():
    errors = []
    for rel in [".claude-plugin/marketplace.json", ".agents/plugins/marketplace.json"]:
        try:
            data = json.loads((ROOT / rel).read_text())
        except Exception as e:
            errors.append(f"{rel}: {e}")
            continue
        for p in data.get("plugins", []):
            src = p["source"] if isinstance(p["source"], str) else p["source"].get("path", "")
            plugin_dir = ROOT / src
            for manifest in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
                m = plugin_dir / manifest
                if not m.exists():
                    errors.append(f"{rel}: plugin {p['name']!r} is missing {src}/{manifest}")
                    continue
                if json.loads(m.read_text()).get("name") != p["name"]:
                    errors.append(f"{src}/{manifest}: name does not match marketplace entry {p['name']!r}")
    return errors


def main():
    skills = sorted(p for g in SKILL_GLOBS for p in ROOT.glob(g))
    errors = check_manifests()
    for s in skills:
        errors += check_skill(s)
    for e in errors:
        print(f"ERROR {e}")
    print(f"Checked {len(skills)} skill(s): {'FAILED' if errors else 'OK'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
