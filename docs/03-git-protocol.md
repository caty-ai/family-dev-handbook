# L0 git規律 — 物理衝突を防ぐ層

複数セッション / 複数エージェントが**同一リポを並行して触る前提**の規律（2026-07-03 合意・2026-07-21 に契約化）。
各ルールに安定 rule ID（`L0-1`〜`L0-9`）を付す。要約側（[docs/04](04-adoption.md)）はこの ID を参照する。検証できない時の姿勢は [docs/05](05-fail-posture.md)。

## L0-1 着手前の被り確認 + WIP宣言（Issue = ソフトロック）

```bash
gh issue list --state open
gh pr list --state open
```

で被りを確認してから、担当 Issue に WIP コメントを書く（[テンプレ](../templates/issue-template.md)）。

WIP 宣言がソフトロックとして効力を持つのは、**4つの必須フィールドを備えている間だけ**:
`agent / date / Files to touch / Branch`

フィールドを欠く WIP はロックとして無効 — スコープ不明として扱い、そのレーンと関わる作業は直列にする（[FP-7](05-fail-posture.md)）。他のセッションは、有効な WIP のファイル集合と交差する作業に着手しない。

## L0-2 宣言パスの意味論 — 宣言外は触らない（default-deny）

- パスは**リポルート相対**。ファイル名はそのファイルだけを指す。末尾スラッシュのディレクトリはその配下すべてを覆う
- glob・否定（`!` 除外）は禁止
- `Files to touch: UNKNOWN` と宣言したレーンは**直列専用**（並行不可）
- **宣言していないファイルはスコープ外**（default-deny）。触る必要が出たら、スコープ外への最初の書き込みの*前*に WIP を再宣言し、並行相手との交差チェック（[L2-4](01-milestone-loop.md)）をやり直す
- **実効ファイル集合**には rename の両パス・削除・lockfile・生成物も数える（宣言・交差判定の両方で）
- **楽観的再読** — レーンでの最初の書き込みの前にアクティブな WIP 群を読み直し、GO 判定以降に変化（WIP の増減・宣言内容の変更・再宣言）があれば交差判定をやり直す

## L0-3 ロックの失効と引き継ぎ（stale = 72h / TAKEOVER）

ロックが失効するのは: branch が merge / 削除された・stale・`RELEASE` コメント・`HANDED-OFF` コメント。
`RELEASE` / `HANDED-OFF` は**ロックのライフサイクルコメント**であって L1-4 のレーン状態ではない（様式は[テンプレ](../templates/issue-template.md)）。**発行できるのはロック所有者（WIP の agent）だけ** — 他者の発行は無効で、他者がロックを外す経路は stale + TAKEOVER のみ。

- **stale = 72h 宣言/更新なし**（GitHub コメントのタイムスタンプで測る — 更新は新しいコメントを書けば足りる。staleness 計測用の独自タイムスタンプ欄は増やさない: プラットフォームのメタデータを重複させない。WIP 宣言本体の `date` フィールドは L0-1 どおり必須のまま）。長い沈黙が予定されるレーンは WIP 宣言時に**理由つき**で長い窓を明示してよい（例外であって既定ではない。事後の延長は新しいコメントとして可視に行う）
- **stale ⇒ 所有者不明 ⇒ 黙って空き扱いしない**。stale レーンを引き取る手順: L0-9 再開チェックリスト + stale WIP を引用した **`TAKEOVER` コメント** + 新しい WIP 宣言
- 72h という数字の調整は、運用データ（週次 probe）を根拠に**本ハンドブックの PR でのみ**行う（レーン内で勝手に変えない）。調整不可なのは「stale を黙って自由化しない」という不変条件の方

HOLD はロックの失効事由では**ない**（非終端 — [L1-5](02-issue-loop.md)）。HOLD コメントは**ロックの扱い**（review-by まで保持 or 解放）を必ず明記する — ロックに無言な HOLD は無効。

## L0-4 1セッション = 1 Issue = 1 branch = 1 worktree

1レーン / 1 worktree につき**アクティブな書き手は1つ**。共有 checkout では作業しない:

```bash
git worktree add ../<repo>-wt/<issue> -b fix/<issue>-<slug> origin/main
```

## L0-5 main はマージ専用

main への直接 push 禁止。すべて PR 経由。

## L0-6 PR 本文に触ったファイル一覧 + diff 照合

WIP宣言との差分（宣言より増えた/減ったファイル）がレビューで見えるようにする。
merge 時は宣言ファイル集合と `git diff --stat` を突き合わせる — **diff にあって一覧にないファイルは blocking**（[L1-7](02-issue-loop.md) 完了証拠ゲートの一部）。

**多段レーンの PR 本文に `close(s|d) #N` / `fix(es|ed) #N` / `resolve(s|d) #N` の文字列を書かない。** GitHub のキーワード解析は否定形も文脈も読まず、`Does not close #18` と書いても merge 時に #18 を閉じる（sitter#18・handbook#80 で実害）。閉じるキーワードを使ってよいのは**その merge だけで Done when の全項目が満たされるとき**に限る。bootstrap PR・複数段の PR・merge 後に Done when が残る PR では「leaves #N open」「tracked in #N」のように書き、Issue の close は最終段の完了記録（[L1-4](02-issue-loop.md) の終端コメント）で行う。

## L0-7 マージは1本ずつ

```
git fetch → rebase origin/main → 再検証（typecheck / tests）→ merge
```

merge 後、他のオープンブランチは速やかに rebase する。2本同時に merge しない。
**隣接 PR が merge されたら、キューで待つ PR は rebase + 再検証（typecheck / tests 再実行）の義務を負う** — rebase が通っただけでは義務を果たしたことにならない。

git を触るスクリプト・自動化は、**identity / config を毎回 env で明示し、ユーザーの git 状態を読まない・書かない**（global / local config・実 index・HEAD に依存せず、必要なら一時 index を使う）。実行アカウント名義で刻まれる API マージ事故の構造的一般化。

## L0-8 ブランチは小さく短命に

長生きしたブランチは rebase 地獄になる。マージ保留する PR は **HOLD コメント**（必須フィールドは [L1-5](02-issue-loop.md)）で状態を明示し、黙って放置しない。

## L0-9 再開チェックリスト — 再開・引き継ぎレーンの最初の書き込み前

再開 / 引き継ぎ / TAKEOVER したレーンでは、**最初の書き込みの前に**、以下4点の確認結果を Issue コメントとして1本投稿する（[テンプレ](../templates/issue-template.md)）:

1. **ロック** — 自分のものか、L0-3 に照らして失効しているか
2. **ファイルスコープ** — 宣言ファイル集合が現 origin/main に照らして今も正確で、**かつ**現在アクティブな全 WIP/PR と非交差か（`gh issue list` + `gh pr list --state open` を再実行。この項目は「自分の宣言スコープはまだ有効か？」という1つのゲートに2つの照会を束ねている）
3. **branch** — fetch / rebase がクリーンに通るか（遅れている時・merge 前は rebase）
4. **Done when** — handoff 時から変わっていないか

不一致が出たら: 修復 / handoff・TAKEOVER / 直列化のいずれか。**他エージェントの生きたロックの上で黙って続行しない。**
チェックリストは**この4項目で固定**。投稿したコメント自体が監査可能な成果物であり、項目を増やさない（チェックリスト疲れが名指しされた失敗モード）。

## 事故が起きたら

- conflict が出た → 慌てず rebase で解消。解消が大きくなるなら、その事実を Issue にコメントして直列に切り替える
- 宣言外のファイルを触る必要が出た → **書き込む前に** WIP を再宣言し、交差チェックをやり直す（L0-2）
- 間違えて main に push した → revert commit で戻し、経緯を Issue に記録
