#!/usr/bin/env bash
# Symlink every skill in this repo into the personal skill folders for
# Claude Code (~/.claude/skills) and OpenAI Codex (~/.agents/skills).
# Re-run after pulling to pick up new skills. Existing non-symlink folders are left alone.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
targets=("$HOME/.claude/skills" "$HOME/.agents/skills")

for target in "${targets[@]}"; do
  mkdir -p "$target"
  for skill in "$repo"/plugins/*/skills/*/; do
    name="$(basename "$skill")"
    dest="$target/$name"
    if [ -e "$dest" ] && [ ! -L "$dest" ]; then
      echo "skip  $dest (exists and is not a symlink)"
      continue
    fi
    ln -sfn "${skill%/}" "$dest"
    echo "link  $dest"
  done
done
