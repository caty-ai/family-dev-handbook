> **机器翻译。**日文原文（[04-adoption.md](../../../docs/04-adoption.md)）是正本 — 本页与原文不一致时，以日文为准。

# 导入方法 — 集成到各 Agent 环境

## 原则

- **正本是本仓库**。各 Agent 在自己"常驻上下文"的位置放置**摘要**，详情参照本仓库
- 摘要与本仓库出现冲突时，**以本仓库为准**。摘要一侧应跟随更新
- 为了在模型更换后依然生效，放在"始终加载的配置文件"中（不依赖特定模型的记忆或体贴）

## 摘要块的规范

- **带版本刻印的紧凑摘要，唯一 owner 是本页面（docs/04）**。下游副本（各 CLAUDE.md / AGENTS.md / system prompt）是 owner-applies —— 由干事 Agent 提出建议，各运行时的 owner 自行贴入
- 下游本地摘要的覆盖，**允许比正本更严格，禁止比正本更宽松**（tighten only）。该原则的跨 Agent 通用规范 owner 是 family-os 的 operations-policy（config trust 节 —— 参见 [README](../../../README.zh.md) 的"Caty AI ファミリー"节）。本页面是该协作协议的应用。若在没有 sister projects 的情况下导入，直接套用 tighten-only 原则即可
- 摘要不誊写正文，而是以 **rule ID + 一行姿态**来引用。ID 的定义正文在 docs/01〜03・05〜11，注释样式的字段模式在 templates/issue-template.md・templates/epic-template.md・templates/brief-template.md

## 各 Agent 的集成位置

不同运行时"始终加载的配置文件"各不相同。以如下形式维护导入台账：

| Agent | 常驻上下文 | 状态 |
|---|---|---|
| `<agent-a>`（例: Claude Code 系） | `~/.claude/CLAUDE.md` 等用户全局配置（permanent 处理的章节） | 例: ✅ 已导入（YYYY-MM-DD） |
| `<agent-b>`（例: 常驻 agent 运行时） | 各 Agent 的 system prompt / 工作区的 `AGENTS.md` | 例: ✅ 已导入 —— rule-ID 版通过 owner-applies 分发 |
| `<agent-c>`（例: 运维笔记驱动的 agent） | 运维笔记 / 技能组的参考文档 | 例: ⬜ 未导入 —— 待分发摘要块 |

> 实际导入的活台账由各团队自行管理。导入对象增多时，请在自己的仓库中维护此表（用 Issue 评论作台账也可以）。

## 分发用摘要块（可直接复制粘贴）

将以下内容原样贴入各 Agent 的常驻上下文：

```markdown
## 並行開発プロトコル要約（handbook-revision: 2026-08-21 (v0.18.0) / owner: 貼った本人名 / last-verified: 貼った日付）
正本: <このハンドブックの正本リポ URL（fork した場合は fork 先）> — 食い違えば正本が正。
この要約は厳しくしてよいが緩めるのは禁止。ID の本文は正本 docs/01〜03・05〜11、様式は templates/issue-template.md・epic-template.md・brief-template.md。

L2 並行可否: L2-1 ゴール合意・重さ判定（迷えば重い側）・設計を難しくする要件は一度疑う（消す決定は依頼者） / L2-2 境界変更は境界PR1本先行 /
  L2-3 Issue に触るファイル予測必須 / L2-4 並行GO=宣言ファイル集合が非交差のみ /
  L2-5 広域Issueは単独実行 / L2-6 ホットスポットは並行安全マップ+分割投資
L1 Issue完遂: L1-1 Issue-first / L1-2 Why・Done when・触るファイル予測 /
  L1-3 merge レビュー=別モデル or 別エージェント・self-approve 禁止・後続ラウンドの新規 blocking は実証済み欠陥 or 未充足ゲート基準のみ（non-blocking は自由） /
  L1-4 レーン状態は WIP/HOLD/MERGED/SUPERSEDED/ABANDONED の5語彙・不明状態=非アクティブ扱い・
  MERGED は release 履行報告必須（vX.Y.Z 宣言レーンは tag URL 無き MERGED は終端未成立） /
  L1-5 HOLD は owner/reason/review-by/lock disposition/残作業or後継 必須 /
  L1-6 リトライ有限・尽きたら証拠付き HOLD/ABANDONED / L1-7 merge は完了記録（Done when→PASS/FAIL/理由付きN/A・
  証拠・候補SHA・diff照合・CI 状態・release 欄+直前の出荷相当 merge の履行確認）必須 / L1-8 訂正は差し替え記録で（黙った編集禁止） /
  L1-9 サイズ L/H/Epic（=L2-1 の重い側・アーキ・要件含む）は実装着手前に異種レビュー（S/M 単発Issueには課さない） /
  L1-10 席は相互異種+writer異種・設計/実装者は席に数えない・適格モデル名簿はローカル設定・requested/actual記録・実名カタログ=データ層（handbook外・非規範=法とメンバー設定を上書きできない）・抽選/代打は異系統必須（記録された6フィールド例外のみ可）・名指しパネルの同系統は記録つきcorrelated-seatsのみ適法（レビュー記録に明記・無明記=席数未達） /
  L1-11 席数 S/M=異種3（発効はメンバー（家）ごと・発効データ=正本リポの pinned Issue 3フィールド・発効前は旧床2で適法・**Issue無し/フィールド欠落=発効前を主張できず床3**）・L/H=異種3・高リスク領域=5（サイズより優先）・Epic上流=実装着手前L/H・確保不能はオーナー承認の降格 or SEAT-WAIT（対象はレーンのみ・家への無期限適用禁止）
L0 git: L0-1 被り確認+WIP 4フィールド（agent/date/Files to touch/Branch）=ソフトロック /
  L0-2 宣言外は触らない・UNKNOWN=直列 / L0-3 stale=72h・引き取りは TAKEOVER+再開チェック+新WIP宣言 /
  L0-4 1セッション=1Issue=1branch=1worktree / L0-5 main マージ専用 /
  L0-6 PR にファイル一覧+diff照合 / L0-7 マージ1本ずつ・git 自動化は identity/config env 明示・ユーザー git 状態 不読不書 / L0-8 ブランチ短命・HOLD 明示 /
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
  R-3 良品でも断る7箇条（執行は常にオーナー専決） / R-4 前提検証4パターン+「行を指させないなら前提未検証」・path:line か実行ログを引用できない指摘は blocking 不可 /
  R-5 置き場所はしご6段・最小の段・新リポはオーナー承認・同種3つで共通受け口 / R-6 方針は check で強制・2回破られたら起票・ゲートは fail-closed
T テスト&CI基準: T-1 コードを含む新規リポは作成時にテストランナー+CI（test を gate・型検査ある言語は typecheck も）整備・
  テスト0本でも枠を先に張る・既存リポは次にコードを触るレーンで同時整備（opportunistic・棚卸しレーンは立てない）・非コードリポは理由付き N/A /
  T-2 サイズ M/L/H（Epic 子は子の重さ）のバグ修正 PR は再現テスト（fix 前赤・fix 後緑）同梱が既定・S は免除・
  同梱不能の理由は3類型（環境依存/外部サービス依存/再現コスト過大=オーナー承認）・類型外はオーナー専決を PR に1行記録 /
  T-3 コード変更を含む委譲ブリーフの実装チェックに「追加・変更したテストと実行結果」を標準項目化・追加なしは閉じた列挙（T-3）の理由つき報告 /
  T-4 CI 赤のまま merge 禁止・例外は既知無関係の赤のみ（base 再現+赤の identity+LC-1 期限つき Issue 参照+実在検証できるオーナー専決の4条件すべて必須）・
  flaky は含めない・CI 不在は green ではない・N/A は CI が当該変更を検査しない場合のみ・参照無き赤・検証できない例外は例外にならない /
  T-5 全完了記録に release 欄必須（vX.Y.Z / deferred / N/A の3語彙）・出荷相当（利用者の挙動・公開API・配布物・規範が変わる）は N/A 不可・迷ったら出荷相当・
  欄なし/空欄/未編集プレースホルダ/語彙外=blocking・vX.Y.Z はタグを切り URL を載せ Release を実在させた MERGED まで終端不成立
  （未履行レーンは終端せず WIP のまま stale 時計に乗る・非アクティブ扱いが掛かるのは tag URL または Release 実在を欠く MERGED=不正形式の方）・
  deferred は退場トリガー付き Issue 参照必須（失効=「切らない特権」を失い次の出荷相当は vX.Y.Z 必須・失効自体は記録を止めない）・
  N/A は閉じた4類型（規範なし docs のみ/挙動・API・配布物不変の内部整理/CI・開発配線のみ/main 未到達の Epic 子→epic）+類型外はオーナー専決・
  全完了記録に previous release 欄（直前の出荷相当 merge の値+履行状態）・未履行の vX.Y.Z は blocking・deferred 連続は出荷相当列で数え vX.Y.Z でリセット・2連続の次は deferred 不可・
  タグは当該 merge が main に残したコミットへ annotated+SemVer（原則は宣言と同名・レビュー後にスコープが動いた時のみ別名可+MERGED に差異と理由1行）・
  リリースノートに証拠ポインタ1つ以上・署名検証リポは署名タグ必須（鍵 per-repo）他は SHOULD・
  Epic 子→epic は対象外（N/A・T-5 は epic→main に掛かる）・全リポ一律（出荷相当が無ければ自然に N/A）
  T-6 家族製ランナーは PASS/FAIL/SKIP と動的3値サマリ（declared/executed/skipped・declared=executed+skipped）+閉じた exit code・必須依存欠落は missing-dep 付き127・異常終了でもサマリ必須・
  SKIP率20%超は赤（変更値はCI caller入力を正本+記録）・整備済みは require_suite_reconciliation: true のCI照合が有効になった時点 /
  T-7 公開READMEはT-1 test workflowのliveバッジか灰のCI: not yetを必須表示・静的色はlightgrey/blueのみ・実測数字はrun URL+実測日必須・Project status標準形は条文内蔵
PB 公開準備: PB-1 リポ公開は正本チェックリストの項目別PASS/FAIL/理由付きN/A+証拠でゲート・検証不能は未通過（fail-closed） /
  PB-2 正本は templates/publication-checklist.md・原則リリースタグ、未包含時だけcommit SHA+後続タグ追記 /
  PB-3 (a)=run URL・(b)=名指し手動手順+記録・(c)=オーナー発行3形のみ、自己申告禁止 /
  PB-4 完了記録は1レーン1つをレーンIssueへ置くL1-7特則・PRはポインタ1行・run URL実在+head SHA一致 /
  PB-5 第1・第2消費者のギャップを#100へ還流して失効する時限パイロット条項
FP: 検証不能なら直列（書き込み・merge も停止側に倒す）。fail-open は「通過」を意味しない。Epic チェックポイント表が不在・未承認なら人間へエスカレーション（FP-9）。（詳細: 正本 docs/05）
```

## 仓库侧的准备工作

对于新仓库（或首次应用本协议的仓库）：

1. 在 `ARCHITECTURE.md` 中新建"并行安全地图"章节（[模板](../templates/architecture-parallel-map.md)）
2. 将 Issue 模板（[templates/issue-template.md](../templates/issue-template.md)）放入 `.github/ISSUE_TEMPLATE/`（可选但推荐）
3. 全员遵守避免直接 push main 的运作方式（能设置 branch protection 的话就设置）
4. 整备测试运行器 + CI workflow，并注册到 required status checks（[T-1](10-test-ci-baseline.md)；类型见 [templates/ci/](../../../templates/ci/README.md)。非代码仓库在 Issue 中记录一行理由付 N/A）
5. 公开仓库时，以公开检查清单（[PB-1](11-publication.md)、[templates/publication-checklist.md](../templates/publication-checklist.md)）作为 lane 的门禁

## 角色分工由各 Agent 自行决定

实现 / 评审 / 验证具体分配给哪个模型或工具，交由各 Agent 的工具链自行决定（例如 implementer=Codex / reviewer=GLM / verifier=Claude 这样的不同模型三角色构成）。**需要遵守的是协议本身（3层结构 + 交叉评审 + fail-posture），而不是具体使用的工具。**
