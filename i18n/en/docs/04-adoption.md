> **Machine translation.** The Japanese original ([04-adoption.md](../../../docs/04-adoption.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# How to Roll Out — Integrating into Each Agent Environment

## Principles

- **This repository is the source of truth**. Each agent places a **summary** in whatever location loads into its own "always-on context," and refers to this repo for details
- If a summary and this repo disagree, **this repo wins**. The summary side must be brought into line
- Place it in a "config file that always gets loaded" so it keeps working even when the model changes (don't rely on a specific model's memory or attentiveness)

## Discipline for summary blocks

- **This page (docs/04) is the sole owner of the version-stamped compact summary**. Downstream copies (each CLAUDE.md / AGENTS.md / system prompt) are owner-applies — the coordinating agent proposes, and each runtime's owner pastes it in themselves
- Downstream local summaries and overrides **may be made stricter than the source of truth, but never looser** (tighten only). The cross-agent normative owner of this principle is family-os's operations-policy (config trust section — see the "Caty AI Family" section of the [README](../../../README.md)). This page is the application of that shared protocol. When adopting without sister projects, just apply the tighten-only principle as-is
- Summaries reference rule IDs with **rule ID + a one-line posture**, not full prose copies. The defining text for each ID lives in docs/01–03, 05–07; the comment format's field schema lives in templates/issue-template.md, templates/epic-template.md, templates/brief-template.md

## Where to integrate, by agent

Each runtime has a different "config file that's always loaded." Keep the rollout ledger in this shape:

| Agent | Always-on context | Status |
|---|---|---|
| `<agent-a>` (e.g., Claude Code family) | User-global config such as `~/.claude/CLAUDE.md` (sections treated as permanent) | e.g. ✅ Adopted (YYYY-MM-DD) |
| `<agent-b>` (e.g., a resident agent runtime) | Each agent's system prompt / the workspace's `AGENTS.md` | e.g. ✅ Adopted — rule-ID version distributed owner-applies |
| `<agent-c>` (e.g., an ops-note-driven agent) | Ops notes / reference docs for the skill set | e.g. ⬜ Not yet adopted — summary block distributed |

> Keep the living ledger of actual rollouts under each team's own control. As more integration points appear, maintain this table in your own repository (using Issue comments as the ledger also works).

## Summary block for distribution (copy-paste)

Paste the following as-is into each agent's always-on context:

```markdown
## 並行開発プロトコル要約（handbook-revision: 2026-08-06 / owner: 貼った本人名 / last-verified: 貼った日付）
正本: <このハンドブックの正本リポ URL（fork した場合は fork 先）> — 食い違えば正本が正。
この要約は厳しくしてよいが緩めるのは禁止。ID の本文は正本 docs/01〜03・05〜07、様式は templates/issue-template.md・epic-template.md・brief-template.md。

L2 並行可否: L2-1 ゴール合意・重さ判定（迷えば重い側）・設計を難しくする要件は一度疑う（消す決定は依頼者） / L2-2 境界変更は境界PR1本先行 /
  L2-3 Issue に触るファイル予測必須 / L2-4 並行GO=宣言ファイル集合が非交差のみ /
  L2-5 広域Issueは単独実行 / L2-6 ホットスポットは並行安全マップ+分割投資
L1 Issue完遂: L1-1 Issue-first / L1-2 Why・Done when・触るファイル予測 /
  L1-3 merge レビュー=別モデル or 別エージェント・self-approve 禁止 /
  L1-4 レーン状態は WIP/HOLD/MERGED/SUPERSEDED/ABANDONED の5語彙・不明状態=非アクティブ扱い /
  L1-5 HOLD は owner/reason/review-by/lock disposition/残作業or後継 必須 /
  L1-6 リトライ有限・尽きたら証拠付き HOLD/ABANDONED / L1-7 merge は完了記録（Done when→PASS/FAIL/理由付きN/A・
  証拠・候補SHA・diff照合）必須 / L1-8 訂正は差し替え記録で（黙った編集禁止） /
  L1-9 Epic・アーキ・要件は実装前に異種レビュー（単発Issueには課さない） /
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
FP: 検証不能なら直列（書き込み・merge も停止側に倒す）。fail-open は「通過」を意味しない。Epic チェックポイント表が不在・未承認なら人間へエスカレーション（FP-9）。（詳細: 正本 docs/05）
```

## Repo-side preparation

For a new repo (or one applying this protocol for the first time):

1. Create a "Parallel Safety Map" section in `ARCHITECTURE.md` ([template](../templates/architecture-parallel-map.md))
2. Place the Issue template ([templates/issue-template.md](../templates/issue-template.md)) under `.github/ISSUE_TEMPLATE/` (optional but recommended)
3. Have everyone stick to avoiding direct pushes to main (enable branch protection where possible)

## Role assignment is up to each agent

Which model or tool is assigned to implementation / review / verification is left to each agent's own toolchain (e.g., a three-role setup with different models like implementer=Codex / reviewer=GLM / verifier=Claude). **What must be upheld is the protocol (three layers + cross-review + fail-posture), not the specific tooling.**
