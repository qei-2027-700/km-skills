---
name: gh-wt
description: GitHub Issueを確認し、作業用ブランチとGit worktreeを作成する。ユーザーが「gh-wt」「worktreeを作って」「ブランチとworktreeを切って」と依頼したときに使う。
---

# gh-wt

1. リポジトリの指示、`git remote -v`、`git worktree list`、`git branch --list` を確認する。Issueが指定されていれば `gh issue view <number-or-url>` で対象と目的を読む。未指定でも作業目的が分かればブランチを作成できる。
2. 分岐元はユーザーやリポジトリの指定を優先する。指定がなければ `gh repo view --json nameWithOwner,defaultBranchRef` でデフォルトブランチを確認し、対応するリモートをfetchする。現在の作業ブランチをmergeやresetして最新化しない。
3. 命名規約がなければ、Issueありでは `feature/issue-<number>-<slug>`、Issueなしでは `feature/<slug>` を候補にする。作成先は指定を優先し、未指定ならリポジトリの隣の `<repo-name>-<slug>` にする。既存パスや別作業のブランチを上書きしない。
4. `git worktree add -b <branch> <path> <base-ref>` で作成する。同名ブランチが存在し、それが今回の対象だと確認できた場合は `git worktree add <path> <branch>` を使う。他のworktreeで使用中なら、そのパスを案内する。
5. `git worktree list` と `git -C <path> status -sb` を確認し、作成先・ブランチ・分岐元を報告する。元の作業ツリーにある未コミット変更は移動しない。
