> **Machine translation.** The Japanese original ([brief-template.md](../../../templates/brief-template.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# Delegation Brief Template

The canonical format for the B layer ([docs/07](../docs/07-delegation-brief.md)). For each delegation, copy the following into the request text and fill it in. Heading strings are subject to machine inspection, so do not change them from the wording each family has decided on ([B-5](../docs/07-delegation-brief.md)).

## Brief Body (B-1)

```markdown
## 実装仕様

<!-- Goal: 何を作る / 直すかを1〜3行で。担当 Issue: #番号 or URL（B-3: Issue が正本） -->
<!-- 触ってよい範囲: ファイル / ディレクトリの列挙（Issue のファイル予測と一致させる）。範囲外は触らない -->
<!-- 前積みの文脈: 必要な事実・パス・仕様・制約・環境の癖。委譲先に探索させない（B-4） -->
<!-- 納品形式: 出力先ファイルのパス・報告の分量・報告に含めるもの -->

## 実装チェック

<!-- 納品前に作業者自身が回す検証。機械判定できる形で書く -->
- [ ] テスト / lint green（実行コマンドと期待結果を明記）
- [ ] 触ってよい範囲の外に diff がない
- [ ] （タスク固有の検証項目）

## レビュー基準

<!-- 後段のレビューが見る観点。作業者にも最初から見せる -->
- 正しさ: <このタスクで「正しい」とは何か>
- 境界: 宣言ファイル集合の内側に収まっているか
- 最悪の失敗形: <この変更で一番まずいのは◯◯が起きること（B-4: 名指しする）>
```

## Key Points for Writing

- **Write assuming the delegate cannot read this conversation's history** (fresh context). "With the approach from earlier" or "that thing" doesn't exist as far as they're concerned.
- **Keep independent review seats blind** (B-4): give every seat the identical brief, and don't mix in other seats' feedback, your own prior analysis, or the conclusion you expect.
- **Don't inline a long body into the request text**: it's fine to put the body in a file and give the request text only "read `<path>` and follow it." In some execution environments, argument-length limits can cause the request itself to die silently.
- **Retries are finite** ([L1-6](../docs/02-issue-loop.md)): don't keep re-issuing the same brief. Add the observed failure to the pre-loaded context and re-issue; if that's exhausted too, stop and provide evidence.
