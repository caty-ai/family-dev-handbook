> **Machine translation.** The Japanese original ([04-adoption.md](../../../docs/04-adoption.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# Setup — Integrating into Each Agent Environment

## Principles

- **This repository is the source of truth.** Each agent places a **summary** in its own "always-loaded context" location and refers to this repo for details
- If a summary and this repo disagree, **this repo wins**. Update the summary to match
- Place it in a "config file that's always loaded" so it keeps working across model changes (don't rely on any specific model's memory or attentiveness)

## Discipline for the summary block

- **This page (docs/04) is the single owner of the version-stamped compact summary.** Downstream copies (each CLAUDE.md / AGENTS.md / system prompt) are owner-applies — the coordinating agent proposes it, and each runtime's owner pastes it in themselves
- Downstream local summaries and overrides **may be stricter than the source of truth, never looser** (tighten only). The cross-agent norm owner for this principle is family-os's operations-policy (config trust section — see the "Caty AI Family" section of the [README](../../../README.md)). This page is that collaboration protocol's application. When adopting this without sister projects, just apply the tighten-only principle as-is
- Summaries reference material by **rule ID + a one-line posture**, not by copying the body text. The ID definitions live in docs/01–03, 05–10; the comment format's field schema lives in templates/issue-template.md, templates/epic-template.md, templates/brief-template.md

## Where to integrate, by agent

Each runtime has a different "config file that's always loaded." Keep an adoption ledger in this shape:

| Agent | Always-loaded context | Status |
|---|---|---|
| `<agent-a>` (e.g. Claude Code family) | User-global config such as `~/.claude/CLAUDE.md` (sections marked permanent) | e.g. ✅ Adopted (YYYY-MM-DD) |
| `<agent-b>` (e.g. long-running agent runtime) | Each agent's system prompt / the workspace's `AGENTS.md` | e.g. ✅ Adopted — the rule-ID version is distributed owner-applies |
| `<agent-c>` (e.g. an agent driven by ops notes) | Ops notes / the skill set's reference docs | e.g. ⬜ Not yet adopted — summary block pending distribution |

> Keep the living ledger of actual adoption under each team's own control. As more integration points appear, maintain this table in your own repository (using Issue comments as the ledger also works).

## Summary block for distribution (copy-paste)

Paste the following as-is into each agent's always-loaded context:

```markdown
## 並行開発プロトコル要約（handbook-revision: 2026-08-15 / owner: 貼った本人名 / last-verified: 貼った日付）
正本: <このハンドブックの正本リポ URL（fork した場合は fork 先）> — 食い違えば正本が正。
この要約は厳しくしてよいが緩めるのは禁止。ID の本文は正本 docs/01〜03・05〜10、様式は templates/issue-template.md・epic-template.md・brief-template.md。

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
  L1-10 席は相互異種+writer異種・設計/実装者は席に数えない・適格モデル名簿はローカル設定・requested/actual記録・実名カタログ=データ層（handbook外・非規範=法とメンバー設定を上書きできない）・抽選/代打は異系統必須（記録された6フィールド例外のみ可）・名指しパネルの同系統は記録つきcorrelated-seatsのみ適法（レビュー記録に明記・無明記=席数未達） /
  L1-11 席数 S/M=異種3（発効はメンバー（家）ごと・発効データ=正本リポの pinned Issue 3フィールド・発効前は旧床2で適法・**Issue無し/フィールド欠落=発効前を主張できず床3**）・L/H=異種3・高リスク領域=5（サイズより優先）・Epic上流=実装着手前L/H・確保不能はオーナー承認の降格 or SEAT-WAIT（対象はレーンのみ・家への無期限適用禁止）
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
R 却下ルーブリック: R-1 自動却下は3理由のみ（main 済を行で指す/バグ再現不能の記録付き/照会後も内容不存在）・証拠必須・
  価値判断の却下はオーナー専決・迷ったら閉じない / R-2 歓迎6箇条（クラス全体修正・端は拡張腰は保守・宣言リファクタ歓迎=宣言と照合は緩まない等） /
  R-3 良品でも断る7箇条（執行は常にオーナー専決） / R-4 前提検証4パターン+「行を指させないなら前提未検証」 /
  R-5 置き場所はしご6段・最小の段・新リポはオーナー承認・同種3つで共通受け口 / R-6 方針は check で強制・2回破られたら起票・ゲートは fail-closed
T テスト&CI基準: T-1 コードを含む新規リポは作成時にテストランナー+CI（test を gate・型検査ある言語は typecheck も）整備・
  テスト0本でも枠を先に張る・既存リポは次にコードを触るレーンで同時整備（opportunistic・棚卸しレーンは立てない）・非コードリポは理由付き N/A /
  T-2 サイズ M/L/H（Epic 子は子の重さ）のバグ修正 PR は再現テスト（fix 前赤・fix 後緑）同梱が既定・S は免除・
  同梱不能の理由は3類型（環境依存/外部サービス依存/再現コスト過大=オーナー承認）・類型外はオーナー専決を PR に1行記録 /
  T-3 コード変更を含む委譲ブリーフの実装チェックに「追加・変更したテストと実行結果」を標準項目化・追加なしは閉じた列挙（T-3）の理由つき報告 /
  T-4 CI 赤のまま merge 禁止・例外は既知無関係の赤のみ（base 再現+赤の identity+LC-1 期限つき Issue 参照+実在検証できるオーナー専決の4条件すべて必須）・
  flaky は含めない・CI 不在は green ではない・N/A は CI が当該変更を検査しない場合のみ・参照無き赤・検証できない例外は例外にならない
FP: 検証不能なら直列（書き込み・merge も停止側に倒す）。fail-open は「通過」を意味しない。Epic チェックポイント表が不在・未承認なら人間へエスカレーション（FP-9）。（詳細: 正本 docs/05）
```

## Repository-side preparation

For a new repo (or one applying this protocol for the first time):

1. Add a "parallel-safety map" section to `ARCHITECTURE.md` ([template](../templates/architecture-parallel-map.md))
2. Place the Issue template ([templates/issue-template.md](../templates/issue-template.md)) under `.github/ISSUE_TEMPLATE/` (optional, but recommended)
3. Have everyone honor a no-direct-push-to-main policy (enable branch protection where possible)
4. Set up a test runner + CI workflow and register it as a required status check ([T-1](10-test-ci-baseline.md); the template type lives at [templates/ci/](../../../templates/ci/README.md). A non-code repo records a one-line justified N/A on its Issue)

## Role assignment is up to each agent

Which model/tool handles implementation / review / verification is left to each agent's toolchain (e.g. a three-role setup with different models: implementer=Codex / reviewer=GLM / verifier=Claude). **What must be honored is the protocol (three layers + cross-review + fail-posture) — not the specific tooling.**
