---
name: gh-merge
description: GitHub PRのCIとレビュー条件を確認してマージする。ユーザーが「gh-merge」「PRをマージして」と依頼したときに使う。ブランチやworktreeの削除は依頼された場合に行う。
---

# gh-merge

1. 対象PRを `gh pr view <number-or-url> --json url,state,isDraft,baseRefName,headRefName,headRefOid,mergeable,reviewDecision` で確認し、リポジトリのマージ規約を読む。対象が曖昧なら確定する。すでにマージ済みなら再実行せず結果を報告する。
2. `gh pr checks <number-or-url>` とレビューを確認する。必須チェックが失敗・実行中、draft、競合、未解消の変更要求がある場合はマージせず状況を報告する。CIが設定されていない場合はその事実とローカル検証を区別する。関連Issueの完了条件や必要なレビューも確認する。
3. リポジトリ指定の方式でマージする。指定がなければsquashを使う。確認したコミットを固定して `gh pr merge <number-or-url> --squash --match-head-commit <head-sha>` を実行する。別方式を使う場合は `--squash` を `--merge` または `--rebase` に替える。管理者による条件の迂回は行わない。
4. `gh pr view <number-or-url> --json state,mergedAt,url` でマージ済みか確認する。マージキューに入った場合は「待機中」と報告し、マージ完了扱いにしない。
5. 後片付けまで依頼されている場合は、マージ完了後に対象worktreeの未コミット・未追跡ファイルとブランチの未送信コミットを確認する。未保存の作業があれば保持する。削除対象の外へ移動してから `git worktree remove <path>` と `git branch -d <branch>` を使う。squash後に `-d` が拒否した場合は、その事実を報告して保持し、`--force` や `-D` で押し切らない。リモートブランチの削除も後片付けの対象を確認して行う。

PRのURL、マージ状態、実施した後片付けと残したものを報告する。
