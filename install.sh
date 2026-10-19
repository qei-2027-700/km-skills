#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$REPO_DIR/skills"
case "${1:-all}" in
  all) targets=("$HOME/.claude/skills" "$HOME/.agents/skills") ;;
  claude) targets=("$HOME/.claude/skills") ;;
  codex) targets=("$HOME/.agents/skills") ;;
  -h|--help)
    echo "Usage: bash install.sh [all|claude|codex]"
    exit 0
    ;;
  *)
    echo "Usage: bash install.sh [all|claude|codex]" >&2
    exit 1
    ;;
esac
if [ "$#" -gt 1 ]; then
  echo "Usage: bash install.sh [all|claude|codex]" >&2
  exit 1
fi

for skills_target in "${targets[@]}"; do
  mkdir -p "$skills_target"

  linked=0
  for skill_path in "$SKILLS_DIR"/*/; do
    [ -d "$skill_path" ] || continue
    [ -f "$skill_path/SKILL.md" ] || continue
    skill_name="$(basename "$skill_path")"
    target="$skills_target/$skill_name"

    if [ -L "$target" ]; then
      # 既存シンリンクを更新（-n: シンリンク先をディレクトリとして辿らない）
      ln -sfn "$skill_path" "$target"
      echo "updated: $skill_name"
    elif [ -e "$target" ]; then
      echo "skip (already exists, not a symlink): $skill_name"
      continue
    else
      ln -sn "$skill_path" "$target"
      echo "linked:  $skill_name"
    fi
    ((linked++)) || true
  done

  echo ""
  echo "$linked skill(s) installed → $skills_target"
done
