# NOTICE — 出典とライセンス

`templates/ci/` の一部は [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)（MIT License）に由来する。取得日: 2026-08-09。

## 各ファイルの由来区分

| ファイル | 区分 | 取得元 |
|---|---|---|
| `history-check.yml` | **翻案**（standalone 化+checkout を PR head SHA に固定・検知ロジックと事故実録コメントは原文維持） | [.github/workflows/history-check.yml](https://github.com/NousResearch/hermes-agent/blob/main/.github/workflows/history-check.yml) |
| `review-labels.yml` | **翻案**（standalone 化・検知統合・ラベル語彙と承認判定を家庭版に変更） | [.github/workflows/review-labels.yml](https://github.com/NousResearch/hermes-agent/blob/main/.github/workflows/review-labels.yml) |
| `scripts/assemble_review_comment.py` | **そのまま**（冒頭の出典ヘッダ追記のみ・本体差分ゼロ） | [scripts/ci/assemble_review_comment.py](https://github.com/NousResearch/hermes-agent/blob/main/scripts/ci/assemble_review_comment.py) |
| `test-lint.yml` / `gitleaks.yml` / `pr-size.yml` / `risk-reviewers.txt.example` / `check-required-checks.sh` / `README.md` | **新規**（本リポ設計。設計思想の一部は hermes-agent の Contribution Rubric / CI 構成の調査に基づく） | — |

由来のあるファイルは冒頭に次の様式のヘッダを持つ:

```
# Adapted from NousResearch/hermes-agent (MIT)
# Source: https://github.com/NousResearch/hermes-agent/blob/main/<path>
# Retrieved: 2026-08-09 / Changes: <変更点の要約>
```

関連: 条文側の翻案は [docs/09-rejection-rubric.md](../../docs/09-rejection-rubric.md)（章前文の出典1行が本 NOTICE の様式を参照する）。

## MIT License（hermes-agent 原文）

```
MIT License

Copyright (c) 2025 Nous Research

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
