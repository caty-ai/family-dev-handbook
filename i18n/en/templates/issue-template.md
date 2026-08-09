> **Machine translation.** The Japanese original ([issue-template.md](../../../templates/issue-template.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# Issue / Lane Comment Templates

The canonical field schema for each contract (rule ID). The body text (docs/01–03, 05–09) carries only minimal MUST statements; the details live here.
The EPIC Issue and the formats specific to the Epic lane (checkpoint table, Epic log, light-gate record, Epic termination) live in [epic-template.md](epic-template.md) (E series). Child Issues within an Epic use this page's formats as-is.

## Issue body (L1-2)

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

## WIP comment (L0-1 — post to the Issue when starting work. All 4 fields required)

```markdown
🔒 WIP (<agent名> session, YYYY-MM-DD): <何をするか1行>

agent: <agent名>
date: YYYY-MM-DD
Files to touch:
- path/to/file1        <!-- リポルート相対。ファイル名はそのファイルだけ -->
- path/to/dir/         <!-- 末尾スラッシュ = 配下すべて。glob・否定は禁止（L0-2） -->
Branch: fix/<issue>-<slug> (worktree)
```

- A WIP missing any of the 4 fields (agent / date / Files to touch / Branch) is an invalid lock (L0-1)
- When the scope can't be predicted, write `Files to touch: UNKNOWN` = serial-only (L0-2)
- A lane that expects a silence longer than 72h must state the longer staleness window explicitly in the body **with a reason** (L0-3 exception declaration. A later extension must be made visible via a new comment)

## HOLD comment (L1-5 — all 5 fields required)

```markdown
⏸ HOLD (<agent名>, YYYY-MM-DD): <保留する理由1行>

owner: <agent名>
reason: <なぜ止めるか>
review-by: YYYY-MM-DD          <!-- 超過で可視のレビュー義務。ロックは明示処置まで保持・自動解放はされない -->
evidence: <失敗ログ・実行結果へのポインタ>   <!-- リトライ使い切り経由の HOLD では必須（L1-6）。それ以外は任意 -->
lock disposition: retained until review-by | released   <!-- 無言は HOLD 無効 -->
remaining work / successor: <残作業 or 引き継ぎ先>
```

## Terminal state comment (L1-4 — MERGED / SUPERSEDED / ABANDONED)

```markdown
🏁 <MERGED|SUPERSEDED|ABANDONED> (<agent名>, YYYY-MM-DD): <1行>

evidence / successor: <PR リンク・後継 Issue・打ち切りの証拠（L1-6）>
```

## TAKEOVER comment (L0-3 — taking over a stale lane)

```markdown
🔁 TAKEOVER (<agent名>, YYYY-MM-DD)

stale WIP: <引用（宣言者・日付・最終更新からの経過時間）>
resume checklist: <L0-9 チェック結果コメントへのリンク or 本文に併記>
```

Post a new WIP comment (format above) immediately after.

## RELEASE / HANDED-OFF comment (L0-3 — lock lifecycle comment. Not a lane state)

Can only be issued by the **lock owner (the WIP's agent)**. The only path for someone else to remove the lock is stale + TAKEOVER.

```markdown
🔓 RELEASE (<agent名>, YYYY-MM-DD): <ロックを手放す理由1行。レーン状態は L1-4 のコメントで別途宣言>
```

```markdown
🤝 HANDED-OFF (<agent名>, YYYY-MM-DD) → <引き継ぎ先 agent名>

handoff note: <続きの入口・残作業へのポインタ>   <!-- 引き継ぎ先は書き込み前に L0-9 を実施 -->
```

## Resume checklist comment (L0-9 — before the first write on resume, handoff, or TAKEOVER)

```markdown
✅ Resume check (<agent名>, YYYY-MM-DD)

1. lock: mine | lapsed per L0-3（根拠1行）
2. file scope: 宣言集合は origin/main に照らして正確 / アクティブ WIP・PR と非交差
   （gh issue list + gh pr list --state open 再実行済み）
3. branch: fetch/rebase clean（コマンドと結果）
4. Done when: handoff 時から変更なし | 変更あり → <対応>
```

Fixed at 4 items. Do not add more (L0-9).

## Completion record (L1-7 — the merge gate pasted into the PR body)

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

Corrections are made by publishing a new replacement record and reopening review (L1-8). Never edit silently.
