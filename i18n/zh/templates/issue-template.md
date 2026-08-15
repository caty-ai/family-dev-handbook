> **机器翻译。**日文原文（[issue-template.md](../../../templates/issue-template.md)）是正本 — 本页与原文不一致时，以日文为准。

# Issue / 车道评论 模板

各契约（rule ID）字段规范的正本。正文侧（docs/01〜03・05〜10）只保留最小的 MUST 条文，细节放在这里。
EPIC Issue 与 Epic 车道专属的格式（检查点表・Epic 日志・轻量门禁记录・Epic 终结）见 [epic-template.md](epic-template.md)（E 系列）。Epic 内部的子 Issue 照搬本页的格式。

## Issue 正文（L1-2）

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

## WIP 评论（L0-1 — 着手时发到 Issue。4个字段全部必须）

```markdown
🔒 WIP (<agent名> session, YYYY-MM-DD): <何をするか1行>

agent: <agent名>
date: YYYY-MM-DD
Files to touch:
- path/to/file1        <!-- リポルート相対。ファイル名はそのファイルだけ -->
- path/to/dir/         <!-- 末尾スラッシュ = 配下すべて。glob・否定は禁止（L0-2） -->
Branch: fix/<issue>-<slug> (worktree)
```

- 缺少4个字段（agent / date / Files to touch / Branch）中任一个的 WIP，锁定无效（L0-1）
- 无法预测时写 `Files to touch: UNKNOWN` = 只能串行（L0-2）
- 预计沉默时间会超过 72h 的车道，需在正文中**附理由**明确写出更长的 staleness 窗口（L0-3 的例外声明。事后延长可用新评论使其可见）

## HOLD 评论（L1-5 — 5个字段全部必须）

```markdown
⏸ HOLD (<agent名>, YYYY-MM-DD): <保留する理由1行>

owner: <agent名>
reason: <なぜ止めるか>
review-by: YYYY-MM-DD          <!-- 超過で可視のレビュー義務。ロックは明示処置まで保持・自動解放はされない -->
evidence: <失敗ログ・実行結果へのポインタ>   <!-- リトライ使い切り経由の HOLD では必須（L1-6）。それ以外は任意 -->
lock disposition: retained until review-by | released   <!-- 無言は HOLD 無効 -->
remaining work / successor: <残作業 or 引き継ぎ先>
```

## 终结状态评论（L1-4 — MERGED / SUPERSEDED / ABANDONED）

```markdown
🏁 <MERGED|SUPERSEDED|ABANDONED> (<agent名>, YYYY-MM-DD): <1行>

evidence / successor: <PR リンク・後継 Issue・打ち切りの証拠（L1-6）>
release: <tag URL（+ 署名必須リポは「署名: あり | 対象外」） | deferred #n（完了記録どおり） | N/A>
<!-- MERGED の必須フィールド（T-5 / L1-4）。vX.Y.Z を宣言したレーンは、タグを切って URL を載せるまで MERGED を宣言できない（URL 無き MERGED は不正形式 = 終端未成立）。宣言と異なる版を切った場合は差異と理由を1行 -->
```

## TAKEOVER 评论（L0-3 — 接手 stale 车道）

```markdown
🔁 TAKEOVER (<agent名>, YYYY-MM-DD)

stale WIP: <引用（宣言者・日付・最終更新からの経過時間）>
resume checklist: <L0-9 チェック結果コメントへのリンク or 本文に併記>
```

紧接着发布新的 WIP 评论（上述格式）。

## RELEASE / HANDED-OFF 评论（L0-3 — 锁定的生命周期评论。不是车道状态）

只有**锁定所有者（WIP 中的 agent）**才能发布。他人解锁的途径只有 stale + TAKEOVER。

```markdown
🔓 RELEASE (<agent名>, YYYY-MM-DD): <ロックを手放す理由1行。レーン状態は L1-4 のコメントで別途宣言>
```

```markdown
🤝 HANDED-OFF (<agent名>, YYYY-MM-DD) → <引き継ぎ先 agent名>

handoff note: <続きの入口・残作業へのポインタ>   <!-- 引き継ぎ先は書き込み前に L0-9 を実施 -->
```

## 复位检查清单 评论（L0-9 — 恢复・交接・TAKEOVER 的首次写入之前）

```markdown
✅ Resume check (<agent名>, YYYY-MM-DD)

1. lock: mine | lapsed per L0-3（根拠1行）
2. file scope: 宣言集合は origin/main に照らして正確 / アクティブ WIP・PR と非交差
   （gh issue list + gh pr list --state open 再実行済み）
3. branch: fetch/rebase clean（コマンドと結果）
4. Done when: handoff 時から変更なし | 変更あり → <対応>
```

固定为4项。不要增加（L0-9）。

## 完成记录（L1-7 — 贴在 PR 正文中的合并门禁）

```markdown
## 完了記録 (Completion record)

candidate SHA: <commit SHA>   <!-- レビュー時点の PR head と一致。変われば L1-8 差し替え記録 -->
implementer: <agent/model>
reviewer: <agent/model>
identity check: <差の軸を明記: 別モデル | 別エージェント>   <!-- merge には実装者と別モデル or 別エージェント必須（L1-3）。空欄は blocking -->
CI: <green | red | N/A（理由）>   <!-- 赤のまま merge 禁止（T-4）。空欄・未編集のプレースホルダは blocking。CI 不在は green ではない。N/A は CI が当該変更を検査しない場合に限る（CI が走る変更は非コードでも N/A 不可） -->
release: <vX.Y.Z | deferred（理由 + トリガー付き Issue #n） | N/A（①規範を含まない docs のみ / ②挙動・公開API・配布物を変えない内部整理 / ③CI・開発環境の配線のみ / ④main 未到達の中間 merge=Epic 子→epic / 類型外はオーナー専決1行）>
<!-- 全完了記録で欄必須（T-5）。空欄・未編集のプレースホルダ・3語彙以外の値は未記入扱い = blocking。出荷相当（挙動・公開API・配布物・利用者が従う規範が変わる）の merge は N/A 不可・迷ったら出荷相当。
     vX.Y.Z は宣言 — merge 後に当該 merge が main に残したコミットへ annotated タグを切り、tag URL を MERGED コメントに載せるまで MERGED を宣言できない（原則は宣言と同名・版が動いたら MERGED に差異と理由を1行）。
     deferred は退場トリガー付き Issue 参照が必須（無ければ先に立てる）。トリガー失効後は「切らない特権」を失い、次の出荷相当 merge は vX.Y.Z 必須（失効自体は記録を止めない） -->
previous release: <直前の出荷相当 merge の release 値 + 履行状態（vX.Y.Z→tag URL | deferred #n（トリガー生存 or 失効） | none（初回））>
<!-- 全完了記録に置く（T-5）。履行確認（L1-7⑦）と deferred 連続計数の台帳を兼ねる。未履行の vX.Y.Z は blocking。直前が deferred でその previous も deferred なら今回は vX.Y.Z 必須 -->
<!-- red の場合は、以下の4点をコメントの外に転記して埋める（コメントのままは未記入扱い = blocking。1点でも欠ければ例外不成立 — T-4）:
     failing check: <check 名> / run: <run 識別子> @ <候補SHA> / 観測日付: <YYYY-MM-DD>
     無関係の根拠: <base で同一の赤を再現した記録（インライン抜粋）>
     既知 Issue: #<n>（LC-1 退場トリガー付き）
     owner 承認: <オーナー本人の PR コメント等、実在を第三者が確認できる形。本文記述のみは不成立（FP-8）> -->

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

订正需新发布一份差替记录并重新打开复审（L1-8）。不做无声的编辑。
