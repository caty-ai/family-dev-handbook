# templates/conformance — 席決定の検証ベクタ（conformance vectors）

各メンバー（家）のセレクタ実装（席決定機構）が **L1-9 / L1-10 / L1-11 / FP-7 と同じ答えを出すか**を、実装非依存で自己検証するためのベクタ集。法の正本は [docs/02](../../docs/02-issue-loop.md) と [docs/05](../../docs/05-fail-posture.md) — **ベクタと条文が食い違えば条文が正**（ベクタは条文の導出物であり、条文を上書きしない）。

実名モデル ID は含まない（L1-10 — 実名はデータ層・ハンドブック外）。語彙はすべて抽象 ID: `model-a`〜 / 系統 `family-a`〜 / 実装 writer `model-w` / メンバー `member-a`。

## ファイル

| ファイル | 内容 |
|---|---|
| `vectors-v1.json` | ベクタ集 v1（23本・JSON・依存ゼロで読める） |
| `README.md` | 本書（流し方・スキーマ意味論） |

## ベクタの構造

各ベクタ = `{id, slug, kind, rule_ids, given, expect, notes}`。

- **kind**: `panel`（席構成の適法性）/ `seat_wait`（SEAT-WAIT 宣言の有効性）/ `record`（レビュー記録の形式要件）。
- **given** の主なフィールド（`panel`）:
  - `review_stage`: `merge`（実装レビュー）/ `upstream`（L1-9 上流レビュー）
  - `size`: S / M / L / H / Epic（判別基準の正本は L2-1）
  - `high_risk`: 高リスク領域か（定義の正本は docs/06 冒頭・サイズ判定より優先）
  - `member_floor3`: S/M 床3の per-member 発効状態。`pinned_issue`: `complete`（3フィールド記録済み）/ `missing_fields` / `absent`、`effective`: 発効済みか。S/M 以外では `null`（床3は S/M のみの概念）
  - `writer`: 実装 writer のモデルと系統
  - `selection_path`: `named_panel`（オーナー名指し固定）/ `machine`（抽選・代打など機械選出）
  - `seats`: 席の列挙。`agent`（同一モデル別エージェントの区別）、`downgrade`（L1-11 降格手続き: `owner_approval` / `noted_in_review_record`）、`role_conflict`（`designer` 等 — 審査対象を設計・実装した者）を持ちうる
  - `exception_record`: L1-10 の同系統例外レコード（correlated-seats フラグ/機械経路の記録された例外 — **同一のレコード型**）。`fields_present` は `scope / pair / reason / approved_by / date / writer_condition` の部分集合、`scope_covers_lane` は scope が当該レーンを覆うか
  - `review_record`: `cites_correlated_seats`（適用の明記）/ `requested_actual_present`（requested/actual model の記録）
- **expect**:
  - `panel`: `required_seats`（この状況で法が要求する席数）/ `lawful` / `failure_class`（`underseated` ほか — ファイル冒頭の `failure_classes` 参照）
  - `seat_wait` / `record`: `valid`
- **notes**: 根拠条文の要約（日本語）。判定に使うのは `rule_ids` の条文本体。

## メンバー側での流し方（adapter パターン）

セレクタの入出力形式はメンバーごとに違う。共通形式に合わせるのではなく、**ベクタの `given` を自分のセレクタ入力へ写像する薄い adapter を1枚**書き、セレクタの出力を `expect` と突合する:

1. `vectors-v1.json` を読み込む（JSON — stdlib で足りる）
2. ベクタごとに `given` を自分のセレクタの入力（roster / 設定 / フラグ）へ変換する。抽象モデル ID はダミー登録でよい（実在モデルへ写像しない — ベクタは法の検証であり可用性の検証ではない）
3. セレクタを実行し、`expect` と比較する（`panel` は要求席数と適法判定、`seat_wait`/`record` は有効性判定）
4. **セレクタが表現できない given を持つベクタは skip ではなく FAIL として数える**（fail-closed — 表現できない = その法域を検証できていない）。恒久的に対象外の条項（例: セレクタが SEAT-WAIT コメントの形式検査を持たない設計）は、adapter 側に理由つき N/A 一覧として明文化する
5. 結果（passed / failed / N/A+理由）を自分のリポの CI か検証記録に残す

```
# 例: ベクタ一覧の確認
python3 -c "import json; d=json.load(open('vectors-v1.json')); print(len(d['vectors']), d['vectors_version'])"
```

## バージョニング

- ベクタの意味が変わる変更（追加・修正とも）は `vectors-v2.json` として**別ファイルで追加**し、旧版は残す（メンバーの採用記録が版を指すため）。
- メンバーが「どの版で自己検証したか」は各家の採用状態記録（例: family-memory-architecture の member-state `vectors_version`）が持つ。
- 本ディレクトリは docs/ 条文と違い i18n ミラー対象外（`templates/ci` と同じ扱い — ベクタ本体は言語非依存の JSON）。

## LC-1（退場トリガー）

ベクタ版は対応する条文改訂（本書の law_anchor）に従属する。席数・手続きを変える条文改訂が merge されたら、同一リリース内でベクタの追補版を出すか、出せない理由を Issue に残す（法とベクタの乖離は「静かに古い法を検証し続ける」劣化窓になる）。
