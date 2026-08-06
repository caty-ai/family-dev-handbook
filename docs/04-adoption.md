# 導入方法 — 各エージェント環境への組み込み

## 原則

- **正本はこのリポジトリ**。各エージェントは自分の「常時コンテキストに載る場所」に**要約**を置き、詳細はこのリポを参照する
- 要約とこのリポが食い違ったら、**このリポが正**。要約側を追従させる
- モデルが変わっても効くように、「常時読み込まれる設定ファイル」に置く（特定モデルの記憶や気配りに依存させない）

## 要約ブロックの規律

- **バージョン刻印付きのコンパクト要約のオーナーは本ページ（docs/04）ただ1つ**。下流コピー（各 CLAUDE.md / AGENTS.md / system prompt）は owner-applies — 幹事エージェントが提案し、各ランタイムのオーナーが自分で貼る
- 下流のローカル要約・上書きは、正本より**厳しくするのは可・緩めるのは禁止**（tighten only）。この原則のエージェント横断規範オーナーは family-os の operations-policy（config trust 節 — [README](../README.ja.md) の「Caty AI ファミリー」節参照）。本ページはその協働プロトコルへの適用。sister projects なしで導入する場合は tighten-only 原則をそのまま適用すればよい
- 要約は本文を書き写さず **rule ID + 1行ポスチャ**で参照する。ID の定義本文は docs/01〜03・05〜07、コメント様式のフィールドスキーマは templates/issue-template.md・templates/epic-template.md・templates/brief-template.md

## エージェント別の組み込み先

ランタイムごとに「常時読み込まれる設定ファイル」が違う。導入台帳をこの形で持つ:

| エージェント | 常時コンテキスト | 状態 |
|---|---|---|
| `<agent-a>`（例: Claude Code 系） | `~/.claude/CLAUDE.md` 等のユーザーグローバル設定（permanent 扱いのセクション） | 例: ✅ 導入済み（YYYY-MM-DD） |
| `<agent-b>`（例: 常駐 agent ランタイム） | 各エージェントの system prompt / ワークスペースの `AGENTS.md` | 例: ✅ 導入済み — rule-ID 版は owner-applies で配布 |
| `<agent-c>`（例: 運用ノート駆動の agent） | 運用ノート / スキル群の参照ドキュメント | 例: ⬜ 未導入 — 要約ブロックを配布 |

> 実導入の生きた台帳は各チームの管理下に置く。導入先が増えたら、この表を自分のリポジトリで維持する（Issue のコメントを台帳にする運用でもよい）。

## 配布用の要約ブロック（コピペ用）

各エージェントの常時コンテキストに、以下をそのまま貼る:

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

## リポジトリ側の準備

新しいリポ（または初めてこのプロトコルを適用するリポ）では:

1. `ARCHITECTURE.md` に「並行安全マップ」セクションを作る（[テンプレ](../templates/architecture-parallel-map.md)）
2. Issue テンプレート（[templates/issue-template.md](../templates/issue-template.md)）を `.github/ISSUE_TEMPLATE/` に置く（任意だが推奨）
3. main の直接 push を避ける運用を全員で守る（branch protection が張れる場合は張る）

## 役割分担はエージェントごとに自由

実装 / レビュー / 検証をどのモデル・ツールに割り当てるかは各エージェントのツールチェーンに任せる（例: implementer=Codex / reviewer=GLM / verifier=Claude のような別モデル3役構成）。**守るべきはプロトコル（3層 + クロスレビュー + fail-posture）であって、道具立てではない。**
