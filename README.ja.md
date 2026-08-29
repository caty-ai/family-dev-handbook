# Family Dev Handbook

<div align="center">

[🇺🇸 English](README.md) ｜ **🇯🇵 日本語（正本）** ｜ [🇨🇳 简体中文](README.zh.md) ｜ [🇹🇭 ไทย](README.th.md)

![Family Dev Handbook — 5本のレーンがゲートを通って1本に合流する](assets/readme/hero.png)

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![version](https://img.shields.io/badge/version-v0.18.0-blue)
![type](https://img.shields.io/badge/type-docs%2Btemplates-blue)
![docs](https://img.shields.io/badge/docs-Japanese%20canonical-lightgrey)
![status](https://img.shields.io/badge/status-active-lightgrey)
[![Test + Lint](https://github.com/caty-ai/family-dev-handbook/actions/workflows/test-lint.yml/badge.svg)](https://github.com/caty-ai/family-dev-handbook/actions/workflows/test-lint.yml)

複数の AI エージェントと複数のセッションが、同じコードベースを衝突せずに並行開発するための共通ルールです。<br>
同じファイルを同時に直して壊す・「できました」が信用できない・引き継いだ時に何が終わっているか分からない、を解決します。<br>
判断を人の注意力から、着手前の機械的な判定と、証拠つきのゲートへ移すことで解決します。

**検証できないなら、直列。**

🔧 [ルール本文 — L0 git 規律](docs/03-git-protocol.md) ｜ 📘 [様式の正本 — Issue テンプレート](templates/issue-template.md)

</div>
<!-- repo-state:begin (generated; do not edit) -->
<p align="center"><sub>generation: <code>3fe2b7d</code> (2026-08-29T18:27:16Z) · verify: <a href="https://api.github.com/repos/caty-ai/family-dev-handbook/commits/main">API HEAD</a> · <a href="./status.json">status.json</a></sub></p>
<!-- repo-state:end -->

---

<a id="toc"></a>

## 目次

- [こんな経験はありませんか？](#problems)
- [前提](#premises)
- [できること](#what-you-get)
- [使うのに必要なもの](#requirements)
- [使いはじめる](#get-started)
- [安心して使える理由](#safety)
- [並行してよいかの決め方](#parallel-go)
- [ルールの全体像](#rules)
- [もっと詳しく](#docs)
- [Caty AI ファミリー](#ecosystem)
- [開発ステータス](#status)
- [コントリビュート](#contributing)
- [謝辞](#acknowledgements)
- [ライセンス](#license)

---

<a id="problems"></a>

## こんな経験はありませんか？

AI エージェントに任せる仕事が増えると、コードそのものより先に、こういうことが起き始めます。

- **同じファイルを2人（2体）が同時に直していた** — 気づくのは merge の時
- **「できました」が信用できない** — 何をどこまで確かめたのかが残っていない
- **引き継いだ瞬間、何が終わっているか分からない** — 前のセッションの記憶はもうない
- **並行してよいのか毎回悩む** — 判断が人によって違い、事故のたびにルールだけが増える

この4つを、注意力ではなく仕組みで潰すために作られたのがこのハンドブックです。

その前に、このハンドブックが何を出発点にしているかを先にお伝えします。

---

<a id="premises"></a>

## 前提

読み始める前に共有しておきたい出発点が3つあります。以降の説明は、この3つを出発点にしています。3つは順序ではなく、どれから入っても同じ土俵に立つための前提です。

### Issue から始める

**コードを触る前に、GitHub の Issue を1本立てる**ところから始めます（Issue-first）。

会話やチャットで決めたことは、セッションが終われば消えます。AI エージェントは毎回記憶ゼロで始まるので、なおさらです。残るのは Issue の本文と Pull Request の差分だけで、だからこそその2つを引き継ぎの唯一の正本にします。誰が忘れっぽいかという話ではなく、**忘れることを前提にした置き場所を1つ決めておく**、という話です。

詳しくは [Issue-first とは](docs/why-issue-first.md) へ。

### モジュールは小さく切る

**並行できるかどうかは、着手する前にコードの形で決まっています。**

多くの責務が同居した巨大なファイルが1つあると、そのエリアでは何をやっても触るファイルが交差するので、いつも直列になります。だから分割は「あとで、きれいにするためにやる整理」ではなく、**先にやる投資**として扱います。返ってくるものは3つです。

- **並行できる** — 分割した瞬間から、そのエリアの並行が構造的に安全になる
- **集中できる** — 読む量が減るほど、エージェントは目の前の仕事だけに向かえる
- **差し替えられる** — ブロックのつけ外しのように、壊れた1つだけを直せる

これを自分で設計する必要はありません。**このハンドブックをエージェントに渡しておけば、分割すべき場所は向こうから Issue として上がってきます。**

詳しくは [なぜモジュールを小さく切るのか](docs/why-small-modules.md) へ。

### 複雑さは要件で消す

**設計でハマったら、より賢い設計ではなく、まず要件を疑います。**

難しさの多くは設計ではなく要件が連れてきます。前提を1つ消せると、設計の難所が実装ごと・保守ごと、まるごと消えます。ただし疑うのはエージェントの自由、**消す決定は依頼した人のもの**です。受け入れた複雑さは理由を Issue に1行残します。

詳しくは [なぜシンプルに作るのか](docs/why-simple-systems.md) へ。

---

<a id="what-you-get"></a>

## できること

問題を3つの層に分け、それぞれ別の方法で潰します。上の層ほど「事故を予防する」、下の層ほど「事故を検出して封じ込める」役割です。さらに v0.10.0 からは、3層の下に **T（テスト & CI 基準）** が土台として加わり、「作業の進め方」だけでなく「成果物の正しさの証明」も契約になりました。

図に出てくる言葉を先に3つだけ。**レーン**＝1本の Issue に対応する作業の流れ。**WIP**＝ work in progress（作業中）の宣言。**ソフトロック**＝宣言している間だけ他の人がそこを触らない、という約束です。

```mermaid
flowchart TB
    subgraph L2["L2 — 並行してよいかを決める"]
        A1["ゴール合意・重さ判定"] --> A2{"モジュール境界を動かすか"}
        A2 -->|動かす| A3["境界PRを1本だけ先に通す"]
        A2 -->|動かさない| A4["Issue に触るファイルを予測して書く"]
        A3 --> A4
        A4 --> A5["交差しない Issue だけ並行GO"]
    end
    subgraph L1["L1 — 1つの作業を完遂する"]
        B1["Issue 起票<br/>Why / Done when / 触るファイル予測"] --> B2["実装<br/>レーン状態は5語彙で宣言"] --> B3["自分以外がレビュー"] --> B4["完了記録つき PR → merge"]
    end
    subgraph L0["L0 — git で物理衝突を防ぐ"]
        C1["worktree で分離"] --> C2["WIP 4フィールド宣言<br/>= ソフトロック（72時間で失効）"] --> C3["main はマージ専用<br/>1本ずつ rebase → 再検証"]
    end
    subgraph T["T — 正しさの証明を蓄積する"]
        D1["リポ作成時に<br/>テスト + CI の枠を張る"] --> D2["バグ修正は<br/>再現テストを同梱"] --> D3["CI 赤のまま merge しない<br/>例外は検証つきのみ"]
    end
    L2 --> L1 --> L0 --> T
```

- 🚦 **並行してよいかを、着手前に決める**

  「2つの作業が触るファイルの集合は交差しない」と着手前に分かる時だけ、並行を許します。判断は3つの問いで決まり、どれか1つでも確かめられなければ自動的に直列へ倒れます。

- 📋 **1つの作業を、証拠つきで終わらせる**

  Issue には Why・Done when・触るファイルの予測を必ず書きます。merge には完了記録（Done when の全項目に PASS / FAIL / 理由付き N/A・候補となるコミット・宣言と実際の差分の照合・自分以外によるレビュー）を要求します。「できました」が言葉ではなく記録になります。

- 🔒 **物理的な衝突を、git の使い方で封じ込める**

  1セッション＝1 Issue＝1ブランチ＝1 worktree（同じリポジトリを複数の作業フォルダに分ける git の機能）。main はマージ専用。作業中のレーンは4つの項目を宣言している間だけソフトロックとして扱われ、72時間で自然に失効します。

- 🧪 **成果物の正しさを、テストと CI に蓄積する**

  コードを含むリポジトリは作成時から CI の枠を持ち、バグ修正は当該バグの再現テスト（fix 前に赤・fix 後に緑）を連れて merge されます。CI が赤のままの merge は禁止で、通れるのは検証条件を全部満たした既知・無関係の赤だけです。「動いているはず」ではなく、証明が増えていきます。

効くかどうかの前に、そもそも何が必要か。答えは「ほとんど何も要りません」です。

---

<a id="requirements"></a>

## 使うのに必要なもの

このリポジトリの条文はドキュメントだけでできています。このリポジトリ自体にインストールするプログラムはありません（[templates/ci/](templates/ci/README.md) に、各リポへ配布して使う型 — YAML とスクリプト — を含みます）。

| 必要なもの | 対応 |
|---|---|
| 実行するランタイム（Node / Python など） | 不要（条文は docs のみ。templates/ci に配布用の型（YAML+スクリプト）を含む） |
| バージョン管理 | ✅ git |
| 作業の記録場所 | ✅ GitHub の Issue / Pull Request |
| AI エージェント | ✅ 常時読み込まれる設定ファイル（`CLAUDE.md` / `AGENTS.md` / システムプロンプトなど）を持つものなら種類を問わない |
| 人間だけの運用 | ✅ 可（AI を使わないチームでもそのまま使える） |

特定のエージェント製品・特定の記憶基盤・特定のツールチェーンには依存しません。守る対象はプロトコルであって、道具立てではないためです。組み込み先の一覧をどう管理するかは [docs/04](docs/04-adoption.md) にあります。

揃っていれば、導入は「貼る」だけです。

---

<a id="get-started"></a>

## 使いはじめる

導入とは、各エージェントの常時コンテキストにルールの要約を置くことです。

### AI に入れてもらう

普段使っているエージェントに、次のように頼みます。

```text
https://github.com/caty-ai/family-dev-handbook の docs/04-adoption.md にある
「配布用の要約ブロック」を、私の常時コンテキスト（CLAUDE.md / AGENTS.md）に貼ってください。
その設定ファイルがまだ無ければ作ってください。
1行目の owner は私の名前、last-verified は今日の日付に書き換えてください。
2行目の「正本:」には、このハンドブックのリポジトリ URL を入れてください。
handbook-revision の値は書き換えないでください。
```

### 自分で入れる

1. [docs/04](docs/04-adoption.md) の「配布用の要約ブロック」を開く（50行ほどのテキストです）
2. 常時読み込まれる設定ファイルに、丸ごと貼る
3. 1行目の `owner` と `last-verified` を自分と今日の日付に書き換える。`handbook-revision` はそのまま残す
4. 2行目の `正本:` を、このハンドブックのリポジトリ URL（fork したなら fork 先）に書き換える

貼るのはこれだけです。中身は10系統の rule ID（`L2-1`〜`L2-6` / `L1-1`〜`L1-11` / `L0-1`〜`L0-9` / `FP-1`〜`FP-9` / `E-1`〜`E-10` / `B-1`〜`B-5` / `LC-1`〜`LC-5` / `R-1`〜`R-6` / `T-1`〜`T-7` / `PB-1`〜`PB-5`）と、それぞれ1行の方針（ポスチャ）だけで、条文の本文は入っていません。**本文の正本はこのリポジトリで、要約と食い違ったら正本が正です。** 自分のリポジトリに合わせて厳しくするのは自由ですが、緩めるのは禁止しています。

やめたくなったら、貼った50行ほどを消すだけで元に戻ります。ほかのファイルには触りません。

リポジトリ側の準備（並行安全マップ・Issue テンプレート・main の保護・テストランナー + CI）は [docs/04](docs/04-adoption.md) にあります。

貼る前に引っかかる点があるはずです。先に答えておきます。

---

<a id="safety"></a>

## 安心して使える理由

- **全部を一度に入れなくてよい** — L0（git 規律）だけでも効きます。L2 と L1 は運用が回りはじめてから足せます
- **今の Issue / PR 運用を作り替えなくてよい** — 足すのは Issue 本文の3項目と、レーンの状態を表す5つの言葉（WIP / HOLD / MERGED / SUPERSEDED / ABANDONED）だけです
- **緩める方向の改変だけが禁止** — 自分のリポジトリで厳しくするのは自由です。守るのは「正本より緩い要約を配らない」の一点だけ
- **エージェントが守らない前提で設計されている** — 気配りや記憶に頼らず常時読み込まれる場所に置き、判定は交差するかしないかの2値で、確かめられなければ必ず直列側へ倒れます

**向かない使い方**もあります。

- 1人・1セッションで、常に直列にしか作業しない — L0-4 以外はほとんど空振りします
- Issue / PR を使わない運用 — L1 の完遂ゲートが成立しません
- 単発の bug fix だけを回す小さなリポジトリ — 上流レビュー（実装に入る前に別のモデルへ設計を見せる確認・L1-9）は最初から適用対象外です

運用で毎回いちばん迷うのは「いま並行で始めてよいか」です。その判定だけ、ここで完結させます。

---

<a id="parallel-go"></a>

## 並行してよいかの決め方

3つの問いで決まります。どれか1つでも確かめられなければ、並行しません。

```mermaid
flowchart TD
    S["並行で新しい Issue に着手したい"] --> Q1{"進行中の作業が<br/>WIP 4フィールドを<br/>宣言しているか"}
    Q1 -->|いいえ / 形式が不正| X1["直列<br/>宣言を直してもらう"]
    Q1 -->|はい| Q2{"自分が触るファイルと<br/>交差するか"}
    Q2 -->|交差する / 予測できない| X2["直列で待つ<br/>または境界分離を先に通す"]
    Q2 -->|交差しない| Q3{"どちらかが広域変更か<br/>全面リファクタ・一括整形など"}
    Q3 -->|はい| X3["広域変更は単独実行<br/>同リポの並行は全停止"]
    Q3 -->|いいえ| GO["並行GO<br/>worktree を切って着手"]
```

もし何をやっても毎回交差してしまうなら、それは判定の問題ではなく切り方の問題です（[なぜモジュールを小さく切るのか](docs/why-small-modules.md)）。

この1枚は `L2-4` というたった1条にすぎません。全体の地図はこの先です。

---

<a id="rules"></a>

## ルールの全体像

ルールは10系統に分かれ、すべてに変わらない ID が振ってあります。要約も会話も Issue も、この ID で指し合います。

| 系統 | 決めること | rule ID | 本文 |
|---|---|---|---|
| **L2** マイルストーンループ | 並行してよいか | `L2-1`〜`L2-6` | [docs/01](docs/01-milestone-loop.md) |
| **L1** Issue ループ | 1つの作業をどう完遂するか | `L1-1`〜`L1-11` | [docs/02](docs/02-issue-loop.md) |
| **L0** git 規律 | 物理衝突をどう防ぐか | `L0-1`〜`L0-9` | [docs/03](docs/03-git-protocol.md) |
| **FP** 失敗時姿勢 | 検証できない時どちらへ倒すか | `FP-1`〜`FP-9` | [docs/05](docs/05-fail-posture.md) |
| **E** Epic レーン | 複数 Issue の束をどう運ぶか | `E-1`〜`E-10` | [docs/06](docs/06-epic-lane.md) |
| **B** 委譲ブリーフ | 1回の委譲をどう契約にするか | `B-1`〜`B-5` | [docs/07](docs/07-delegation-brief.md) |
| **LC** ライフサイクル | 置いた物をいつ・どう退場させるか | `LC-1`〜`LC-5` | [docs/08](docs/08-lifecycle.md) |
| **R** 却下ルーブリック | 何を受け入れ・何を断るか | `R-1`〜`R-6` | [docs/09](docs/09-rejection-rubric.md) |
| **T** テスト & CI 基準 | 正しさの証明をどう蓄積するか | `T-1`〜`T-7` | [docs/10](docs/10-test-ci-baseline.md) |
| **PB** 公開準備 | リポ公開を何でゲートするか | `PB-1`〜`PB-5` | [docs/11](docs/11-publication.md) |

とくに効き目を左右する条文が2つあります。ひとつは **FP** の合言葉「検証不能なら直列。fail-open は『通過』を意味しない」— 確かめられない時に通す側へ倒す設計を選んだとしても、それは「確認済み」の意味には決してならない、という宣言です。もうひとつは **高リスク領域の単一定義**で、ここに触れる作業は人間が必ず止まり、レビューの席が増えます（対外公開・課金・不可逆な操作・権限まわりの境界などが該当します。正確な線引きは正本を見てください）。同じ定義を2か所に持たないよう、正本は [docs/06](docs/06-epic-lane.md) の1箇所だけに置いています。

Epic レーン（`E-1`〜`E-10`）は任意です。オーナーが承認して初めて成立し、それまでは通常の Issue 運用のまま使えます。

<details>
<summary>コア契約 P1〜P5（v0.1.0 で導入した5つの背骨）</summary>

このコア契約 P1〜P5 は、PB 層（PB-1〜PB-5・[docs/11](docs/11-publication.md)）とは別物です。

| 契約 | 内容 | rule ID |
|---|---|---|
| **P1 WIPロック** | WIP は `agent / date / Files to touch / Branch` の4フィールドを備える間だけソフトロック。宣言外のファイルは触らない、stale は72時間、引き取りは TAKEOVER 手続 | `L0-1`〜`L0-3` |
| **P2 レーン状態** | 閉じた5状態語彙。WIP は宣言する状態であって既定値ではない。不明・不正な状態は非アクティブ扱いで修復待ち。リトライは有限で、使い切りは成功にならない | `L1-4`〜`L1-6` |
| **P3 再開チェック** | 再開・引き継ぎレーンの最初の書き込み前に、4点（ロック / スコープ / ブランチ / Done when）の確認結果を Issue に投稿する | `L0-9` |
| **P4 失敗時姿勢** | ガード付きの遷移ごとに fail-open / fail-closed を事前宣言する。欠落は常に権限が縮む方向へ。成果物の本文は自己承認しない | `FP-1`〜`FP-9` |
| **P5 完了証拠ゲート** | merge には完了記録が必須。Done when 全項目の PASS / FAIL / 理由付き N/A・証拠・候補 SHA・宣言と diff の照合・別モデルまたは別エージェントのレビュアー | `L1-7`〜`L1-8` |

この5つは以後、凍結して扱っています。

</details>

条文の本文はすべて `docs/` にあります。索引をどうぞ。

---

<a id="docs"></a>

## もっと詳しく

docs と templates の機械翻訳版（English / 简体中文 / ไทย）は [i18n/](i18n/README.md) にあります — 正本は日本語で、食い違えば日本語が正です。

| ファイル | 内容 |
|---|---|
| [docs/why-issue-first.md](docs/why-issue-first.md) | Issue-first とは — 前提の解説（**条文ではありません**。会話でなく Issue から始める理由・Issue に何を書くか・要らない場合） |
| [docs/why-small-modules.md](docs/why-small-modules.md) | なぜモジュールを小さく切るのか — 前提の解説（**条文ではありません**。分割が並行可能性への投資である理由・「小さい」の意味・このハンドブック自身の切り方） |
| [docs/why-simple-systems.md](docs/why-simple-systems.md) | なぜシンプルに作るのか — 前提の解説（**条文ではありません**。複雑さを設計でなく要件で消す理由・疑うときの質問・「疑うのは自由、消す決定は依頼者のもの」） |
| [docs/01-milestone-loop.md](docs/01-milestone-loop.md) | L2 マイルストーンループ — 並行の可否を決める層（`L2-1`〜`L2-6`） |
| [docs/02-issue-loop.md](docs/02-issue-loop.md) | L1 Issue ループ — 完遂・レーン状態・完了証拠ゲート・上流異種レビュー（`L1-1`〜`L1-11`） |
| [docs/03-git-protocol.md](docs/03-git-protocol.md) | L0 git 規律 — WIP ロック・worktree・マージ手順・再開チェック（`L0-1`〜`L0-9`） |
| [docs/04-adoption.md](docs/04-adoption.md) | 導入方法 — 組み込み先・配布用の要約ブロック・要約の規律 |
| [docs/05-fail-posture.md](docs/05-fail-posture.md) | 失敗時姿勢 — 検証できない時にどちらへ倒すか（`FP-1`〜`FP-9`） |
| [docs/06-epic-lane.md](docs/06-epic-lane.md) | Epic レーン — 人間の確認を Epic 単位に束ねる層・高リスク領域の単一定義（`E-1`〜`E-10`） |
| [docs/07-delegation-brief.md](docs/07-delegation-brief.md) | B 委譲ブリーフ — サブエージェントへ仕事を1回渡すときの依頼文の契約（`B-1`〜`B-5`） |
| [docs/08-lifecycle.md](docs/08-lifecycle.md) | LC ワークスペース・ライフサイクル — 置いた物の退場を契約にする層・退場条件の数値はローカル正本（`LC-1`〜`LC-5`） |
| [docs/09-rejection-rubric.md](docs/09-rejection-rubric.md) | R 却下ルーブリック — 何を受け入れ・何を断るかの意図の層。自動却下の3理由・歓迎/却下の判断基準・前提検証・置き場所のはしご・check 昇格（`R-1`〜`R-6`） |
| [docs/10-test-ci-baseline.md](docs/10-test-ci-baseline.md) | T テスト & CI 基準 — 初期整備・回帰テスト既定・ブリーフ接続・fail-closed merge・リリース既定・テスト出力契約・バッジと数字の正直さ。付録に非規範のランナー早見表（`T-1`〜`T-7`） |
| [docs/11-publication.md](docs/11-publication.md) | PB 公開準備 — リポジトリ公開を正本チェックリストでゲートする層（`PB-1`〜`PB-5`） |
| [templates/issue-template.md](templates/issue-template.md) | Issue テンプレートと全レーンコメント様式（WIP / HOLD / 終端 / TAKEOVER / 再開チェック / 完了記録） |
| [templates/epic-template.md](templates/epic-template.md) | Epic テンプレートと人間チェックポイント表 |
| [templates/brief-template.md](templates/brief-template.md) | 委譲ブリーフのテンプレート（3層構造・書き方の要点） |
| [templates/publication-checklist.md](templates/publication-checklist.md) | リポジトリ公開チェックリスト — A1〜E4 の項目別判定・手順・証拠 artifact の正本 |
| [templates/architecture-parallel-map.md](templates/architecture-parallel-map.md) | 各リポの `ARCHITECTURE.md` に置く「並行安全マップ」テンプレート |
| [templates/ci/](templates/ci/README.md) | 機械の門番テンプレ一式 — テスト+lint / secret 検知 / PR サイズ / 歴史切断拒否 / 高リスク人間確認ゲート / 報告合成器（展開手順は同梱 README） |
| [templates/conformance/](templates/conformance/README.md) | 席決定の検証ベクタ31本（抽象 ID・`L1-9` / `L1-10` / `L1-11` / `FP-7`）とメンバー側での流し方 |
| [templates/seat-resolver/](templates/seat-resolver/README.md) | 席決定の参考実装（設定駆動・検証ベクタ31本を全通過・参考例であって必須部品ではない） |
| [CONTRIBUTING.md](CONTRIBUTING.md) | コントリビュートの流れ（Issue-first / WIP 宣言 / 完了記録の要約） |

最後に、このハンドブックがどこから来て、どこで使われているかを一言だけ。

---

<a id="ecosystem"></a>

## Caty AI ファミリー

<!-- family:generated:family-footer:start -->

---

このリポジトリは **Caty AI ファミリー** の一員です — AI エージェントの家族を運用するためのオープンなツール群。公開準備中のモジュールを含む全体の地図は [Family OS](https://github.com/caty-ai/family-os) にあります。

| 軸 | モジュール | 何をするもの | 状態 |
| --- | --- | --- | --- |
| 地図 | [Family OS](https://github.com/caty-ai/family-os) | AIファミリー全体の地図 — モジュール・状態・つながり | 公開・MIT |
| 掟 | **Family Dev Handbook** | 開発の交通ルール — Issue・PR・worktree・受け渡し・並行開発 | 公開・MIT |
| 縦軸・基盤 | [Caty Agent Harness](https://github.com/caty-ai/caty-agent-harness) | AIエージェントのタスク基盤 — 試行・リトライ・チェックポイント・完了判定 | 公開・MIT |
| 縦軸 | [context-kit](https://github.com/caty-ai/context-kit) | エージェント1体分の6点コンテキスト衛生キット — 大出力の退避・委譲ブリーフ検査・安全フック・記憶検索・worktree スナップショット | 公開・MIT |
| 縦軸 | [Persona Engine](https://github.com/caty-ai/persona-engine) | エージェントの既存人格に関係と感情のレイヤーを重ねる | 公開・MIT |
| 縦軸 | [Persona Growth Loop](https://github.com/caty-ai/persona-growth-loop) | 人格そのものを育てる — 最小・冪等な提案づくり | 公開・MIT |
| 縦軸 | [X Collector](https://github.com/caty-ai/x-collector) | Xやウェブの素材を1日1回のダイジェストに — 人にもエージェントにも | 公開・MIT |
| 縦軸 | [Self Growth Loop](https://github.com/caty-ai/self-growth-loop) | エージェントが自分の能力を育てるループ — 提案・ガバナンス・採用記録 | 公開・MIT |
| 横軸・基盤 | [Family Memory Architecture](https://github.com/caty-ai/family-memory-architecture) | 記憶バス — 家族が知っていることを共有する層 | 公開・MIT |
| 横軸 | [Sitter](https://github.com/caty-ai/sitter) | 委譲したエージェント実行の見張り番 — 監視・証拠の記録・宣言した範囲内でのみ再起動 | 公開・MIT |
| 横軸 | [Alpha Nightshift](https://github.com/caty-ai/alpha-nightshift) | 夜間自律保守ループ — deny-by-default の guard の内側で夜のレーンが走り、朝は人間が cherry-pick するだけ | 公開・MIT |

<!-- family:generated:family-footer:end -->

このハンドブックは単体で完結します。外部サービスも、姉妹リポジトリも、特定の記憶基盤も必要ありません。必要なのは git と Issue / PR、そしてルールを守る主体だけです。表の各リポジトリも同じように単独で使えます — 組み合わせは任意で、どれか1つだけを使っても成立します。

エージェント横断の一般規範（fail-posture の適用範囲など）のオーナーは family-os 側にあり、このハンドブックの担当は**人間とエージェントの協働プロトコル — 条文と、その執行を助ける配布用の型（templates/）— だけ**です。一般規範をここに新設することはしません。

現在地とこれからです。

---

<a id="status"></a>

## 開発ステータス

現行バージョンは **v0.18.0**（2026-08-21）。リポジトリ公開をゲートする **PB 層**（`PB-1`〜`PB-5`・[docs/11](docs/11-publication.md)）と、その正本チェックリスト（[templates/publication-checklist.md](templates/publication-checklist.md)・A1〜E4 の28項目）が加わりました（[#109](https://github.com/caty-ai/family-dev-handbook/issues/109)・棚卸しと決裁の親 = [#100](https://github.com/caty-ai/family-dev-handbook/issues/100)）。公開レーンは項目ごとの PASS / FAIL / 理由付き N/A と証拠 artifact で完了記録を書き、FAIL または検証不能な項目が残る限り公開しません（fail-closed）。(c) 項目はオーナー発行の記録（3形の発行者要件・自己申告は絶対に通過しない）だけで通過します。オーナー決裁2件 — 巨大 vendored 正本ファイルの `size-exempt` ラベル一本化（D7）と、公開前の全履歴 secret スキャンの must-pass 化（C1・ジョブ実装までは手動走査 + transcript）— を条文とチェックリストに焼き込みました。層 ID はコア契約 P1〜P5 との衝突を避けて `PB` です（設計レビュー3席の収束 finding）。PB-5 は時限のパイロット条項で、指名された第1・第2消費者レーンのギャップ還流が正本へ反映された時点で失効します。

- **v0.17.0**（2026-08-21） — T-5 のリリース履行を機械で強制する層が加わりました（[#103](https://github.com/caty-ai/family-dev-handbook/issues/103)）。① **release-sync キャリアー**（[templates/ci/](templates/ci/README.md)・reusable は API-only＝checkout なし）— annotated SemVer の `v*` タグ push から GitHub Release を自動作成します（notes はタグメッセージ・lightweight／非 SemVer／空メッセージは赤・免除は default branch 上の `.github/release-sync-ignore` のみ＝タグ側ツリーからの自己免除は不成立）。② **ドリフト監査**（`templates/ci/check-release-drift.sh`）— タグと Releases の乖離を API だけで検知してレポートします（検知のみ・自動削除なし・読めない時は findings ゼロで exit 2）。③ **条文追随** — tag URL 義務は **Release 実在まで含めて履行**になりました（[docs/10](docs/10-test-ci-baseline.md) `T-5`。素のタグでも `/releases/tag/<名前>` の URL は 200 を返すため、URL の存在は Release の存在を意味しません）。record-vs-reality の PR-side check と定期スイープは [#106](https://github.com/caty-ai/family-dev-handbook/issues/106) で追跡します。

- **v0.16.0**（2026-08-19） — テストと表示の正直さを閉じる2条を追加しました（[#81](https://github.com/caty-ai/family-dev-handbook/issues/81)）。① **テスト出力契約**（`T-6`・[docs/10](docs/10-test-ci-baseline.md)）— 家族製ランナーは `suites: declared=N executed=M skipped=K` の3値サマリを動的に出し、`declared = executed + skipped` を不変条件にします。exit code は閉じた集合、必須依存の欠落は `missing-dep:` と 127、異常終了でもサマリ必須です。SKIP 率20%超を赤とし、上限を変える場合は LC-3 型でローカル値と根拠を記録します。採用完了は CI の照合ゲートが有効になった時点です。② **表示契約**（`T-7`・[docs/10](docs/10-test-ci-baseline.md)）— 緑は機械が塗ったものだけ。README を持つ公開リポは T-1 の test workflow に結びつく live バッジか灰の `CI: not yet` を必ず示し、静的色は `lightgrey` / `blue` の閉じた列挙に限定します。条文内に Project status の標準形を置き、実測数字には run URL と実測日を必須にしました。設計の起点は consistency campaign W0-4 と family-os#56、確定は3席の設計レビューです。

- **v0.15.0**（2026-08-18） — 条文の改訂4点（[#75](https://github.com/caty-ai/family-dev-handbook/issues/75)・grok-build ランタイム解析の5席クロスレビューからの還流）。① **後続ラウンドのラチェット禁止**（`L1-3`・[docs/02](docs/02-issue-loop.md)）— round-2 以降で新たに blocking を追加できるのは実証済みの欠陥か未充足のゲート基準のみ。レビューラウンドが進むほど新しい好みが後出し blocking になりレーンが終端しない「ラチェットチャーン」を止める狭い条項です。② **指摘の引用要件**（`R-4`・[docs/09](docs/09-rejection-rubric.md)）— path:line を指すか実行ログを引用できない指摘は blocking にできない（non-blocking の懸念は自由）。①がその上に実証要件を重ねる引用水準の「床」の明文化です（二層の制約であり同一水準ではありません）。③ **B-4 に理由1文**（[docs/07](docs/07-delegation-brief.md)）— 常設 instruction ファイルが委譲境界で読まれず劣化する runtime も実在するため、必要な規約はブリーフ本文にインラインで書く。④ **git を触る自動化の衛生1文**（`L0-7`・[docs/03](docs/03-git-protocol.md)）— identity / config は毎回 env で明示し、ユーザーの git 状態を読まない・書かない。

- **v0.14.1**（2026-08-16） — 条文の改訂はありません — README（4言語）の v0.12.0 版歴が `T-5` の条文と食い違っていたのを訂正しました。未履行のレーン（`vX.Y.Z` を宣言したのにタグを切っていないレーン）は「**終端しないまま WIP として残り** stale 時計に乗る」のであって、非アクティブ扱いになるわけではありません（非アクティブ扱いが掛かるのは **tag URL を欠く MERGED** の方）。あわせて、同じ段落で `N/A` の閉じた列挙を「3類型」と書いていたのを **4類型**（v0.12.0 で入った Epic 子→epic を含む）に直しました。条文（[docs/10](docs/10-test-ci-baseline.md)）・i18n ミラー・[docs/04](docs/04-adoption.md) のダイジェストは当初から正しく、README だけが取り残されていた形です — 「要約層と正本が食い違えば正本が正・要約を追従させる」の自己適用にあたります（[#73](https://github.com/caty-ai/family-dev-handbook/issues/73)）。

- **v0.14.0**（2026-08-16） — 条文の改訂はありません — 席決定の**参考実装**（[templates/seat-resolver/](templates/seat-resolver/README.md)）が加わりました。v0.13.0 で配った検証ベクタ31本を**全通過する、設定駆動のリゾルバ**です。ルール表・モデル語彙・系統・リスク領域・writer をすべて設定から読むので、自分の家の構成に置き換えて使えます（実名モデル ID はコードにも設定例にも含みません）。**参考例であって必須部品ではありません** — 条文はこれを要求せず、使いたい家だけが使います。また**席決定の実装は各家に1つだけ**にしてください（同じ仕組みを複数リポにコピーすると権限と改訂が分裂します）。共有するのは実装ではなく、[templates/conformance/](templates/conformance/README.md) への適合です（[#71](https://github.com/caty-ai/family-dev-handbook/issues/71)）。

- **v0.13.0**（2026-08-15） — 条文の改訂はありません — 席決定の**検証ベクタ**（[templates/conformance/](templates/conformance/README.md)）が加わりました。各家のセレクタ（席を決めるプログラム）が、`L1-9` の席数・`L1-10` の異種と系統・`L1-11` の席数スケールと FP-7 に対して**実装非依存で自己採点**できる31本のケース集です。実名モデル ID を含まず（抽象 ID のみ）、条文と食い違えば条文が正（ベクタは導出物）。セレクタが表現できないケースは skip ではなく FAIL と数える fail-closed 運用で、版が変わるときは新ファイルを足して旧版を残します（採用記録が版を指すため）（[#63](https://github.com/caty-ai/family-dev-handbook/issues/63)）。

- **v0.12.0**（2026-08-15） — リリース既定の条文追加（`T-5`・[docs/10](docs/10-test-ci-baseline.md)）です。リリースタグはこれまで「安定点で git tag」の一言だけで、切り忘れても何にも引っかからず、セッションが変わると構造的に忘れられていました（実例が繰り返し観測されています）。T-5 は「忘れないようにする」のではなく「**忘れると完了記録（L1-7）が通らない**」形にします — すべての完了記録に **release 欄**（`vX.Y.Z` 宣言 / `deferred`（理由 + 退場トリガー付き Issue） / `N/A`（閉じた4類型の理由）の3語彙）を置き、**出荷相当の変更**（利用者が動かす挙動・公開 API・配布物・利用者が従う規範が変わる merge）は `N/A` を選べません（迷ったら出荷相当）。さらに宣言だけで終わらないよう、**タグを切って URL を載せた MERGED でなければレーンは終端しない**形にしました — 未履行のレーンは**終端しないまま WIP として残る**ので stale 時計（`L0-3`）に乗り、次のレーンが来ないリポでも切り忘れが可視になります（tag URL を欠く MERGED は**不正形式**で終端が成立せず、`L1-4` の非アクティブ扱いになります）。deferred は再浮上する面（トリガー付き Issue）に置き、2回続いたら3回目の出荷相当 merge では切る（`R-6` と同型のエスカレーション・計数は完了記録の `previous release` で後から検証できます）。適用は全リポ一律 — 出荷相当が無いリポは自然に N/A になるため、私有スクラッチに実質負荷はありません（[#64](https://github.com/caty-ai/family-dev-handbook/issues/64)）。

- **v0.11.0**（2026-08-15） — レビュー席の条文改訂2点（`L1-10` / `L1-11`・[docs/02](docs/02-issue-loop.md)）。① **S / M の席床が異種2席 → 異種3席**に上がりました — 発効は**メンバー（家）ごと**（発効データは正本リポの家ごと pinned Issue が持ち、発効前の家は旧床2席で適法 — **施行ギャップは「日程」であって「違反」ではない**（3フィールドの pinned Issue が無い家は「発効前」を主張できない）。初日から満たせない法を即時全員発効で出さないための形で、SEAT-WAIT の対象はレーンのみと明文化）。② **実名カタログ条項と correlated-seats** — 家族で共有する実名モデルカタログはデータ層としてハンドブックの外に置き、非規範（カタログは法が禁じる席を合法化できず、生存確認できないモデルを使用可能にできない）。席の系統は、機械が選ぶ経路（抽選・代打）では相互異系統または記録された例外が必須、オーナー名指しパネルの同系統着席は記録つき correlated-seats フラグがある場合に限り適法。出発点は MoA ファミリー全体化設計 — 7席×2周の設計レビューと3席 delta 確認を経た v2.1 の条文化（[#45](https://github.com/caty-ai/family-dev-handbook/issues/45) / [#57](https://github.com/caty-ai/family-dev-handbook/issues/57)）

- **v0.10.0**（2026-08-14） — テスト & CI 基準層（`T-1`〜`T-4`・[docs/10](docs/10-test-ci-baseline.md)）。コードを含む新規リポは作成時にテストランナー + CI を整備・サイズ M / L / H のバグ修正は再現テスト同梱が既定・委譲ブリーフに「追加・変更したテストと実行結果」を標準項目化・CI 赤のままの merge 禁止（例外は4条件を満たす既知無関係の赤のみ）。出発点は [caty-ai/x-collector#9](https://github.com/caty-ai/x-collector/issues/9)
- **v0.9.2**（2026-08-11） — 機械の門番テンプレ（[templates/ci/](templates/ci/README.md)）の硬化改訂。初回展開（3リポ）の実測から還流した「静かに緑」の欠陥3件を型で塞ぎました（`RISK_PATHS_AUTH` 常設カテゴリ新設・`none` 宣言の大小文字硬化と宣言行の健全性検査・展開検証の落とし穴を README に追記）。多席レビュー4ラウンド（3席全 GO）を経て、展開済みリポへ同期済み
- **v0.9.1**（2026-08-10・タグなし・型のみの改訂） — `RISK_PATHS_GATES` 常設カテゴリの新設と、既定網への Makefile / `scripts/ci/**` の追加（v0.9.0 の展開検証からの還流）
- **v0.9.0**（2026-08-10） — 機械の門番テンプレ一式（[templates/ci/](templates/ci/README.md)）が加わりました — テスト+lint / secret 検知 / PR サイズ上限 / 歴史切断拒否 / 高リスク人間確認ゲート / 報告合成器の6門番を、対象リポへコピーして置くだけの standalone 型として配ります。全ゲートは検証不能・未設定のとき赤（fail-closed）・承認は head SHA に束縛。設計にあたり [Hermes Agent](https://github.com/NousResearch/hermes-agent)（MIT）を一部参考にさせていただきました（→ [謝辞](#acknowledgements)）。

- **v0.8.0**（2026-08-09） — R 却下ルーブリック層（`R-1`〜`R-6`・[docs/09](docs/09-rejection-rubric.md)）が加わりました — 「どう進めるか」（L 層）に対して「何を受け入れ・何を断るか」を定める意図の層です。人間の判断なしに閉じてよいのは機械的に白黒がつく3理由だけで、価値判断による却下はオーナー専決。歓迎する貢献6箇条・よくできていても断るもの7箇条・前提検証の4パターン・置き場所のはしご6段・「破られた方針は check に昇格」を条文にしています（[Hermes Agent](https://github.com/NousResearch/hermes-agent) の Contribution Rubric を一部参考にしています）。

- **v0.7.1**（2026-08-07） — 上流レビュー（`L1-9`・[docs/02](docs/02-issue-loop.md)）の対象列挙をサイズ体系（L / H / Epic = 重い側）へ揃える文言追従
- **v0.7.0**（2026-08-07） — サイズ判別基準（`L2-1` 拡張・[docs/01](docs/01-milestone-loop.md)）。定義表と3軸・迷ったら重い側
- **v0.6.0**（2026-08-07） — ワークスペース・ライフサイクル層（`LC-1`〜`LC-5`・[docs/08](docs/08-lifecycle.md)）。置いた物の退場を契約に（退場トリガー・検査は警告のみ・退場条件の数値はローカル正本）
- **v0.5.0**（2026-08-06） — 委譲ブリーフ層（`B-1`〜`B-5`・[docs/07](docs/07-delegation-brief.md)）。依頼文を実装仕様・実装チェック・レビュー基準の3層で契約に（様式は [templates/brief-template.md](templates/brief-template.md)）
- **v0.4.0**（2026-08-05） — 第3の前提「シンプルに作る — 複雑さは要件で消す」（[docs/why-simple-systems.md](docs/why-simple-systems.md)）と、L2-1 への要件疑いフック（消す決定は依頼者）
- **v0.3.0**（2026-07-31） — Epic レーン（`E-1`〜`E-10`）と、実装着手前の上流異種レビュー（`L1-9`〜`L1-11`）
- **v0.2.1 / v0.2.0**（2026-07-22） — MIT ライセンスと community health files の整備、家族固有の記述を外した汎用化
- **v0.1.0 / v0.1.1**（2026-07-21） — ルールを散文から契約へ。安定 rule ID・閉じた5状態語彙・証拠つきマージゲート・失敗時姿勢の宣言

これからの予定は [Issue 一覧](https://github.com/caty-ai/family-dev-handbook/issues)が正本です。README では二重に管理しません。

提案の入り口も、同じルールの上にあります。

## Project status

[![Test + Lint](https://github.com/caty-ai/family-dev-handbook/actions/workflows/test-lint.yml/badge.svg)](https://github.com/caty-ai/family-dev-handbook/actions/workflows/test-lint.yml)

- CI: ローカル caller から Test + Lint を含む reusable `@ci-v1` セット（5ゲート）を実行し、suite-count 照合を有効にしています。CI と同じエントリーポイントをローカルで実行するには `make test` と `make lint` を使います。
- 検証済み環境: CI で `ubuntu-latest` と `macos-latest` を実行し、macOS でのローカル開発も行っています。WSL2 も対象です — `ubuntu-latest` レーンが検証しているのと同じ GNU 経路で動きます（clone は `/mnt/c` 配下ではなく Linux ファイルシステム側に）。
- maturity: `stable` — 規範の正本です。
- 既知の制約: runtime code を持たない docs-only リポジトリです。また、タイ語ミラーの既知のリンク2件を [#89](https://github.com/caty-ai/family-dev-handbook/issues/89) で追跡しています。

---

<a id="contributing"></a>

## コントリビュート

- 変更提案はこのリポジトリに Issue を立て、PR を出し、別モデルまたは別エージェントのレビューを受けてから merge します（self-approve は禁止です）
- **このハンドブック自身がこの手順で更新されています** — WIP 4フィールド宣言 → worktree → クロスモデルレビュー → 完了記録つき PR。条文の追加も改定も、すべてこの手順を通っています
- 詳しい流れは [CONTRIBUTING.md](CONTRIBUTING.md) へ

最後に、この形の元になったプロジェクトへ、ひとことお礼を。

---

<a id="acknowledgements"></a>

## 謝辞

- [Hermes Agent](https://github.com/NousResearch/hermes-agent)（Nous Research・MIT） — 公開されている自律エージェントのフレームワークです。その貢献受け入れ基準（Contribution Rubric）と CI ゲートの構成には多くの学びがあり、R 却下ルーブリック層（docs/09）と templates/ci の設計にあたって一部参考にさせていただきました。templates/ci には同プロジェクト由来のファイル（翻案2本・そのままのコピー1本）を含みます — ファイル単位の由来は [templates/ci/NOTICE.md](templates/ci/NOTICE.md) にまとめています。

使う条件は、いちばんゆるい形にしてあります。

---

<a id="license"></a>

## ライセンス

[MIT](LICENSE) © 2026 Sho Jikumaru

ルールは広まってこそ意味があるので、改変も再配布も自由な MIT にしています。fork して自分のチームに合わせて厳しくする使い方を想定しています。

<div align="center">

**条文はドキュメントのみ** ｜ **ランタイム不要** ｜ **git と Issue / PR だけで動く**

</div>
