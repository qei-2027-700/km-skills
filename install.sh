#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$REPO_DIR/skills"
CLAUDE_SKILLS="$HOME/.claude/skills"

mkdir -p "$CLAUDE_SKILLS"

linked=0
for skill_path in "$SKILLS_DIR"/*/; do
  [ -d "$skill_path" ] || continue
  skill_name="$(basename "$skill_path")"
  target="$CLAUDE_SKILLS/$skill_name"

  if [ -L "$target" ]; then
    # 既存シンリンクを更新
    ln -sf "$skill_path" "$target"
    echo "updated: $skill_name"
  elif [ -e "$target" ]; then
    echo "skip (already exists, not a symlink): $skill_name"
    continue
  else
    ln -s "$skill_path" "$target"
    echo "linked:  $skill_name"
  fi
  ((linked++)) || true
done

echo ""
echo "$linked skill(s) installed → $CLAUDE_SKILLS"
