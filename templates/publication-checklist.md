# リポジトリ公開チェックリスト

## 目的

このチェックリストは、リポジトリ公開レーンが [PB-1](../docs/11-publication.md#pb-1) のゲートを項目ごとの判定と証拠 artifact で通過したことを記録するための正本である。

⟨RS-n⟩ = 各家のローカル公開前ゲート由来の由来注記。参照先が無くても各項目は自己完結している。

項目 ID は rule ID ではないが同様に安定 ID として扱い、追加は各セクションの末尾、削除は欠番とする。

## 版規則

[PB-2](../docs/11-publication.md#pb-2) に従い、原則は参照した handbook リリースタグを記録し、タグ未包含の状態で走った場合に限り commit SHA を記録して、その状態を含むタグが出た後にタグを完了記録へ追記する。

```text
checklist version: <handbook release tag>
# タグ未包含時だけ
checklist commit: <full commit SHA>
checklist release tag (追記): <その状態を含む handbook release tag>
```

## 消費者手順

1. A1〜E4 の全28項目について、項目が指定する証拠 artifact を収集する。
2. レーン Issue の完了記録に次の表を**ちょうど1つ**置く。判定は `PASS` / `FAIL` / 理由付き `N/A` のいずれかとし、証拠欄には項目が指定する artifact 本体または解決可能なポインタを記す。

   ```markdown
   | ID | 判定 | 証拠 artifact | 注記 |
   |---|---|---|---|
   | A1 | PASS / FAIL / N/A（理由） | <項目指定の証拠> | <必要な補足> |
   ```

3. public→private→public の再公開では、直近の完了記録を引用し、前回以後に変わった項目と再公開によって結果が変わり得る項目を再走する。新しい表には全28項目を載せ、再利用する証拠には引用元を、再走した証拠には今回の artifact を記す。
4. 曖昧・不足・誤分類を見つけたら [Issue #100](https://github.com/caty-ai/family-dev-handbook/issues/100) へギャップとして報告する。

(c) 項目の所要時間を計測するのは [PB-5](../docs/11-publication.md#pb-5) が指す消費者レーンだけである。

(b) 項目は、機械化が実装されたら該当行の手動手順を run URL に置き換える。

分類セルは [Phase 2 確定版](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5355210694) の原文を保持している: **(a)** = 今日の既存 handbook reusable による機械検査、**(b)** = 機械化可能だが未実装、**(c)** = オーナーのラベルまたは決裁記録だけで通す人間判断。

## A — リポジトリの初期構成（構造と入口）

| ID | 項目 | 分類 | 今日どう通すか | 証拠 artifact |
|---|---|---|---|---|
| A1 | リポジトリ作成時から test を gate とする CI を置く（T-1）。CI がまだ無い場合は緑を装わず、README に `CI: not yet` と書く | (b) — no bootstrap conformance check exists; T-1 is prose | test-lint caller の存在と pin を目視確認し、実行する。未整備なら README の `CI: not yet` を確認する | test-lint caller の初回 run URL、または README の明示的な `CI: not yet` |
| A2 | `make test` / `make lint` の入口が存在し、終了コードを伝播する（campaign rule 4。強制失敗時に make が Error になることまで確認する） | (b) — checkable by a bootstrap script; today proven only by seat sandbox runs | `make test` と `make lint` を実行し、隔離した作業状態で意図的な失敗を入れて非0終了を確認する | ローカル実行 transcript + 強制失敗の証明 |
| A3 | lint target を no-op にしない。失敗不能な lint を緑のバッジの背後に置かない | (b) — mechanizable as "lint job must have ≥1 failable step / placeholder-echo detector" | lint 違反を一時的に導入し、lint が赤になることを隔離した作業状態で確認する | lint 違反を導入した mutation が赤になる証明 |
| A4 | 5つの gate caller（test-lint / pr-size / review-labels / gitleaks / history-check）が存在し、`@ci-v1` に pin され、`templates/ci` の正本と byte-identical であり、走査ロジックをリポジトリ内へ複製していない | (a) today the *identity* is seat-verified by hand; caller presence is machine-fact | 5 caller の初回 run URL を記録し、各ファイルの SHA256 を正本と照合する | 正本との SHA256 照合 + 初回 run URL |
| A5 | T-6 の reconciliation を配線し、`require_suite_reconciliation: true` で有効化する。既定値 false のままは inert gate である | (b) — flag presence is greppable; today unchecked | caller の入力値を確認し、test-lint を実行してサマリの3値が照合されることを確認する | `declared=N executed=N skipped=K` を示す green run |
| A6 | branch protection / required checks を登録し、gate を助言でなく blocking にする（`branches/main/protection` の状態を確認する） | (c) today (owner-only settings) / (b) verifiable half: a read-only API probe can red-flag absence | オーナーのラベル / PB-3 の発行者要件を満たす決裁記録 | API probe 出力 + オーナー行動の記録。`branches/main/protection` の 404 は「保護なし」と「権限不足」を区別しないため、曖昧な probe 結果は通過にしない。`rulesets` も併測する（Phase 1 §3.5 の実績形） |

## B — 表示の正直さ（README・バッジ・数字）

| ID | 項目 | 分類 | 今日どう通すか | 証拠 artifact |
|---|---|---|---|---|
| B1 | 緑バッジは機械だけが塗る。静的バッジは T-7 の閉じた色許可リストに従い、全バッジ URL が解決する | (b) — badge-lint (slug points at this repo, endpoint 200, color allowlist) is a concrete gap | バッジごとに URL を取得し、対象リポジトリ・HTTP 応答・静的色を T-7 と照合する | バッジごとの curl transcript |
| B2 | 手書きの実測値には日付と解決可能な出典を付ける。「日付の無い件数 = 0」とする | (c) with a (b) assist: a date-adjacency lint can flag bare numbers; truth needs a human | オーナーのラベル / PB-3 の発行者要件を満たす決裁記録 | grep sweep + 記録 |
| B3 | 対応環境表 ⟨RS-1⟩、hero image ⟨RS-2⟩、相互 nav を持つ4言語 README ⟨RS-4⟩、docs の3層構造を備える | (b) — presence/cross-link lint is trivial; content quality stays (c) | 存在と相互リンクは publication-gate を実行し、対象ファイルの一覧を記録して確認する。内容品質はオーナーのラベル / PB-3 の発行者要件を満たす決裁記録で通す | publication-gate run（今日の部分適用範囲）+ ファイル一覧 |
| B4 | social preview を 1280×640 にし ⟨RS-3⟩、Settings の description を英語で設定する ⟨RS-10⟩ | (c) — API-readable but set by owner; (b) probe possible | オーナーのラベル / PB-3 の発行者要件を満たす決裁記録 | API probe（`gh api repos/OWNER/REPO --jq .description` 等） |
| B5 | OS に関する主張を正確にし、skip を可視化する。`run_macos` / `macos_skip_reason` を使い、理由のない skip は赤にする | (a) — reusable enforces once caller adopts matrix inputs | test-lint reusable の matrix 初回 run URL を記録する | skip lane を含む最初の matrix run URL |
| B6 | Issue label を既定9個のままにせず設計する ⟨RS-11⟩。component: / platform: / severity: の軸を持ち、priority と severity を併存させない | (b) — label-census script exists in spirit (.github#19: 11/11→14/14 measured by seats); no reusable | `gh api repos/OWNER/REPO/labels` の出力を取得し、軸と併存禁止を確認する | `gh api .../labels` の census 出力 |

## C — 秘密情報と履歴

| ID | 項目 | 分類 | 今日どう通すか | 証拠 artifact |
|---|---|---|---|---|
| C1 | gitleaks caller を実際の初回 run まで通す。reusable が走査するのは merge-base..HEAD の PR range であって full history ではないことを明記し、これとは別に公開前の全履歴走査 ⟨RS-6⟩ を **must-pass** とする | (a) for PR-range; **(b) gap: one-shot full-history scan as a publication-time job** | PR-range reusable の run URL を記録する。全履歴ジョブの実装までは、リポジトリ root で `gitleaks git --no-banner --redact --log-opts="--all" .` を実行し、コマンド・gitleaks version・終了コード・全出力を transcript に記録する | PR-range caller の run URL + 手動 full-history 走査 transcript |
| C2 | history-check caller を実際の初回 run まで通す（merge-base / unrelated histories gate。空の range は fail-closed） | (a) | history-check reusable の初回 run URL を記録する | 初回 run URL |
| C3 | `.publication-denylist` を置き、D8 に適合させる。commit する denylist は保護対象の literal を露出してはならず、公開安全な表記 / gitignore + CI への秘密注入 / 記録された明示受容、の3形から選ぶ | (a) for gate execution; **(c) for D8 choice** (which of the 3 options, recorded per repo); (b) gap: a literal-exposure self-scan on the denylist file itself | オーナーのラベル / PB-3 の発行者要件を満たす決裁記録 | publication-gate run + 記録された D8 の選択 |
| C4 | 内部情報を sweep する ⟨RS-5⟩。家族名、個人パス、`_handoffs/`、スクリーンショット、Issue / PR 内のテストログを対象に含める | (c) — judgment; publication-gate covers denylist-declared patterns only | オーナーのラベル / PB-3 の発行者要件を満たす決裁記録 | 対象範囲を列挙した sweep 記録 |
| C5 | publication-gate script を正本と byte-identical に vendoring し、embedded selftest を T-6 の counted suite として green にする | (a) | publication-gate selftest の run URL を記録し、blob identity を正本と照合する | blob identity 注記 + selftest run URL |

C1 の full-history 走査を must-pass とする理由と、ジョブ実装まで手動 transcript で満たす根拠は [#100 のオーナー決裁2](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5359570954) に置く。

## D — レビューと merge の規律

Phase 2 原文では D1, D2, D3, D7, D4, D5, D6 の順だったものを、ID を変えず昇順に並べ替えている。

| ID | 項目 | 分類 | 今日どう通すか | 証拠 artifact |
|---|---|---|---|---|
| D1 | サイズに応じたレビュー席を確保し（L1-9 / L1-10）、requested / actual を記録する。fallback と無効票は原文のまま記録し、verdict の無い拒否を票に数えない | (c) — quorum is human process; (a) assist: review-labels reusable enforces label presence | オーナーのラベル / PB-3 の発行者要件を満たす決裁記録 | 完了記録内の seat table |
| D2 | 人間承認 gate を head SHA / event に束縛する。close→reopen 前の承認を有効なまま扱わず、リポジトリごとに一度その束縛を検証する | (a) — the gate behaves this way today; checklist item is "verify the binding once per repo" | review-labels reusable の run URL を記録し、head SHA とラベルイベントの対応を確認する | timeline 抜粋 |
| D3 | merge は noreply identity を用いたローカル `--no-ff` とし、PR manifest との diff 照合を記録する。noreply email の前例と、API merge の identity 事故からローカル merge を採る前例は別々である | (c) process + (b) gap: a post-merge probe could verify merge-commit authorship/email pattern | オーナーのラベル / PB-3 の発行者要件を満たす決裁記録 | merge SHA + 完了記録内の identity 注記 |
| D4 | L1-7 フィールドと **T-5 release / previous release 連鎖**を持つ完了記録を作る。deferred は Issue 参照、N/A は閉じた類型、タグは annotated であることを記録する | (c) today; **(b) gap: T-5 record-linter** (parse completion comments; verify tag exists+annotated+dereferences to merge SHA; walk 1-hop chain) — the fos#64 L1-8 record fixed exactly what this linter would catch (skipped v0.2.1 hop, non-resolving run IDs) | オーナーのラベル / PB-3 の発行者要件を満たす決裁記録 | 完了記録 URL + タグ検証 |
| D5 | 記録中の全 run URL が実在する run に解決し、head SHA が候補 SHA と一致することを確認する | (b) — resolvable-evidence linter is a concrete, high-value gap | 各 run URL を再取得し、実在と head SHA の一致を記録する | 手動の再取得注記 |
| D6 | 完了記録をレーン Issue に置き、1レーンにつき1記録だけにする | (b) partial: "exactly one completion record per closed lane Issue" is machine-checkable | レーン Issue のコメントを確認し、完了記録がちょうど1つであることを記録する | 完了記録 URL |
| D7 | pr-size を超える vendored canonical file は、**オーナー付与の `size-exempt` ラベル + 正本との blob identity 根拠**だけを宣言形とする。過去の advisory-red 受容・無ラベルは grandfathered な歴史であり、前例にしない | (c) choice of form is owner rule-making; (a) assist: pr-size gate + blob check | オーナーのラベル / PB-3 の発行者要件を満たす決裁記録 | オーナーアカウントの `size-exempt` ラベルイベント + 正本との blob SHA identity 注記 |

D7 の唯一の宣言形は [#100 のオーナー決裁1](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5359570954) を反映した意図的差分である。

## E — 組織と registry の統合

| ID | 項目 | 分類 | 今日どう通すか | 証拠 artifact |
|---|---|---|---|---|
| E1 | family-os の `modules.json` に published 状態と #62 契約の pin fields を持つ registry entry を置き、次の weekly run で orphan check を green にする | (a) — family-os machine checks + weekly lane | family-os の registry check run URL を記録する | registry diff + check run URL |
| E2 | family footer を決定的に render し、再実行の diff が0であることを確認する | (a) — renderer + idempotence pattern (fma#24) | renderer を実行して、同じ入力で再実行した diff が0であることを記録する | 再実行 diff transcript |
| E3 | org-default template を継承するか意図的に上書きし、GraphQL の `repository.issueTemplates` で結果を確認する | (b) — probe script exists as recorded practice, not a reusable | GraphQL query を実行し、返された template 一覧を記録する | GraphQL 出力 |
| E4 | community health files ⟨RS-9⟩、LICENSE=MIT/Caty ⟨RS-8⟩ を備え、quickstart をコピー&ペーストで実行する ⟨RS-7⟩ | LICENSE presence (b)-trivial; quickstart (c) — human execution | LICENSE と community health files の存在は API / community standards 画面で確認して記録する。quickstart の実行判定はオーナーのラベル / PB-3 の発行者要件を満たす決裁記録で通す | community standards の screenshot / API + 実行 transcript |
