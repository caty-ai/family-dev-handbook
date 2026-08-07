> **机器翻译。**日文原文（[epic-template.md](../../../templates/epic-template.md)）是正本 — 本页与原文不一致时，以日文为准。

# EPIC Issue / Epic 通道模板

Epic 通道（[docs/06](../docs/06-epic-lane.md)・E-1〜E-10）字段架构的权威文档。单个 Issue、WIP/HOLD 等评论格式仍沿用 [issue-template.md](issue-template.md)（Epic 内的子 Issue 也使用该文档）。

## EPIC Issue 正文（E-1 / E-2 / E-3 / E-10）

```markdown
## 目的 (Why) — 機能軸

<!-- 人間の言葉で価値を書く。モジュール名ではなく「何ができるようになるか」 -->

## 完了条件 (Done when) — Epic レベル

- [ ] <!-- 統合状態で判定できる形で（子の Done when の単純合算にしない） -->
- [ ] 統合レビュー（E-6③ フル L1-7）通過・epic→main マージ

## 子 Issue 一覧 — モジュール軸

<!-- 1子 = 1モジュール or 1リポ。依存は Blocked-by で。
     契約凍結の第0号はモジュール境界のインターフェースに触る Epic のみ必須（E-2）— 触れない Epic では行0を省略し、
     E-3 の契約級判定は Done when・外部IF 記述で行う -->

| # | Issue | モジュール / リポ | Blocked-by |
|---|---|---|---|
| 0 | #<n> 契約凍結（境界インターフェース確定） | <対象> | — |
| 1 | #<n> | <対象> | #0 |

## 実効宣言集合（E-10 — 子の宣言集合の和集合 ∪ EPIC Issue の WIP 宣言集合）

<!-- Epic 間・Epic 外レーンとの並行GO判定（L2-4 準用）の入力。子の増減・epic worktree の統合作業対象（E-4 の WIP）で更新する -->

- path/to/module-a/
- path/to/module-b/

## 人間チェックポイント表（E-3 — 必須セクション）

<!-- 必須トリガー（高リスク領域の全項目 + 契約級の逸脱）は該当の有無を必ず行にする（該当なしなら「該当なし」と書く）。
     行の追加はエージェント単独可（ただし既存行を狭める内容は緩和扱い）。行の削除・緩和はオーナー再承認まで旧表が有効（FP-8 / L1-8）。
     通過承認はオーナーの明示コメントのみ — 状態欄の書き換え自体は承認を生まない（E-3 / FP-8） -->

| # | どこで止まるか | 何を見せるか | なぜ人間判断か | 状態 |
|---|---|---|---|---|
| 1 | <例: 子#3 完了後・外部公開の直前> | <例: ステージング URL + 差分要約> | 対外公開（高リスク領域） | 未到達 / 承認済み YYYY-MM-DD + 承認コメント URL |

## キックオフ承認（E-1 — Epic 成立の証跡）

<!-- オーナーの承認コメントへのリンクを貼る。承認前は Epic 未成立（E-4/E-5 の特権なし・FP-9）。
     設計レビューの締切は L1-9/E-6① と同一の時計（遅くとも最初の子 Issue の実装着手前）— 独自の締切を作らない。
     キックオフ時点で未実施なら「未実施」と書き、実施・記録まで子の実装に着手しない（L1-9 fail-closed） -->

- 設計レビュー記録（E-6①/L1-9 — 席・requested/actual・verdict）: <URL または「未実施（最初の子の実装着手前に必須）」>
- 承認コメント: <URL>（YYYY-MM-DD）
```

## Epic 日志评论（E-7 — 每当子 Issue 终结时发布到 EPIC Issue）

```markdown
📦 Epic log (<agent名>, YYYY-MM-DD): 子 #<n> 終端

- できるようになったこと: <1〜3行>
- 証拠: <子→epic PR リンク + 要点（テスト結果の終端値など）>
- Done when 未達・妥協事項: <列挙。無ければ「なし」と明記 — 省略不可>
- 次: <次に動く子 Issue / 待ち>
```

## 子→epic 轻量门禁记录（E-6② — 写在子→epic PR 正文中）

```markdown
## ライトゲート記録 (E-6②)

candidate SHA: <commit SHA>   <!-- マージ時点の PR head と一致していること。レビュー後に変わったら再レビュー（E-6②・L1-8 準用） -->
implementer: <agent/model>
reviewers: <席1: agent/model（requested/actual）> <席2: …>   <!-- 席数は子の重さで L1-11 表を引く。高リスク領域を触る子は5席 -->
identity check: <別モデル | 別エージェント>   <!-- L1-3。空欄は blocking -->

テスト結果（インライン終端値）: <例: 24 passed / exit 0 / YYYY-MM-DD>
要点: <Done when への対応を文章で。表形式は省略可。リンクだけの証拠は不適合（L1-7 の「記録単体で終端結果が読める」原則維持）>

宣言 vs 実 diff（L0-6 — 子→epic でも必須）:
git diff --stat <epic>...<候補SHA>: <出力 or 要約>
宣言ファイル集合との差分: なし | <差分と説明>   <!-- diff にあって宣言にないファイルは blocking -->
```

## Epic 终结评论（E-9 — 发布到 EPIC Issue。适用 L1-4 的 5 个词汇）

```markdown
🏁 <MERGED|SUPERSEDED|ABANDONED> (<agent名>, YYYY-MM-DD): <1行>

- epic ブランチの処分: 破棄（削除） | 救出 PR <URL>（E-6③ ゲート適用）
- 子 Issue の状態収束: <各子の終端状態 or 独立 Issue への切り出し先>
- worktree 掃除: 済み（YYYY-MM-DD）
- evidence / successor: <統合レビュー記録・後継 Issue 等>
```
