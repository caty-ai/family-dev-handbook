> **แปลโดยเครื่อง** ต้นฉบับภาษาญี่ปุ่น ([issue-template.md](../../../templates/issue-template.md)) เป็นฉบับหลัก — หากหน้านี้ขัดกับต้นฉบับ ให้ยึดข้อความภาษาญี่ปุ่นเป็นหลัก

# เทมเพลต Issue / คอมเมนต์เลน

ต้นฉบับหลักของ field schema สำหรับแต่ละสัญญา (rule ID) เนื้อหาหลัก (docs/01〜03・05〜07) มีเฉพาะประโยค MUST ขั้นต่ำเท่านั้น รายละเอียดทั้งหมดอยู่ที่นี่
รูปแบบเฉพาะของ EPIC Issue และเลน Epic (ตารางจุดตรวจสอบ・บันทึก Epic・บันทึก light gate・การสิ้นสุด Epic) อยู่ที่ [epic-template.md](epic-template.md) (กลุ่ม E) Issue ย่อยภายใน Epic ใช้รูปแบบของหน้านี้ตรงๆ

## เนื้อหา Issue (L1-2)

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

## คอมเมนต์ WIP (L0-1 — โพสต์ลง Issue ตอนเริ่มงาน ต้องมีครบทั้ง 4 ฟิลด์)

```markdown
🔒 WIP (<agent名> session, YYYY-MM-DD): <何をするか1行>

agent: <agent名>
date: YYYY-MM-DD
Files to touch:
- path/to/file1        <!-- リポルート相対。ファイル名はそのファイルだけ -->
- path/to/dir/         <!-- 末尾スラッシュ = 配下すべて。glob・否定は禁止（L0-2） -->
Branch: fix/<issue>-<slug> (worktree)
```

- WIP ที่ขาดฟิลด์ใดฟิลด์หนึ่งจาก 4 ฟิลด์ (agent / date / Files to touch / Branch) ถือว่าล็อกไม่มีผล (L0-1)
- ถ้าคาดการณ์ไม่ได้ ให้ใช้ `Files to touch: UNKNOWN` = สำหรับงานแบบต่อเนื่อง (serial) เท่านั้น (L0-2)
- เลนที่คาดว่าจะเงียบนานเกิน 72h ต้องเขียนช่วง staleness ที่ยาวกว่านั้นไว้ในเนื้อหาอย่างชัดเจน **พร้อมเหตุผล** (คำประกาศข้อยกเว้นของ L0-3 การขยายเวลาในภายหลังต้องทำให้เห็นชัดผ่านคอมเมนต์ใหม่)

## คอมเมนต์ HOLD (L1-5 — ต้องมีครบทั้ง 5 ฟิลด์)

```markdown
⏸ HOLD (<agent名>, YYYY-MM-DD): <保留する理由1行>

owner: <agent名>
reason: <なぜ止めるか>
review-by: YYYY-MM-DD          <!-- 超過で可視のレビュー義務。ロックは明示処置まで保持・自動解放はされない -->
evidence: <失敗ログ・実行結果へのポインタ>   <!-- リトライ使い切り経由の HOLD では必須（L1-6）。それ以外は任意 -->
lock disposition: retained until review-by | released   <!-- 無言は HOLD 無効 -->
remaining work / successor: <残作業 or 引き継ぎ先>
```

## คอมเมนต์สถานะสิ้นสุด (L1-4 — MERGED / SUPERSEDED / ABANDONED)

```markdown
🏁 <MERGED|SUPERSEDED|ABANDONED> (<agent名>, YYYY-MM-DD): <1行>

evidence / successor: <PR リンク・後継 Issue・打ち切りの証拠（L1-6）>
```

## คอมเมนต์ TAKEOVER (L0-3 — การรับช่วงเลนที่ stale)

```markdown
🔁 TAKEOVER (<agent名>, YYYY-MM-DD)

stale WIP: <引用（宣言者・日付・最終更新からの経過時間）>
resume checklist: <L0-9 チェック結果コメントへのリンク or 本文に併記>
```

ให้โพสต์คอมเมนต์ WIP ใหม่ (ตามรูปแบบด้านบน) ทันทีหลังจากนั้น

## คอมเมนต์ RELEASE / HANDED-OFF (L0-3 — คอมเมนต์วงจรชีวิตของล็อก ไม่ใช่สถานะเลน)

ผู้ที่โพสต์ได้มีเพียง **เจ้าของล็อก (agent ที่โพสต์ WIP) เท่านั้น** ช่องทางเดียวที่ผู้อื่นจะปลดล็อกได้คือผ่าน stale + TAKEOVER

```markdown
🔓 RELEASE (<agent名>, YYYY-MM-DD): <ロックを手放す理由1行。レーン状態は L1-4 のコメントで別途宣言>
```

```markdown
🤝 HANDED-OFF (<agent名>, YYYY-MM-DD) → <引き継ぎ先 agent名>

handoff note: <続きの入口・残作業へのポインタ>   <!-- 引き継ぎ先は書き込み前に L0-9 を実施 -->
```

## คอมเมนต์เช็คลิสต์การกลับมาทำงานต่อ (L0-9 — ก่อนการเขียนครั้งแรกของการกลับมาทำงานต่อ・การส่งต่องาน・TAKEOVER)

```markdown
✅ Resume check (<agent名>, YYYY-MM-DD)

1. lock: mine | lapsed per L0-3（根拠1行）
2. file scope: 宣言集合は origin/main に照らして正確 / アクティブ WIP・PR と非交差
   （gh issue list + gh pr list --state open 再実行済み）
3. branch: fetch/rebase clean（コマンドと結果）
4. Done when: handoff 時から変更なし | 変更あり → <対応>
```

กำหนดตายตัวไว้ที่ 4 หัวข้อ ห้ามเพิ่ม (L0-9)

## บันทึกความสำเร็จ (L1-7 — merge gate ที่แปะไว้ในเนื้อหา PR)

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

การแก้ไขให้เผยแพร่บันทึกแทนที่ใหม่และเปิดรีวิวอีกครั้ง (L1-8) ห้ามแก้ไขแบบเงียบๆ
