> **机器翻译。**日文原文（[04-adoption.md](../../../docs/04-adoption.md)）是正本 — 本页与原文不一致时，以日文为准。

# 接入方法 — 集成到各 Agent 环境

## 原则

- **正本是这个仓库**。每个 Agent 在自己"始终加载的上下文位置"放置**摘要**，详细内容参照本仓库
- 摘要与本仓库不一致时，**以本仓库为准**。摘要一侧需要跟进修改
- 为了在模型变化后依然有效，要放在"始终会被加载的配置文件"里（不要依赖特定模型的记忆或体贴）

## 摘要块的规范

- **带版本刻印的精简摘要，唯一的 owner 是本页面（docs/04）**。下游副本（各个 CLAUDE.md / AGENTS.md / system prompt）是 owner-applies——由干事 Agent 提出建议，各运行时的 owner 自行贴上
- 下游本地摘要、覆盖内容，相对正本**只能收紧、不能放松**（tighten only）。这一原则的跨 Agent 通用规范 owner 是 family-os 的 operations-policy（config trust 节 —— 参见 [README](../../../README.zh.md) 的「Caty AI 家族」节）。本页面是该协作协议的应用。若在没有 sister projects 的情况下引入本协议，直接套用 tighten-only 原则即可
- 摘要不誊抄正文，而是用 **rule ID + 一行 posture** 来引用。ID 的定义正文在 docs/01〜03、05〜07，注释样式的字段 schema 在 templates/issue-template.md、templates/epic-template.md、templates/brief-template.md

## 各 Agent 的接入位置

不同运行时的"始终加载的配置文件"各不相同。用这种形式维护接入台账：

| Agent | 始终上下文 | 状态 |
|---|---|---|
| `<agent-a>`（例: Claude Code 系） | `~/.claude/CLAUDE.md` 等用户全局配置（视为 permanent 的部分） | 例: ✅ 已接入（YYYY-MM-DD） |
| `<agent-b>`（例: 常驻 agent 运行时） | 各 Agent 的 system prompt / 工作区的 `AGENTS.md` | 例: ✅ 已接入 — rule-ID 版通过 owner-applies 分发 |
| `<agent-c>`（例: 运维笔记驱动的 agent） | 运维笔记 / 技能组的参照文档 | 例: ⬜ 未接入 — 待分发摘要块 |

> 实际接入情况的活台账由各团队自行管理。接入对象增多后，请在自己的仓库中维护此表（也可以用 Issue 评论作为台账）。

## 供分发使用的摘要块（可直接复制粘贴）

将以下内容原样贴到各 Agent 的始终上下文中：

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

## 仓库侧的准备工作

对于新仓库（或首次应用本协议的仓库）：

1. 在 `ARCHITECTURE.md` 中创建"并行安全地图"章节（[模板](../templates/architecture-parallel-map.md)）
2. 将 Issue 模板（[templates/issue-template.md](../templates/issue-template.md)）放到 `.github/ISSUE_TEMPLATE/`（可选，但建议这样做）
3. 全员共同遵守避免直接 push main 的运作方式（能设置 branch protection 的话就设置）

## 角色分工由各 Agent 自行决定

实现 / 审查 / 验证分别交给哪个模型・工具，由各 Agent 的工具链自行决定（例如: implementer=Codex / reviewer=GLM / verifier=Claude 这样的不同模型三角色配置）。**需要坚守的是协议本身（三层 + 交叉审查 + fail-posture），而不是具体工具。**
