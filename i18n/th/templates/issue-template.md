> **แปลโดยเครื่อง** ต้นฉบับภาษาญี่ปุ่น ([issue-template.md](../../../templates/issue-template.md)) เป็นฉบับหลัก — หากหน้านี้ขัดกับต้นฉบับ ให้ยึดข้อความภาษาญี่ปุ่นเป็นหลัก

# Issue / เทมเพลตความคิดเห็นในเลน

ต้นฉบับของ field schema สำหรับแต่ละสัญญา (rule ID) ส่วนเนื้อหาหลัก (docs/01〜03・05〜10) มีเฉพาะประโยค MUST ขั้นต่ำเท่านั้น รายละเอียดทั้งหมดอยู่ที่นี่
รูปแบบเฉพาะของ EPIC Issue และเลน Epic (ตารางเช็คพอยต์・บันทึก Epic・บันทึก light gate・การสิ้นสุด Epic) อยู่ที่ [epic-template.md](epic-template.md)（ระบบ E）Issue ลูกภายใน Epic ใช้รูปแบบของหน้านี้ตามเดิม

## เนื้อหา Issue（L1-2）

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

## ความคิดเห็น WIP（L0-1 — ลงใน Issue ตอนเริ่มงาน จำเป็นต้องมีครบทั้ง 4 field）

```markdown
🔒 WIP (<agent名> session, YYYY-MM-DD): <何をするか1行>

agent: <agent名>
date: YYYY-MM-DD
Files to touch:
- path/to/file1        <!-- リポルート相対。ファイル名はそのファイルだけ -->
- path/to/dir/         <!-- 末尾スラッシュ = 配下すべて。glob・否定は禁止（L0-2） -->
Branch: fix/<issue>-<slug> (worktree)
```

- WIP ที่ขาด field ใดๆ ใน 4 field（agent / date / Files to touch / Branch）ถือว่า lock ไม่มีผล（L0-1）
- เมื่อพยากรณ์ไม่ได้ ให้ระบุ `Files to touch: UNKNOWN` = ใช้ได้เฉพาะแบบ serial เท่านั้น（L0-2）
- เลนที่คาดว่าจะเงียบนานเกิน 72h ต้องเขียน window staleness ที่ยาวขึ้นไว้ในเนื้อหาอย่างชัดเจน**พร้อมเหตุผล**（ข้อยกเว้นตาม L0-3 การขยายเวลาในภายหลังทำได้ด้วยความคิดเห็นใหม่เพื่อให้มองเห็นได้）

## ความคิดเห็น HOLD（L1-5 — จำเป็นต้องมีครบทั้ง 5 field）

```markdown
⏸ HOLD (<agent名>, YYYY-MM-DD): <保留する理由1行>

owner: <agent名>
reason: <なぜ止めるか>
review-by: YYYY-MM-DD          <!-- 超過で可視のレビュー義務。ロックは明示処置まで保持・自動解放はされない -->
evidence: <失敗ログ・実行結果へのポインタ>   <!-- リトライ使い切り経由の HOLD では必須（L1-6）。それ以外は任意 -->
lock disposition: retained until review-by | released   <!-- 無言は HOLD 無効 -->
remaining work / successor: <残作業 or 引き継ぎ先>
```

## ความคิดเห็นสถานะสิ้นสุด（L1-4 — MERGED / SUPERSEDED / ABANDONED）

```markdown
🏁 <MERGED|SUPERSEDED|ABANDONED> (<agent名>, YYYY-MM-DD): <1行>

evidence / successor: <PR リンク・後継 Issue・打ち切りの証拠（L1-6）>
release: <tag URL（+ 署名必須リポは「署名: あり | 対象外」） | deferred #n（完了記録どおり） | N/A>
<!-- MERGED の必須フィールド（T-5 / L1-4）。vX.Y.Z を宣言したレーンは、タグを切って URL を載せるまで MERGED を宣言できない（URL 無き MERGED は不正形式 = 終端未成立）。宣言と異なる版を切った場合は差異と理由を1行 -->
```

## ความคิดเห็น TAKEOVER（L0-3 — การรับช่วงต่อเลนที่ stale）

```markdown
🔁 TAKEOVER (<agent名>, YYYY-MM-DD)

stale WIP: <引用（宣言者・日付・最終更新からの経過時間）>
resume checklist: <L0-9 チェック結果コメントへのリンク or 本文に併記>
```

ให้โพสต์ความคิดเห็น WIP ใหม่（รูปแบบด้านบน）ทันทีหลังจากนั้น

## ความคิดเห็น RELEASE / HANDED-OFF（L0-3 — ความคิดเห็นเกี่ยวกับ lifecycle ของ lock ไม่ใช่สถานะของเลน）

ผู้ที่ออกความคิดเห็นได้มีเพียง**เจ้าของ lock（agent ที่ทำ WIP）เท่านั้น** เส้นทางเดียวที่ผู้อื่นจะปลด lock ได้คือ stale + TAKEOVER

```markdown
🔓 RELEASE (<agent名>, YYYY-MM-DD): <ロックを手放す理由1行。レーン状態は L1-4 のコメントで別途宣言>
```

```markdown
🤝 HANDED-OFF (<agent名>, YYYY-MM-DD) → <引き継ぎ先 agent名>

handoff note: <続きの入口・残作業へのポインタ>   <!-- 引き継ぎ先は書き込み前に L0-9 を実施 -->
```

## ความคิดเห็นเช็คลิสต์การเริ่มงานต่อ（L0-9 — ก่อนการเขียนครั้งแรกของการเริ่มงานต่อ・การส่งต่องาน・TAKEOVER）

```markdown
✅ Resume check (<agent名>, YYYY-MM-DD)

1. lock: mine | lapsed per L0-3（根拠1行）
2. file scope: 宣言集合は origin/main に照らして正確 / アクティブ WIP・PR と非交差
   （gh issue list + gh pr list --state open 再実行済み）
3. branch: fetch/rebase clean（コマンドと結果）
4. Done when: handoff 時から変更なし | 変更あり → <対応>
```

กำหนดตายตัวไว้ที่ 4 หัวข้อ ห้ามเพิ่ม（L0-9）

## บันทึกการเสร็จสิ้น（L1-7 — เกตสำหรับ merge ที่แปะไว้ในเนื้อหา PR）

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

การแก้ไขให้เผยแพร่บันทึกฉบับแทนที่ใหม่แล้วเปิดรีวิวใหม่อีกครั้ง（L1-8）ห้ามแก้ไขแบบเงียบๆ
