---
name: gh-rv
description: GitHub Pull Request をレビューする。ユーザーが「gh-rv」「PRをレビューして」「このPRを見て」などと言ったときに使う。
---

# gh-rv スキル

`gh pr diff` と `gh pr view` を使って Pull Request をレビューし、問題点や改善点を指摘する。

## 手順

### 1. PR の概要を確認する

```bash
gh pr view <PR番号またはURL>
```

### 2. 差分を取得する

```bash
gh pr diff <PR番号またはURL>
```

### 3. CI ステータスを確認する

```bash
gh pr checks <PR番号またはURL>
```

### 4. レビューコメントを投稿する（任意）

```bash
gh pr review <PR番号> --comment --body "<コメント>"
gh pr review <PR番号> --approve
gh pr review <PR番号> --request-changes --body "<変更要求>"
```

## 指摘ラベル

各指摘には必ず以下のいずれかのラベルを先頭に付ける:

| ラベル | 意味 |
|---|---|
| `[must]` | マージ前に必ず修正が必要。バグ・セキュリティ問題など |
| `[should]` | 修正を強く推奨。放置すると将来問題になりうる |
| `[nit]` | 軽微な改善提案。対応は任意 |
| `[ask]` | 意図確認。問題ではなく質問 |

例:
> `[must]` エラーが握りつぶされています。`log.Printf` などで記録してください。
> `[nit]` 変数名 `d` より `data` の方が意図が伝わりやすいです。

## レビュー観点

以下の順で確認する:

1. **正確性** — バグ、ロジックエラー、境界値
2. **セキュリティ** — secrets のハードコード、インジェクション、Supply Chain（Actions の hash ピン留めなど）
3. **可読性** — 命名、不要なコメント、複雑すぎる処理
4. **テスト** — 変更に対してテストが存在するか

## 注意

- Dependabot PR はバージョンアップのみなので CI が green なら基本 approve
- `workflow` スコープがない場合は Actions ファイルの変更を含む PR はマージできないため、GitHub UI 上で手動マージを案内する
