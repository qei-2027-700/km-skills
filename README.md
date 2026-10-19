# km-skills

個人用の Claude Code・Codex 共通スキルリポジトリ。
`skills/` を共通のソースとし、各ツールの読み込み先へのシンボリックリンクで、どのプロジェクトからでも利用できる。

| ツール | インストール先 |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.agents/skills/` |

配置先とシンボリックリンクの対応は、[Claude Code の公式ドキュメント](https://code.claude.com/docs/en/skills)と[Codex の公式ドキュメント](https://learn.chatgpt.com/docs/build-skills)に準拠する。

## スキル一覧

| スキル | 説明 |
|---|---|
| [mermaid](skills/mermaid/SKILL.md) | Mermaid 記法で図を生成・表示する |
| [gh-rv](skills/gh-rv/SKILL.md) | GitHub Pull Request をレビューする |
| [gh-pr](skills/gh-pr/SKILL.md) | 変更と検証結果を整理し、pushしてPRを作成する |
| [gh-merge](skills/gh-merge/SKILL.md) | CI・レビュー条件を確認してPRをマージする |
| [git-commit](skills/git-commit/SKILL.md) | 依頼範囲の変更をステージしてコミットする |
| [git-push](skills/git-push/SKILL.md) | 送信先とコミットを確認してpushする |
| [git-rebase](skills/git-rebase/SKILL.md) | 未公開コミットを整理する |

Git・PR操作の追加スキルは `go-drive-etl` の運用を参考に、リポジトリ固有の文書・パス・モデル設定に依存しない形にした。`gh-pr` は本文冒頭のIMPORTANTアラートで課題と変更後の状態を伝え、実施した検証と未確認事項を記載する。

## セットアップ

```bash
git clone https://github.com/qei-2027-700/km-skills ~/dev/_github/km-skills
bash ~/dev/_github/km-skills/install.sh
```

引数を省略すると両方に導入する。片方だけ使う場合は対象を指定する。

```bash
bash install.sh claude
bash install.sh codex
```

既存のシンボリックリンクはこのリポジトリへのリンクに更新する。同名の実ファイル・実ディレクトリは上書きせず、`skip` と表示する。
導入後は新しいセッションで認識を確認する。Claude Code では `/mermaid` や `/gh-rv`、Codex では `$mermaid` や `$gh-rv` で呼び出せる。

## 更新

```bash
bash ~/dev/_github/km-skills/update.sh
```

`git pull --ff-only` の後、両方のリンクを更新する。`bash update.sh codex` のように対象を指定することもできる。

## スキルの追加

```
skills/
  <skill-name>/
    SKILL.md    ← frontmatter に name と description を記載
```

```bash
bash install.sh   # Claude Code・Codex 両方の読み込み先にリンクを作る
```

`SKILL.md` があるディレクトリだけが導入対象になる。共通スキルではツール固有のパスや機能への依存を避ける。Git操作には Git、`gh-*` には認証済みの GitHub CLI（`gh`）、Mermaid の任意のブラウザプレビューには Python 3 と macOS の `open` コマンドが必要。

インストール処理は `python3 tests/test_install.py` で検証できる。一時ディレクトリで実行するため、通常のホームディレクトリにはリンクを作成しない。

### SKILL.md テンプレート

```markdown
---
name: <skill-name>
description: <トリガー条件をここに書く。ユーザーが「...」と言ったときに使う。>
---

# <skill-name> スキル

...
```
