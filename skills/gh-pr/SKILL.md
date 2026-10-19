---
name: gh-pr
description: 現在の作業ブランチをpushし、GitHub Pull Requestを作成する。ユーザーが「gh-pr」「PRを作って」「プルリクエスト作成して」と依頼したときに使う。
---

# gh-pr

認証済みの GitHub CLI（`gh`）と Git を使う。対象リポジトリの指示、PRテンプレート、検証コマンドを確認してから進める。他のスキルや特定リポジトリの文書は必須にしない。

## 作成手順

1. `git status --short`、`git branch --show-current`、`git remote -v`、`gh repo view --json nameWithOwner,defaultBranchRef` で対象を確認する。forkではbase側とhead側のリポジトリを区別する。baseはユーザーやリポジトリの指定を優先し、指定がなければデフォルトブランチを使う。detached HEADやbaseと同じブランチの場合は作業ブランチを用意する。未コミット変更はPRに含まれないため確認し、依頼範囲の変更を含める必要があればコミットまで行う。他の作業をまとめて含めない。
2. baseのリモートをfetchし、`git log --oneline <base-ref>..HEAD` と `git diff <base-ref>...HEAD` を読む。関連Issueは指定されたもの、または変更との関連を確認できたものだけ読む。差分がなければ作成を止め、その理由を報告する。対象のhead・baseに既存PRがないか確認し、存在する場合は重複作成せずURLを使う。
3. 変更に必要なテスト・ビルド・静的解析を実行する。成功済みの検証は、変更や新たな懸念がなければ繰り返さない。失敗・未実施は本文に明記し、未検証を成功扱いしない。作業途中や必要な検証が未完了の場合はdraftにする。
4. 以下の形式でタイトルと本文を作り、現在のブランチを明示した通常のpushで送信する。追跡先がなければ `git push -u <remote> <branch>` を使う。PR作成の依頼には対象ブランチのpushを含むが、force pushやマージは含めない。
5. 本文を一時ファイルに保存し、`gh pr create --repo <owner/repo> --base <base> --head <head> --title '<title>' --body-file <body-file>` で作成する。forkのheadは必要に応じて `<owner>:<branch>` を指定し、draftの場合は `--draft` を付ける。本文をシェルのコマンド置換で渡さない。失敗後の再試行前には作成済みか確認する。

## タイトルと本文

タイトルはリポジトリの規約を優先する。規約がなければ `feat: ...`、`fix: ...`、`docs: ...` などのConventional Commits形式にする。

本文は必ず次のIMPORTANTアラートから始める。Issueと差分で確認した課題と変更後の状態を1〜3文で書く。変更ファイルの列挙だけで済ませず、未確認の効果を補わない。テンプレートの後続セクションは残し、生成元の表記がある場合は末尾に置く。

```markdown
> [!IMPORTANT]
> 解決する課題と、変更後にどうなるかを記載する。

## 変更内容
- 実際の変更を記載する。

## 関連Issue
関係するIssueがある場合に記載する。

## 検証
- 実行したコマンドと結果、未実施の確認を記載する。
```

`Closes #123` はそのIssueの完了条件を満たす場合にだけ使い、部分対応なら `Refs #123` にする。関連Issueがなければ項目を省略する。

## 完了確認

作成したPRを `gh pr view <url> --json url,title,body,baseRefName,headRefName,isDraft` で取得し、本文・対象ブランチ・draft状態を確認する。PRのURLと検証結果、残っている確認事項を報告する。
