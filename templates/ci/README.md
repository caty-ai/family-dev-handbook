# templates/ci — 機械の門番キャリアー stencil 一式

家族のリポに配る「機械の一次ゲート」の型の正本は `caty-ai/family-dev-handbook` の
`.github/workflows/reusable-*.yml`（`workflow_call` の reusable workflow・`@ci-v1` タグで pin）。
このディレクトリはその **caller stencil**（配布用の薄いコピペ元）を置く場所であり、ゲートの実装
（fail-closed ロジック・design-rationale コメント）は reusable 側にのみ存在する。多席レビュー
（handbook L1-3 / L1-11）の手前で、機械的に白黒がつく問題を先に止めるための層であり、レビュー席
の代替ではない。席決定機構そのものの検証ベクタは [templates/conformance](../conformance/README.md) を参照。

## これは何 — 6門番の一覧

| ファイル | 守るもの | 赤になる条件 | 出典 |
|---|---|---|---|
| `test-lint.yml` | テスト・lint が通らないコードの merge | テスト/lint 失敗・**コマンド未設定**（fail-closed） | 新規 |
| `gitleaks.yml` | 秘密情報の main 到達 | 検知あり・走査範囲が解決不能/空（fail-closed） | 新規 |
| `pr-size.yml` | レビュー不能な巨大 PR | 除外後 250 行超（既定・**required 非登録の可視化ゲート**） | 新規 |
| `history-check.yml` | 歴史切断 PR（blame 崩壊） | main と共通祖先なし | 翻案（hermes-agent） |
| `review-labels.yml` | 高リスク領域の無確認 merge | 高リスクパス変更 + `risk-reviewed` ラベルなし・名簿/宣言の不備（fail-closed） | 翻案（hermes-agent） |
| `scripts/assemble_review_comment.py` | （Layer 2）門番報告の PR コメント1枚化 | —（合成器・ゲートではない） | そのまま（hermes-agent） |

**review-labels の現時点の位置づけ**: オーナー確認の**可視化+監査**装置。赤止め（ラベルが付くまで merge 不可）は機能するが、全エージェントがオーナーの資格情報を共有する運用では「AI がラベルを貼れない」ことの機械的保証は **identity 分離の完了まで無い**。無断貼付はプロトコル違反（handbook E-5）として扱い、PR timeline の監査証跡で追及する — 検知は機械・判定と追及は人間（「検証済み」を装わない — FP-5）。

## 展開手順（コピペ順）

1. `templates/ci/*.yml`（**caller stencil**）を対象リポの `.github/workflows/` へ、`scripts/assemble_review_comment.py` を `scripts/ci/` へコピー（Layer 2 を使わないなら合成器は後回しでよい）。各ファイルの `uses:` 行が `caty-ai/family-dev-handbook/.github/workflows/reusable-<gate>.yml@ci-v1` を pin していることを確認する（バージョニングは下記「バージョニング」節を参照）
2. `.github/risk-reviewers.txt` を作成: `risk-reviewers.txt.example` をコピーし、オーナー（人間）の GitHub ID を記入（プレースホルダのままなら赤）
3. ラベルを作成:
   ```bash
   gh label create needs-risk-review --color D93F0B --description "高リスク領域に触れた PR (機械が自動付与)"
   gh label create risk-reviewed    --color 0E8A16 --description "オーナー確認済み (人間のみが貼る・push で自動剥がし)"
   gh label create size-exempt     --color FBCA04 --description "サイズ上限の免除 (オーナーのみが貼る・push で自動剥がし)"
   ```
4. 各キャリアーの `with:` ブロックを必要に応じて埋める（stencil 自体は薄く保ち、説明はここに集約する）:
   - `test-lint.yml` — `run_macos` / `macos_skip_reason`（macOS 分を落とすなら理由をセットで明示。空または空白だけだと赤）/ `require_suite_reconciliation`（既定 `false`。`suites: declared=N executed=N` 行が無い場合は `::notice::` を出して通す。`true` のときはその行が無いだけで赤。行がある場合は `executed != declared` または `executed == 0` なら常に赤。テスト/lint コマンド自体は reusable 側が Makefile の `test`/`lint` ターゲットを試す）
   - `pr-size.yml` — `max_lines` / `exclude_patterns`（サイズ計測の除外パターン。既定の除外〔lockfile・`i18n/**`〕は reusable 側に内蔵済み）
   - `review-labels.yml` — **`risk_paths_billing` / `risk_paths_outbound` / `risk_paths_gates` / `risk_paths_auth`（高リスク領域のリポ固有パスをカテゴリ別に宣言）。「該当なし」でもカテゴリごとに `none` の明示宣言まで必須**（いずれかが `__DECLARE_ME__` のままなら赤）。AUTH は既定網の `**/auth/**` が「認証コードは auth/ ディレクトリにある」配置前提のため常設 — フラット配置（`app/auth.py` 等）のリポは実パスを列挙し、auth/ 配下に集約済みのリポだけ `none` と書く（AUTH=none で `**/auth/**` が0マッチのリポには検知ログが警告を出す）。**複数パターンは1行1パターンの改行区切り**（空白区切りで1行に並べると「空白を含む1つの pathspec」＝0件マッチになるため、行内空白は赤で止まる）。「該当なし」の受理語は `none` のみ（大小文字不問・`n/a` 等の同義語は不可）
5. branch protection の required status checks に各門番の check 名を登録する。**handbook#80 以降、check 名は「`<caller job> / <reusable job>`」の形式になる**: `test-lint / test`・`test-lint / lint`・`gitleaks / gitleaks`・`history-check / history-check`・`risk-review-gate / risk-review-gate`。**`pr-size` は既定で required に含めない**（可視化ゲート・required 化は各リポの判断）
   macOS を required に入れる場合は `test-lint / test-macos` と `test-lint / test-macos-skip` を必ず対で登録する。片方だけだと skip 側の赤が merge を止めず、`run_macos: false` 時に skipped=success の穴が再び開く。既定はどちらも required 非登録。
6. **`check-required-checks.sh` を実行して登録を機械確認する**（この script の `EXPECTED` は上記の新しい check 名形式で既に更新済み）:
   ```bash
   bash check-required-checks.sh <owner/repo> main
   ```
   登録確認を README のお願いで終わらせない（R-6 の自己適用）。branch protection が張れない環境（private の無償プラン等）は、その旨を導入台帳に明示記録する（FP-5: 劣化の可視化）。あわせて **detect-risk-paths ジョブのログに死にパターンの `::warning::` が出ていないことを確認する**（警告は「緑だが守れていない可能性」の唯一のシグナル — 出ていたら宣言を直してから「展開済み」）

## バージョニング

`@ci-v1` は handbook のリリースで維持する **moving major タグ**（`actions/checkout@v6` と同じ慣行 —
v1 系の中では後方互換な改善・バグ修正のみが `ci-v1` に流れ込む）。破壊的変更（入力の削除・意味変更、
job 名の変更など required checks の再キーが必要になる変更）は `ci-v2` を新設して行い、既存の caller
は明示的に `@ci-v2` へ書き換えるまで `ci-v1` のまま動き続ける。同リポ内 (family-dev-handbook 自身) の
呼び出し元だけは `@ci-v1` を pin せずローカルパス (`./.github/workflows/reusable-<gate>.yml`) で参照する
— 改訂 PR が古いタグの内容で自己検証されるデッドロックを避けるため。

## カスタマイズ早見表

| ファイル | `with:` 入力 | 既定値 |
|---|---|---|
| `test-lint.yml` | `run_macos` / `macos_skip_reason` / `require_suite_reconciliation` | `run_macos: true` / `require_suite_reconciliation: false`（suite 行不在は `::notice::` を出して通す。コマンド自体は reusable 側で Makefile 不在 = 赤） |
| `gitleaks.yml` | なし（バージョン pin + SHA256 は reusable 側の固定値・更新は handbook 改訂で） | gitleaks v8.30.1 |
| `pr-size.yml` | `max_lines` / `exclude_patterns` | `max_lines: '250'`（除外は lockfile・`i18n/**` が内蔵済み） |
| `review-labels.yml` | `risk_paths_billing` / `risk_paths_outbound` / `risk_paths_gates` / `risk_paths_auth`（カテゴリ別・宣言必須） | 各 `__DECLARE_ME__`（= 赤） |
| `check-required-checks.sh` | `EXPECTED`（required に登録した check 名。`<caller job> / <reusable job>` 形式） | 5 門番（pr-size 除く） |

## 落とし穴

- **required checks 未登録** — 門番は赤を出すが merge は止まらない。手順 6 の機械確認まで終えて「展開済み」
- **展開検証のダミー secret に bare な AWS access key ID（AKIA+16桁）を使わない** — gitleaks v8.30.1 の既定ルールでは access key ID 単体は検知されず、「門番が壊れている」ように見える偽陰性になる。検知確認済みフィクスチャ（例: 切り詰めた PEM 秘密鍵ブロック）を使う。仕込みはサーバーサイドコミット（contents API）推奨 — ローカルの secret 検知フックと手元 commit がデッドロックするため
- **test/lint の充て先は「対象0件で緑」にならない形に** — 対象を数えて0件なら赤にする（導入例: 本リポ自身の Makefile は対象ファイルの非空ガード込み）。`with:` でコマンドを差し替えられるわけではない（reusable 側は Makefile の `test`/`lint` ターゲット固定）ので、この性質は reusable 側で保たれる
- **シェルスクリプトの lint 充て先は `*.sh` glob だけにしない** — 拡張子なし（shebang のみ）のスクリプトが漏れる。shebang スキャン（例: `grep -rl '^#!.*sh' --exclude-dir=.git`）を併用して対象を組み立てる
- **死にパターン警告は「緑だが守れていない」の唯一のシグナル** — 宣言パターンが HEAD の1ファイルにも解決しない時、detect-risk-paths ログに `::warning::` が出る（LC-5: 検知は機械・判断は人間 — check は赤にならない）。展開時（手順 6）と、リネーム・配置変更を含む PR のマージ時に確認し、出ていたら宣言を追随させる。例外は1つ: **auth コードが本当に無いリポの `risk_paths_auth: 'none'` は AUTH 警告が常在する（仕様）** — 「auth コード無し」を確認した記録を宣言行のコメントに残せば、その警告は既知として許容してよい
- **v0.9.2 で `risk_paths_auth` が増えた（第4常設カテゴリ）** — v0.9.1 以前の展開済みリポにキャリアーを再コピーすると、AUTH を宣言するまで全 PR が赤になる（仕様・fail-closed）。更新 PR に AUTH 宣言（実パス列挙 or `none`）を必ず同梱する
- **fetch-depth** — 履歴を使う門番（gitleaks / pr-size / history-check / review-labels）は `fetch-depth: 0` が必須（reusable 側に焼き込み済み・浅くすると「diff 解決不能 → 緑」の fail-open になる）
- **fork PR** — ゲート判定（read）は fork でも必ず走って赤/緑を出す。承認・免除は**作者が単独で起こせるイベント（synchronize / reopened / ready_for_review、pr-size は edited も）の run では常に無効**で、緑に戻せるのは triage 権限者しか起こせないイベント（labeled / unlabeled）だけ — 作者単独の承認持ち回しは fork でも成立しない。ラベル付与・剥がし（write）は 403 で警告になる（可視化の劣化のみ）。**残余**: 剥がせない古いラベルが triage 権限者の別ラベル操作（labeled / unlabeled の run）で再び有効に見える経路は残る — 共有クレデンシャル環境ではこの線引き自体が identity 分離（機械的保証の前提）待ちであり、このゲートの「可視化+監査」位置づけの範囲内。厳密な SHA 束縛が要る場合は方式2（タイムライン3条件 AND）へ
- **`pull_request_target` は使わない** — untrusted コードに write トークンを渡す典型的脆弱形（全門番 `pull_request` トリガ）
- **gitleaks の赤を消しても秘密は無効化されない** — 一度 push した秘密は必ず rotate する。本線は commit 前のローカル hook・CI は最後の網。検知の許容（allowlist）は base 側 `.gitleaks.toml` だけが効く — PR 側の設定・`.gitleaksignore`・inline `gitleaks:allow` は無効化してある（自己緩和封じ）
- **承認後の push で承認が無効になるのは仕様** — 承認（`risk-reviewed` / `size-exempt`）は「オーナーが見た head SHA」に束縛される。無効化はゲート自身のイベント判定で行われ、ラベル剥がしジョブは可視化のための衛生（「剥がしは機械・貼るのは人間」）
- **ワークフロー自身の改変は機械的には止められない** — `pull_request` トリガは PR head 側のワークフロー定義（caller の `with:` 入力・呼び出し先タグを含む）で実行されるため、門番を無力化する PR はその無力化された門番で判定される（循環）。防御は PR timeline の監査＋可能なら `.github/workflows/` への CODEOWNERS 必須化。これがこのゲートを「可視化+監査」装置と位置づける理由の一つ
- **`pr-size.yml` と `review-labels.yml` の caller types は削らない** — `labeled` / `unlabeled` / `ready_for_review`（`pr-size` は `edited` も）が無いと、免除や承認の付与・剥奪や PR 本文更新で再評価されず、緑が古く残る

## Layer 2（合成器）の配線スケッチ

各門番は `review_status` JSON（`source` + `results[]`）を artifact として出力できる（history-check / review-labels は出力済み）。親 workflow で各門番の artifact を集め、`scripts/ci/assemble_review_comment.py` に渡すと PR コメント1本に合成される。**配線 workflow は型として置かない** — 最初の導入リポで実配線を検証してから型に昇格する（R-6「実体で検証」の向き）。発展形として「required checks の登録状態を毎 PR で self-check する門番」のアイデアも同レーンで検証する。

## 出典とライセンス

[NOTICE.md](NOTICE.md) を参照（hermes-agent 由来ファイルの区分・MIT 全文・取得日）。
