> **Machine translation.** The Japanese original ([04-adoption.md](../../../docs/04-adoption.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# How to Adopt — Integrating into Each Agent's Environment

## Principles

- **This repository is the source of truth.** Each agent places a **summary** in its own "always-loaded context" location, and refers to this repo for details
- If the summary and this repo disagree, **this repo wins**. Update the summary to match
- Place it in an "always-loaded config file" so it keeps working even when the model changes (don't rely on a specific model's memory or attentiveness)

## Discipline for the Summary Block

- **This page (docs/04) is the single owner of the version-stamped compact summary.** Downstream copies (each CLAUDE.md / AGENTS.md / system prompt) are owner-applies — the coordinating agent proposes it, and each runtime's owner pastes it in themselves
- Downstream local summaries or overrides **may be stricter than the source of truth, never looser** (tighten only). The cross-agent norm owner for this principle is family-os's operations-policy (config trust section — see the "Caty AI Family" section of the [README](../../../README.md)). This page is that collaboration protocol's application. When adopting without sister projects, just apply the tighten-only principle as-is
- The summary doesn't copy out the full text — it refers to things via **rule ID + a one-line posture**. The defining text for each ID lives in docs/01–03 and 05–08; the field schema for the comment format lives in templates/issue-template.md, templates/epic-template.md, and templates/brief-template.md

## Where to Integrate, Per Agent

Each runtime has a different "always-loaded config file." Keep an adoption ledger in this shape:

| Agent | Always-loaded context | Status |
|---|---|---|
| `<agent-a>` (e.g. the Claude Code family) | User-global config such as `~/.claude/CLAUDE.md` (the section treated as permanent) | e.g. ✅ Adopted (YYYY-MM-DD) |
| `<agent-b>` (e.g. a resident agent runtime) | Each agent's system prompt / the workspace's `AGENTS.md` | e.g. ✅ Adopted — the rule-ID version is distributed via owner-applies |
| `<agent-c>` (e.g. an operations-notes-driven agent) | Operations notes / reference docs for its skill set | e.g. ⬜ Not yet adopted — distribute the summary block |

> Keep the live adoption ledger under each team's own control. As more targets get adopted, maintain this table in your own repository (using an Issue's comments as the ledger works too).

## Distributable Summary Block (Copy-Paste)

Paste the following as-is into each agent's always-loaded context:

```markdown
## 並行開発プロトコル要約（handbook-revision: 2026-08-07 / owner: 貼った本人名 / last-verified: 貼った日付）
正本: <このハンドブックの正本リポ URL（fork した場合は fork 先）> — 食い違えば正本が正。
この要約は厳しくしてよいが緩めるのは禁止。ID の本文は正本 docs/01〜03・05〜08、様式は templates/issue-template.md・epic-template.md・brief-template.md。

L2 並行可否: L2-1 ゴール合意・重さ判定（迷えば重い側）・設計を難しくする要件は一度疑う（消す決定は依頼者） / L2-2 境界変更は境界PR1本先行 /
  L2-3 Issue に触るファイル予測必須 / L2-4 並行GO=宣言ファイル集合が非交差のみ /
  L2-5 広域Issueは単独実行 / L2-6 ホットスポットは並行安全マップ+分割投資
L1 Issue完遂: L1-1 Issue-first / L1-2 Why・Done when・触るファイル予測 /
  L1-3 merge レビュー=別モデル or 別エージェント・self-approve 禁止 /
  L1-4 レーン状態は WIP/HOLD/MERGED/SUPERSEDED/ABANDONED の5語彙・不明状態=非アクティブ扱い /
  L1-5 HOLD は owner/reason/review-by/lock disposition/残作業or後継 必須 /
  L1-6 リトライ有限・尽きたら証拠付き HOLD/ABANDONED / L1-7 merge は完了記録（Done when→PASS/FAIL/理由付きN/A・
  証拠・候補SHA・diff照合）必須 / L1-8 訂正は差し替え記録で（黙った編集禁止） /
  L1-9 サイズ L/H/Epic（=L2-1 の重い側・アーキ・要件含む）は実装着手前に異種レビュー（S/M 単発Issueには課さない） /
  L1-10 席は相互異種+writer異種・設計/実装者は席に数えない・適格モデル名簿はローカル設定・requested/actual記録 /
  L1-11 席数 S/M=異種2・L/H=異種3・高リスク領域=5（サイズより優先）・Epic上流=実装着手前L/H・確保不能はオーナー承認の降格 or SEAT-WAIT
L0 git: L0-1 被り確認+WIP 4フィールド（agent/date/Files to touch/Branch）=ソフトロック /
  L0-2 宣言外は触らない・UNKNOWN=直列 / L0-3 stale=72h・引き取りは TAKEOVER+再開チェック+新WIP宣言 /
  L0-4 1セッション=1Issue=1branch=1worktree / L0-5 main マージ専用 /
  L0-6 PR にファイル一覧+diff照合 / L0-7 マージ1本ずつ / L0-8 ブランチ短命・HOLD 明示 /
  L0-9 再開・引き継ぎは4点チェックを Issue に投稿してから書く
B 委譲ブリーフ: B-1 実質的な委譲（実装・修正・生成）は3層必須（実装仕様/実装チェック/レビュー基準・様式は brief-template.md） /
  B-2 読み捨ての調査・短い質問は免除・迷えば付ける / B-3 Issue が正本・ブリーフは導出物（食い違えば Issue を先に直す） /
  B-4 文脈は前積み・委譲先に探索させない・レビュー委譲は最悪の失敗形を名指し・独立席には結論を混ぜない /
  B-5 見出しは固定文字列で機械判定できる形に保つ・検査が無い環境でも契約は有効
E Epic レーン: E-1 Epic はオーナーのキックオフ承認で成立（承認前は通常Issue運用） /
  E-2 機能軸Epic×モジュール軸子Issue・契約凍結#0を先行しマージまでEpic内直列 /
  E-3 人間チェックポイント表=事前合意した地点でのみ停止・高リスク領域+契約級逸脱は必須行・
  表の緩和はオーナー再承認まで旧表有効・表なし=Epic不成立 /
  E-4 epic統合ブランチ・子→epicはPRで1本ずつ・mainへは完了時1回既定（中間マージは事前記載+フルゲートの例外） /
  E-5 サンドボックス自由権=禁止列挙以外自由（main直push・スコープ外・他レーン・epic履歴書換・秘密外送・無承認CP実行が禁止） /
  E-6 砂時計レビュー: 設計=Epic1回（実装着手前）・実装=子の重さでライトゲート（高リスク子は5席優先・証拠フロア維持:
  マージ時head一致SHA・diff照合・identity・インライン証拠）・統合=epic→mainフルL1-7 /
  E-7 Epicログ（未達・妥協の列挙必須）+ダイジェスト最終確認 /
  E-8 寿命1〜2週間（起点=キックオフ承認）・staleness は L0-3 の別時計 / E-9 終端も5語彙・ABANDONED はブランチ処分+子収束必須 /
  E-10 Epic並走=子宣言の和集合∪EPIC WIP宣言で L2-4 準用
LC ライフサイクル: LC-1 置く時に退場トリガー（期限 or 完了条件）を必ず一緒に決める（トリガー無し=永久保持になる前提で扱う） /
  LC-2 持続領域は受け取り→現役→完成→退蔵の一方通行・退蔵は不変・復元は消さず新規コピー（git branch / worktree は対象外=L0-4 / L0-8） /
  LC-3 3類型の退場条件を数値つきでローカル設定に明文化（数値は正本に書かない） /
  LC-4 追記型と宣言したストアに限り退場はバックアップ→移動→ポインタ残置の3点セット・実作業は常に手動 /
  LC-5 検査・lint はファイルを動かさない（検知→定期レポート→人が判断・自動退場なし）
FP: 検証不能なら直列（書き込み・merge も停止側に倒す）。fail-open は「通過」を意味しない。Epic チェックポイント表が不在・未承認なら人間へエスカレーション（FP-9）。（詳細: 正本 docs/05）
```

## Repository-Side Preparation

For a new repo (or a repo applying this protocol for the first time):

1. Add a "parallel safety map" section to `ARCHITECTURE.md` ([template](../templates/architecture-parallel-map.md))
2. Place the Issue template ([templates/issue-template.md](../templates/issue-template.md)) in `.github/ISSUE_TEMPLATE/` (optional but recommended)
3. Have everyone follow a practice of avoiding direct pushes to main (enable branch protection where possible)

## Role Assignment Is Free Per Agent

Which model or tool handles implementation / review / verification is left to each agent's toolchain (e.g. a three-role, different-model setup like implementer=Codex / reviewer=GLM / verifier=Claude). **What must be preserved is the protocol (the three layers + cross-review + fail-posture) — not the specific tooling.**
