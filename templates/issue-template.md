# Issue / レーンコメント テンプレート

各契約（rule ID）のフィールドスキーマの正本。本文側（docs/01〜03・05〜09）は最小 MUST 文のみを持ち、詳細はここに置く。
EPIC Issue と Epic レーン固有の様式（チェックポイント表・Epic ログ・ライトゲート記録・Epic 終端）は [epic-template.md](epic-template.md)（E 系）。Epic 内の子 Issue は本ページの様式をそのまま使う。

## Issue 本文（L1-2）

```markdown
## 目的 (Why)

<!-- なぜやるのか。背景と、やらないと何が困るか -->

## 完了条件 (Done when)

- [ ] <!-- 機械判定 or 実機判定できる形で -->
- [ ] テスト / lint green
- [ ] （必要なら）実機確認

## 触るファイル / モジュール予測

<!-- 並行GO判定（L2-4）の入力。着手時に WIP コメントで確定版を再宣言する -->
<!-- 予測できない場合は「予測不能（並行不可）」と明記 -->

- path/to/file1
- path/to/module2/

## 想定スコープ

<!-- やること / やらないこと（スコープ外を明示） -->

## 前提条件 (Blocked by)

<!-- 先に終わっているべき Issue / PR。なければ削除 -->
```

## WIP コメント（L0-1 — 着手時に Issue へ。4フィールドすべて必須）

```markdown
🔒 WIP (<agent名> session, YYYY-MM-DD): <何をするか1行>

agent: <agent名>
date: YYYY-MM-DD
Files to touch:
- path/to/file1        <!-- リポルート相対。ファイル名はそのファイルだけ -->
- path/to/dir/         <!-- 末尾スラッシュ = 配下すべて。glob・否定は禁止（L0-2） -->
Branch: fix/<issue>-<slug> (worktree)
```

- 4フィールド（agent / date / Files to touch / Branch）を欠く WIP はロック無効（L0-1）
- 予測できないときは `Files to touch: UNKNOWN` = 直列専用（L0-2）
- 72h より長い沈黙が予定されるレーンは、本文に明示的に長い staleness 窓を**理由つき**で書く（L0-3 の例外宣言。事後延長は新しいコメントで可視に）

## HOLD コメント（L1-5 — 5フィールドすべて必須）

```markdown
⏸ HOLD (<agent名>, YYYY-MM-DD): <保留する理由1行>

owner: <agent名>
reason: <なぜ止めるか>
review-by: YYYY-MM-DD          <!-- 超過で可視のレビュー義務。ロックは明示処置まで保持・自動解放はされない -->
evidence: <失敗ログ・実行結果へのポインタ>   <!-- リトライ使い切り経由の HOLD では必須（L1-6）。それ以外は任意 -->
lock disposition: retained until review-by | released   <!-- 無言は HOLD 無効 -->
remaining work / successor: <残作業 or 引き継ぎ先>
```

## 終端状態コメント（L1-4 — MERGED / SUPERSEDED / ABANDONED）

```markdown
🏁 <MERGED|SUPERSEDED|ABANDONED> (<agent名>, YYYY-MM-DD): <1行>

evidence / successor: <PR リンク・後継 Issue・打ち切りの証拠（L1-6）>
```

## TAKEOVER コメント（L0-3 — stale レーンの引き取り）

```markdown
🔁 TAKEOVER (<agent名>, YYYY-MM-DD)

stale WIP: <引用（宣言者・日付・最終更新からの経過時間）>
resume checklist: <L0-9 チェック結果コメントへのリンク or 本文に併記>
```

直後に新しい WIP コメント（上記様式）を投稿する。

## RELEASE / HANDED-OFF コメント（L0-3 — ロックのライフサイクルコメント。レーン状態ではない）

発行できるのは**ロック所有者（WIP の agent）だけ**。他者がロックを外す経路は stale + TAKEOVER のみ。

```markdown
🔓 RELEASE (<agent名>, YYYY-MM-DD): <ロックを手放す理由1行。レーン状態は L1-4 のコメントで別途宣言>
```

```markdown
🤝 HANDED-OFF (<agent名>, YYYY-MM-DD) → <引き継ぎ先 agent名>

handoff note: <続きの入口・残作業へのポインタ>   <!-- 引き継ぎ先は書き込み前に L0-9 を実施 -->
```

## 再開チェックリスト コメント（L0-9 — 再開・引き継ぎ・TAKEOVER の最初の書き込み前）

```markdown
✅ Resume check (<agent名>, YYYY-MM-DD)

1. lock: mine | lapsed per L0-3（根拠1行）
2. file scope: 宣言集合は origin/main に照らして正確 / アクティブ WIP・PR と非交差
   （gh issue list + gh pr list --state open 再実行済み）
3. branch: fetch/rebase clean（コマンドと結果）
4. Done when: handoff 時から変更なし | 変更あり → <対応>
```

4項目で固定。増やさない（L0-9）。

## 完了記録（L1-7 — PR 本文に貼るマージゲート）

```markdown
## 完了記録 (Completion record)

candidate SHA: <commit SHA>   <!-- レビュー時点の PR head と一致。変われば L1-8 差し替え記録 -->
implementer: <agent/model>
reviewer: <agent/model>
identity check: <差の軸を明記: 別モデル | 別エージェント>   <!-- merge には実装者と別モデル or 別エージェント必須（L1-3）。空欄は blocking -->

### Done when → 結果

| Done when 項目 | 結果 | 証拠（コマンド or 手順 + 観測結果 + 日付） |
|---|---|---|
| <項目1> | PASS / FAIL / N/A(理由) | <実行したもの + 観測した終端結果 + YYYY-MM-DD> |

<!-- 「走った」は PASS ではない。必須項目の FAIL・理由なき N/A は merge ブロック -->
<!-- 証拠はインライン抜粋が正（記録単体で終端結果が読めること）。CI/外部ログ URL は便宜ポインタ・リンクだけは不適合（L1-7） -->

### 宣言 vs 実 diff（L0-6）

git diff --stat origin/main...<候補SHA>: <出力 or 要約>
宣言ファイル集合との差分: なし | <差分と説明>   <!-- diff にあって宣言にないファイルは blocking -->
```

訂正は差し替え記録を新規に公開してレビュー再オープン（L1-8）。黙った編集はしない。
