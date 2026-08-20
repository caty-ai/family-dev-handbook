> **แปลโดยเครื่อง** ต้นฉบับภาษาญี่ปุ่น ([publication-checklist.md](../../../templates/publication-checklist.md)) เป็นฉบับหลัก — หากหน้านี้ขัดกับต้นฉบับ ให้ยึดข้อความภาษาญี่ปุ่นเป็นหลัก

# เช็คลิสต์การเผยแพร่รีโพ

## วัตถุประสงค์

เช็คลิสต์นี้คือฉบับหลักสำหรับบันทึกว่าเลนเผยแพร่รีโพได้ผ่านประตูของ [PB-1](../docs/11-publication.md#pb-1) ด้วยการตัดสินและหลักฐาน artifact รายข้อแล้ว

⟨RS-n⟩ = หมายเหตุที่มาจากประตูก่อนเผยแพร่ในท้องถิ่นของแต่ละบ้าน แม้ไม่มีจุดอ้างอิง แต่ละรายการก็สมบูรณ์ในตัวเอง

ID ของรายการไม่ใช่ rule ID แต่ให้ปฏิบัติเหมือนเป็น ID ที่คงที่เช่นเดียวกัน การเพิ่มให้ต่อท้ายแต่ละหมวด การลบให้เว้นหมายเลขไว้

## กฎเวอร์ชัน

ตาม [PB-2](../docs/11-publication.md#pb-2) โดยหลักแล้วให้บันทึกแท็ก release ของ handbook ที่อ้างอิง เฉพาะกรณีที่รันในสถานะที่ยังไม่รวมอยู่ในแท็กเท่านั้น ให้บันทึก commit SHA แล้วเพิ่มแท็กที่รวมสถานะนั้นไว้ในบันทึกความเสร็จสมบูรณ์หลังจากมีแท็กออกมา

```text
checklist version: <handbook release tag>
# タグ未包含時だけ
checklist commit: <full commit SHA>
checklist release tag (追記): <その状態を含む handbook release tag>
```

## ขั้นตอนของผู้บริโภค

1. รวบรวมหลักฐาน artifact ที่แต่ละรายการกำหนดไว้ สำหรับทั้ง 28 รายการตั้งแต่ A1〜E4
2. วางตารางต่อไปนี้ไว้ **พอดี 1 ตาราง** ในบันทึกความเสร็จสมบูรณ์ของ Issue ของเลน การตัดสินเป็นหนึ่งใน `PASS` / `FAIL` / `N/A` พร้อมเหตุผล และช่องหลักฐานให้เขียนตัว artifact เองหรือตัวชี้ที่แก้ปัญหาได้ตามที่รายการกำหนด

   ```markdown
   | ID | 判定 | 証拠 artifact | 注記 |
   |---|---|---|---|
   | A1 | PASS / FAIL / N/A（理由） | <項目指定の証拠> | <必要な補足> |
   ```

3. การเผยแพร่ซ้ำแบบ public→private→public ให้อ้างอิงบันทึกความเสร็จสมบูรณ์ล่าสุด แล้วรันใหม่เฉพาะรายการที่เปลี่ยนไปตั้งแต่ครั้งก่อนและรายการที่ผลอาจเปลี่ยนไปจากการเผยแพร่ซ้ำ ตารางใหม่ต้องมีครบทั้ง 28 รายการ หลักฐานที่ใช้ซ้ำให้เขียนที่มาอ้างอิง ส่วนหลักฐานที่รันใหม่ให้เขียน artifact ของครั้งนี้
4. หากพบความคลุมเครือ・ขาด・จัดประเภทผิด ให้รายงานเป็นช่องว่างไปที่ [Issue #100](https://github.com/caty-ai/family-dev-handbook/issues/100)

เวลาที่ใช้ของรายการ (c) มีเพียงเลนผู้บริโภคที่ [PB-5](../docs/11-publication.md#pb-5) ระบุไว้เท่านั้นที่วัด

รายการ (b) เมื่อมีการทำให้เป็นกลไกแล้ว ให้แทนที่ขั้นตอนมือของบรรทัดนั้นด้วย run URL

ช่องประเภทเก็บต้นฉบับของ[ฉบับยืนยันของ Phase 2](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5355210694) ไว้: **(a)** = การตรวจเชิงกลไกด้วย handbook reusable ที่มีอยู่แล้วในวันนี้, **(b)** = ทำให้เป็นกลไกได้แต่ยังไม่ได้ทำ, **(c)** = การตัดสินของมนุษย์ที่ผ่านได้เฉพาะด้วยป้ายหรือบันทึกการตัดสินของ owner เท่านั้น

## A — โครงสร้างเริ่มต้นของรีโป (โครงสร้างและทางเข้า)

| ID | รายการ | ประเภท | วิธีผ่านวันนี้ | หลักฐาน artifact |
|---|---|---|---|---|
| A1 | ตั้งแต่สร้างรีโปให้มี CI ที่ใช้ test เป็น gate (T-1) หากยังไม่มี CI อย่าแสร้งว่าเขียว ให้เขียน `CI: not yet` ใน README | (b) — no bootstrap conformance check exists; T-1 is prose | ตรวจด้วยตาว่ามี test-lint caller อยู่และ pin แล้วหรือไม่ แล้วรัน หากยังไม่จัดเตรียมให้ตรวจสอบ `CI: not yet` ที่ชัดเจนใน README | run URL ครั้งแรกของ test-lint caller หรือ `CI: not yet` ที่เขียนไว้ชัดเจนใน README |
| A2 | มีทางเข้า `make test` / `make lint` และส่งต่อ exit code (campaign rule 4 ตรวจให้ถึงขั้นที่ make กลายเป็น Error เมื่อบังคับให้ล้มเหลว) | (b) — checkable by a bootstrap script; today proven only by seat sandbox runs | รัน `make test` กับ `make lint` แล้วใส่ความล้มเหลวโดยตั้งใจในสถานะงานที่แยกไว้ต่างหาก เพื่อยืนยัน exit code ที่ไม่ใช่ 0 | transcript การรันในเครื่อง + หลักฐานความล้มเหลวที่บังคับให้เกิด |
| A3 | ห้ามทำให้ lint target เป็น no-op ห้ามวาง lint ที่ล้มเหลวไม่ได้ไว้หลังแบดจ์สีเขียว | (b) — mechanizable as "lint job must have ≥1 failable step / placeholder-echo detector" | ใส่การละเมิด lint ชั่วคราว แล้วยืนยันว่า lint กลายเป็นสีแดงในสถานะงานที่แยกไว้ต่างหาก | หลักฐานว่า mutation ที่ใส่การละเมิด lint กลายเป็นสีแดง |
| A4 | มี gate caller ทั้ง 5 ตัว (test-lint / pr-size / review-labels / gitleaks / history-check) ถูก pin ไว้ที่ `@ci-v1` และตรงกับฉบับหลักใน `templates/ci` แบบ byte-identical โดยไม่ copy ตรรกะการสแกนไว้ในรีโปเอง | (a) today the *identity* is seat-verified by hand; caller presence is machine-fact | บันทึก run URL ครั้งแรกของ caller ทั้ง 5 แล้วเทียบ SHA256 ของแต่ละไฟล์กับฉบับหลัก | การเทียบ SHA256 กับฉบับหลัก + run URL ครั้งแรก |
| A5 | เดินสาย reconciliation ของ T-6 แล้วเปิดใช้งานด้วย `require_suite_reconciliation: true` ค่าเริ่มต้น false ยังถือเป็น inert gate | (b) — flag presence is greppable; today unchecked | ตรวจค่า input ของ caller แล้วรัน test-lint เพื่อยืนยันว่าค่าทั้ง 3 ของสรุปตรงกัน | green run ที่แสดง `declared=N executed=N skipped=K` |
| A6 | ลงทะเบียน branch protection / required checks แล้วทำให้ gate เป็น blocking ไม่ใช่แค่คำแนะนำ (ตรวจสถานะของ `branches/main/protection`) | (c) today (owner-only settings) / (b) verifiable half: a read-only API probe can red-flag absence | ป้ายของ owner / บันทึกการตัดสินที่เข้าเงื่อนไขผู้ออกของ PB-3 | เอาต์พุตของ API probe + บันทึกการกระทำของ owner (404 ของ `branches/main/protection` แยกไม่ได้ระหว่าง "ไม่มีการป้องกัน" กับ "สิทธิ์ไม่พอ" ผลลัพธ์ probe ที่คลุมเครือจึงไม่ถือว่าผ่าน วัด `rulesets` ควบคู่ไปด้วย — รูปแบบที่ทำจริงใน Phase 1 §3.5) |

## B — ความซื่อตรงของการแสดงผล (README・แบดจ์・ตัวเลข)

| ID | รายการ | ประเภท | วิธีผ่านวันนี้ | หลักฐาน artifact |
|---|---|---|---|---|
| B1 | แบดจ์เขียวต้องมาจากเครื่องเท่านั้น แบดจ์ static ต้องอยู่ในรายการปิดสีที่อนุญาตของ T-7 และ URL ของแบดจ์ทุกตัวต้องแก้ปัญหาได้ | (b) — badge-lint (slug points at this repo, endpoint 200, color allowlist) is a concrete gap | ดึง URL ของแต่ละแบดจ์ แล้วเทียบรีโปเป้าหมาย・การตอบสนอง HTTP・สี static กับ T-7 | transcript ของ curl แต่ละแบดจ์ |
| B2 | ตัวเลขที่วัดจริงด้วยมือต้องมีวันที่และแหล่งที่มาที่แก้ปัญหาได้ ("จำนวนที่ไม่มีวันที่ = 0") | (c) with a (b) assist: a date-adjacency lint can flag bare numbers; truth needs a human | ป้ายของ owner / บันทึกการตัดสินที่เข้าเงื่อนไขผู้ออกของ PB-3 | grep sweep + บันทึก |
| B3 | มีตารางสภาพแวดล้อมที่รองรับ ⟨RS-1⟩、hero image ⟨RS-2⟩、README 4 ภาษาที่มี nav ไขว้กัน ⟨RS-4⟩、โครงสร้าง docs แบบ 3 ชั้น | (b) — presence/cross-link lint is trivial; content quality stays (c) | ตรวจการมีอยู่และลิงก์ไขว้โดยรัน publication-gate และบันทึกรายการไฟล์เป้าหมาย ส่วนคุณภาพเนื้อหาผ่านได้ด้วยป้ายของ owner / บันทึกการตัดสินที่เข้าเงื่อนไขผู้ออกของ PB-3 เท่านั้น | run ของ publication-gate (ขอบเขตที่ครอบคลุมบางส่วนวันนี้) + รายการไฟล์ |
| B4 | ทำ social preview เป็น 1280×640 ⟨RS-3⟩ และตั้ง description ของ Settings เป็นภาษาอังกฤษ ⟨RS-10⟩ | (c) — API-readable but set by owner; (b) probe possible | ป้ายของ owner / บันทึกการตัดสินที่เข้าเงื่อนไขผู้ออกของ PB-3 | API probe (เช่น `gh api repos/OWNER/REPO --jq .description`) |
| B5 | ทำให้คำกล่าวอ้างเรื่อง OS ถูกต้อง และทำให้ skip มองเห็นได้ ใช้ `run_macos` / `macos_skip_reason` และให้ skip ที่ไม่มีเหตุผลเป็นสีแดง | (a) — reusable enforces once caller adopts matrix inputs | บันทึก run URL ครั้งแรกของ matrix ของ test-lint reusable | run URL ครั้งแรกของ matrix ที่มี skip lane |
| B6 | ออกแบบ Issue label ไม่ให้ค้างอยู่ที่ 9 รายการเริ่มต้น ⟨RS-11⟩ มีแกน component: / platform: / severity: และไม่ให้ priority กับ severity อยู่ร่วมกัน | (b) — label-census script exists in spirit (.github#19: 11/11→14/14 measured by seats); no reusable | รันเอาต์พุตของ `gh api repos/OWNER/REPO/labels` แล้วตรวจแกนและการห้ามอยู่ร่วมกัน | เอาต์พุต census ของ `gh api .../labels` |

## C — ความลับและประวัติ

| ID | รายการ | ประเภท | วิธีผ่านวันนี้ | หลักฐาน artifact |
|---|---|---|---|---|
| C1 | ทำให้ gitleaks caller ผ่าน run ครั้งแรกจริง ระบุให้ชัดว่าสิ่งที่ reusable สแกนคือ PR range ของ merge-base..HEAD ไม่ใช่ full history และให้การสแกนประวัติทั้งหมดก่อนเผยแพร่ ⟨RS-6⟩ แยกต่างหากเป็น **must-pass** | (a) for PR-range; **(b) gap: one-shot full-history scan as a publication-time job** | บันทึก run URL ของ PR-range reusable จนกว่าจะมีการอิมพลีเมนต์ job สแกนประวัติทั้งหมด ให้รัน `gitleaks git --no-banner --redact --log-opts="--all" .` ที่ root ของรีโป แล้วบันทึกคำสั่ง・gitleaks version・exit code・เอาต์พุตทั้งหมดไว้ใน transcript | run URL ของ PR-range caller + transcript การสแกน full-history ด้วยมือ |
| C2 | ทำให้ history-check caller ผ่าน run ครั้งแรกจริง (gate ของ merge-base / unrelated histories range ที่ว่างเปล่าเป็น fail-closed) | (a) | บันทึก run URL ครั้งแรกของ history-check reusable | run URL ครั้งแรก |
| C3 | วาง `.publication-denylist` ให้เข้ากับ D8 denylist ที่ commit ต้องไม่เผย literal ของสิ่งที่ต้องป้องกัน ให้เลือกจาก 3 รูปแบบ คือ การเขียนแบบเผยแพร่ได้อย่างปลอดภัย / gitignore + การฉีดความลับเข้า CI / การยอมรับที่บันทึกไว้ชัดเจน | (a) for gate execution; **(c) for D8 choice** (which of the 3 options, recorded per repo); (b) gap: a literal-exposure self-scan on the denylist file itself | ป้ายของ owner / บันทึกการตัดสินที่เข้าเงื่อนไขผู้ออกของ PB-3 | run ของ publication-gate + บันทึกตัวเลือก D8 ที่บันทึกไว้ |
| C4 | sweep ข้อมูลภายใน ⟨RS-5⟩ ให้ครอบคลุมชื่อครอบครัว・path ส่วนตัว・`_handoffs/`・screenshot・test log ใน Issue / PR | (c) — judgment; publication-gate covers denylist-declared patterns only | ป้ายของ owner / บันทึกการตัดสินที่เข้าเงื่อนไขผู้ออกของ PB-3 | บันทึก sweep ที่แจกแจงขอบเขต |
| C5 | vendoring สคริปต์ publication-gate ให้ตรงฉบับหลักแบบ byte-identical และทำให้ embedded selftest เป็นสีเขียวในฐานะ counted suite ของ T-6 | (a) | บันทึก run URL ของ publication-gate selftest แล้วเทียบ blob identity กับฉบับหลัก | หมายเหตุ blob identity + run URL ของ selftest |

เหตุผลที่ทำให้การสแกน full-history ของ C1 เป็น must-pass และเหตุผลที่ให้ transcript ด้วยมือใช้ได้จนกว่าจะอิมพลีเมนต์ job อยู่ที่[การตัดสินของ owner ครั้งที่ 2 ใน #100](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5359570954)

## D — วินัยของการรีวิวและ merge

ต้นฉบับของ Phase 2 เรียงลำดับ D1, D2, D3, D7, D4, D5, D6 ในที่นี้เรียงตาม ID จากน้อยไปมากโดยไม่เปลี่ยน ID

| ID | รายการ | ประเภท | วิธีผ่านวันนี้ | หลักฐาน artifact |
|---|---|---|---|---|
| D1 | จัดที่นั่งรีวิวตามขนาด (L1-9 / L1-10) และบันทึก requested / actual fallback และ invalid vote ให้บันทึกไว้ตามความเป็นจริง ไม่นับการปฏิเสธที่ไม่มี verdict เป็นคะแนน | (c) — quorum is human process; (a) assist: review-labels reusable enforces label presence | ป้ายของ owner / บันทึกการตัดสินที่เข้าเงื่อนไขผู้ออกของ PB-3 | ตารางที่นั่งในบันทึกความเสร็จสมบูรณ์ |
| D2 | ผูก gate การอนุมัติของมนุษย์กับ head SHA / event ไม่ถือว่าการอนุมัติก่อน close→reopen ยังใช้ได้ ตรวจการผูกนี้หนึ่งครั้งต่อรีโป | (a) — the gate behaves this way today; checklist item is "verify the binding once per repo" | บันทึก run URL ของ review-labels reusable แล้วตรวจว่า head SHA กับ label event ตรงกัน | ส่วนที่ตัดมาจาก timeline |
| D3 | merge ด้วยการ `--no-ff` ในเครื่องโดยใช้ noreply identity แล้วบันทึกการเทียบ diff กับ PR manifest ตัวอย่างของ noreply email กับตัวอย่างที่เลือก merge ในเครื่องเพราะอุบัติเหตุ identity ของ API merge เป็นคนละเรื่องกัน | (c) process + (b) gap: a post-merge probe could verify merge-commit authorship/email pattern | ป้ายของ owner / บันทึกการตัดสินที่เข้าเงื่อนไขผู้ออกของ PB-3 | merge SHA + หมายเหตุ identity ในบันทึกความเสร็จสมบูรณ์ |
| D4 | สร้างบันทึกความเสร็จสมบูรณ์ที่มีฟิลด์ L1-7 และ**ห่วงโซ่ release / previous release ของ T-5** deferred ให้อ้างอิง Issue, N/A ให้เป็นประเภทปิด, แท็กต้องเป็น annotated ให้บันทึกไว้ | (c) today; **(b) gap: T-5 record-linter** (parse completion comments; verify tag exists+annotated+dereferences to merge SHA; walk 1-hop chain) — the fos#64 L1-8 record fixed exactly what this linter would catch (skipped v0.2.1 hop, non-resolving run IDs) | ป้ายของ owner / บันทึกการตัดสินที่เข้าเงื่อนไขผู้ออกของ PB-3 | URL ของบันทึกความเสร็จสมบูรณ์ + การตรวจสอบแท็ก |
| D5 | ยืนยันว่า run URL ทุกตัวในบันทึกแก้ปัญหาได้ไปยัง run ที่มีอยู่จริง และ head SHA ตรงกับ candidate SHA | (b) — resolvable-evidence linter is a concrete, high-value gap | ดึง run URL แต่ละตัวใหม่ แล้วบันทึกว่ามีอยู่จริงและ head SHA ตรงกัน | หมายเหตุการดึงข้อมูลใหม่ด้วยมือ |
| D6 | วางบันทึกความเสร็จสมบูรณ์ไว้ที่ Issue ของเลน และมีเพียง 1 บันทึกต่อ 1 เลนเท่านั้น | (b) partial: "exactly one completion record per closed lane Issue" is machine-checkable | ตรวจคอมเมนต์ของ Issue ของเลน แล้วบันทึกว่ามีบันทึกความเสร็จสมบูรณ์พอดี 1 ฉบับ | URL ของบันทึกความเสร็จสมบูรณ์ |
| D7 | ไฟล์ vendored canonical ที่เกิน pr-size ให้ใช้เพียงรูปแบบการประกาศเดียวคือ **label `size-exempt` ที่ owner ให้ + เหตุผลจาก blob identity ที่ตรงกับฉบับหลัก** การยอมรับแบบ advisory-red ในอดีตหรือไม่มี label เป็นประวัติที่ grandfathered ไม่ใช่ตัวอย่างให้ทำตาม | (c) choice of form is owner rule-making; (a) assist: pr-size gate + blob check | ป้ายของ owner / บันทึกการตัดสินที่เข้าเงื่อนไขผู้ออกของ PB-3 | เหตุการณ์ label `size-exempt` จากบัญชี owner + หมายเหตุ identity ของ blob SHA กับฉบับหลัก |

รูปแบบการประกาศเพียงหนึ่งเดียวของ D7 คือความต่างที่ตั้งใจซึ่งสะท้อน[การตัดสินของ owner ครั้งที่ 1 ใน #100](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5359570954)

## E — การเชื่อมต่อกับองค์กรและ registry

| ID | รายการ | ประเภท | วิธีผ่านวันนี้ | หลักฐาน artifact |
|---|---|---|---|---|
| E1 | วาง registry entry ที่มีสถานะ published และฟิลด์ pin ตามสัญญา #62 ไว้ใน `modules.json` ของ family-os แล้วทำให้ orphan check เขียวใน weekly run ถัดไป | (a) — family-os machine checks + weekly lane | บันทึก run URL ของ registry check ของ family-os | diff ของ registry + run URL ของ check |
| E2 | render family footer แบบ deterministic แล้วยืนยันว่า diff จากการรันซ้ำเป็น 0 | (a) — renderer + idempotence pattern (fma#24) | รัน renderer แล้วบันทึกว่า diff จากการรันซ้ำด้วย input เดิมเป็น 0 | transcript ของ diff จากการรันซ้ำ |
| E3 | สืบทอด org-default template หรือ override โดยตั้งใจ แล้วยืนยันผลด้วย `repository.issueTemplates` ของ GraphQL | (b) — probe script exists as recorded practice, not a reusable | รัน GraphQL query แล้วบันทึกรายการ template ที่ได้กลับมา | เอาต์พุตของ GraphQL |
| E4 | มี community health files ⟨RS-9⟩、LICENSE=MIT/Caty ⟨RS-8⟩ และรัน quickstart แบบ copy&paste ได้ ⟨RS-7⟩ | LICENSE presence (b)-trivial; quickstart (c) — human execution | ตรวจและบันทึกการมีอยู่ของ LICENSE และ community health files ผ่าน API / หน้า community standards ส่วนคำตัดสินการรัน quickstart ผ่านได้ด้วยป้ายของ owner / บันทึกการตัดสินที่เข้าเงื่อนไขผู้ออกของ PB-3 เท่านั้น | screenshot / API ของ community standards + transcript การรัน |
