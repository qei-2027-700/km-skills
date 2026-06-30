# km-skills

個人用 Claude Code スキルリポジトリ。  
`~/.claude/skills/` へのシンリンクで、どのプロジェクトからでも利用できる。

## スキル一覧

| スキル | 説明 |
|---|---|
| [mermaid](skills/mermaid/SKILL.md) | Mermaid 記法で図を生成・表示する |
| [gh-rv](skills/gh-rv/SKILL.md) | GitHub Pull Request をレビューする |

## セットアップ

```bash
git clone https://github.com/qei-2027-700/km-skills ~/dev/_github/km-skills
bash ~/dev/_github/km-skills/install.sh
```

## 更新

```bash
bash ~/dev/_github/km-skills/update.sh
```

## スキルの追加

```
skills/
  <skill-name>/
    SKILL.md    ← frontmatter に name と description を記載
```

```bash
bash install.sh   # ~/.claude/skills/ にシンリンクを張る
```

### SKILL.md テンプレート

```markdown
---
name: <skill-name>
description: <トリガー条件をここに書く。ユーザーが「...」と言ったときに使う。>
---

# <skill-name> スキル

...
```
