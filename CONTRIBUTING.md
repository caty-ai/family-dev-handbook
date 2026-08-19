# Contributing / コントリビュートガイド

**このハンドブックは、自分自身のルールで更新される。** コントリビュートの手順そのものが、このリポが定めるプロトコル（L2/L1/L0）の実演になる。

> **English summary**: This handbook is maintained under its own rules. To contribute: (1) file an Issue first with *Why / Done when / predicted files to touch*; (2) post a 4-field WIP declaration (`agent / date / Files to touch / Branch`) on the Issue before starting; (3) work in a dedicated worktree/branch, touching only declared files; (4) get a cross review — the merge-approving reviewer must be a different model or a different agent from the implementer (no self-approval); (5) put an L1-7 **completion record** (Done-when → PASS/FAIL/reasoned-N/A with inline evidence, candidate SHA, declared-vs-diff reconciliation, identity check) in the PR body. Field schemas: [templates/issue-template.md](templates/issue-template.md). Canonical docs are Japanese.
> Prerequisites are Python 3.9+, `make`, and `git` on macOS or Linux; `make test` and `make lint` are the same entry points used by CI.

## Prerequisites / 前提ツール

ローカルでの変更と検証には、次の環境が必要です。macOS と Linux をサポートしています。

| Requirement / 必要条件 | Notes / 補足 |
|---|---|
| Python 3.9+ | 呼び出されるチェッカーが Python 3.9+ を宣言し、`list[...]` などの組み込みジェネリック型構文（3.9+）を使います。必要なのは標準ライブラリのみで、`tomllib` やサードパーティ製パッケージは不要です。 |
| `make` | `Makefile` の検証ターゲットを実行します。 |
| `git` | 変更差分と worktree を管理します。 |

テスト実行: `make test` と `make lint` は、CI が使うものと同じエントリーポイントです（T-1 / T-6）。

## 変更提案の流れ

### 1. Issue-first（L1-1 / L1-2）

コード・文書の変更は **GitHub Issue 起点**（例外は typo 等の1行修正のみ）。本リポは docs-only のため、L1-1 本文にある「非コード md/json/yaml」の例外は**このリポ自身には適用しない**（文書がプロダクトそのものであるため・ローカルポリシーとして契約より厳しく運用）。Issue 本文には必須3点を書く（[テンプレ](templates/issue-template.md)）:

- **目的 Why** — なぜ必要か、やらないと何が困るか
- **完了条件 Done when** — 機械判定・実機判定できるチェックボックス形式
- **触るファイル / モジュール予測** — 並行GO判定（L2-4）の入力

### 2. WIP 宣言（L0-1）

着手前に `gh issue list` / `gh pr list --state open` で被りを確認し、担当 Issue に **4フィールドすべて**を備えた WIP コメントを書く:

```markdown
🔒 WIP (<agent名> session, YYYY-MM-DD): <何をするか1行>

agent: <agent名>
date: YYYY-MM-DD
Files to touch:
- path/to/file1
Branch: fix/<issue>-<slug> (worktree)
```

フィールドを欠く WIP はロック無効。宣言していないファイルは触らない（default-deny・L0-2）。

### 3. worktree で実装（L0-4）

1セッション = 1 Issue = 1 branch = 1 worktree。共有 checkout では作業しない:

```bash
git worktree add ../<repo>-wt/<issue> -b fix/<issue>-<slug> origin/main
```

### 4. クロスレビュー（L1-3）

- **self-approve 禁止** — 実装した本人だけの承認で merge しない
- merge を通すレビューは、実装者と**モデルまたはエージェントが異なる**こと
- blocking 指摘が 0 になるまで implementer → reviewer のループを回す

### 5. 完了記録つき PR（L1-7 / L0-6）

PR 本文に**完了記録**を貼る（[様式](templates/issue-template.md)）。最低限:

- **candidate SHA**（レビュー時点の PR head と一致）
- **Done when → PASS / FAIL / 理由付き N/A** の対応表 + インライン証拠
- **宣言 vs 実 diff の照合**（`git diff --stat origin/main...<SHA>` — 宣言にないファイルは blocking）
- **identity check**（implementer と reviewer の別モデル / 別エージェントの明記）
- **CI 状態**（green / 赤の例外は T-4 の成立条件4点すべて必須）

merge 後は Issue を close し、各導入先のローカル要約（CLAUDE.md 等）を追従させる（owner-applies）。

## スコープの注意

- 契約本文（docs/01〜03・05〜10 の rule ID つきルール）の変更は影響が大きい。**rule ID は安定 ID** — 番号の振り直し・意味の変更は原則しない（追加は末尾番号）
- エージェント横断の一般規範（fail-posture / stop-precedence 等）は本リポのスコープ外（[docs/05](docs/05-fail-posture.md) 冒頭の規範オーナー分担を参照）。ここには**人間⇔エージェント協働プロトコルの文言**だけを置く
- 条文は役割語（オーナー / エージェント / レビュー席 / 各家 など）で書き、固有名・内部パス・非公開リポ名を書かない

## 言語

- 正本（docs/・templates/・README.ja.md）は**日本語**。README.md（英語）・README.zh.md（简体中文）・README.th.md（ไทย）は各言語の入口（食い違えば日本語が正）
- 条文や README の内容を変える PR は、**4言語の README を同じ PR で更新する**。翻訳版は見出し数・階層・コードブロック数・リンク先集合・画像先集合が正本と一致している必要がある（片方だけ直すと構造検査が落ちる）
- Issue / PR / commit message は日本語・英語どちらでも可
