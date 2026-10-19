---
name: git-push
description: 現在の作業ブランチのコミットをリモートへpushする。ユーザーが「git-push」「pushして」「リモートに上げて」と依頼したときに使う。
---

# git-push

1. `git status -sb`、`git branch --show-current`、`git remote -v`、`git branch -vv` でブランチと送信先を確認する。upstreamがあれば利用し、なければユーザーやリポジトリの指定、通常は `origin` を使う。候補が複数あり判断できない場合は送信先を確認する。detached HEADではpushを止める。
2. 対象リモートをfetchし、送信予定のコミットと差分を読む。リモートブランチがある場合は `git log --oneline <remote>/<branch>..HEAD` などで確認する。新規ブランチでは分岐元との比較で対象を確認する。未コミット変更はpush対象に含まれないため、残っていれば報告する。
3. 追跡先がある場合もリモートと送信元・先を明示して `git push <remote> HEAD:refs/heads/<remote-branch>` を実行する。追跡先がなければ `git push -u <remote> <branch>` を使う。通常のpush依頼ではforce push、タグの一括送信、無関係のブランチの送信を行わない。
4. push先のrefを `git ls-remote <remote> refs/heads/<remote-branch>` で取得し、送信したコミットと一致することを確認して、リモート・ブランチ・コミットIDを報告する。

non-fast-forwardで拒否されたら分岐状況を示す。自動でforce pushせず、統合方法を判断する。`main` / `master` や保護ブランチへのforce pushは行わない。
