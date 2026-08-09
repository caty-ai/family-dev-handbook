# templates/ci — 機械の門番テンプレ一式

家族のリポに配る「機械の一次ゲート」の型の正本。各門番は **standalone**（このディレクトリからコピーして置くだけで、PR に赤/緑が出る）。多席レビュー（handbook L1-3 / L1-11）の手前で、機械的に白黒がつく問題を先に止めるための層であり、レビュー席の代替ではない。

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

1. `templates/ci/*.yml` を対象リポの `.github/workflows/` へ、`scripts/assemble_review_comment.py` を `scripts/ci/` へコピー（Layer 2 を使わないなら合成器は後回しでよい）
2. `.github/risk-reviewers.txt` を作成: `risk-reviewers.txt.example` をコピーし、オーナー（人間）の GitHub ID を記入（プレースホルダのままなら赤）
3. ラベルを作成:
   ```bash
   gh label create needs-risk-review --color D93F0B --description "高リスク領域に触れた PR (機械が自動付与)"
   gh label create risk-reviewed    --color 0E8A16 --description "オーナー確認済み (人間のみが貼る・push で自動剥がし)"
   gh label create size-exempt     --color FBCA04 --description "サイズ上限の免除 (オーナーのみが貼る・push で自動剥がし)"
   ```
4. `# CUSTOMIZE` を埋める:
   - `test-lint.yml` — テスト/lint コマンド（**未設定のままだと赤で落ち続ける = 仕様**）
   - `pr-size.yml` — サイズ計測の除外パターン
   - `review-labels.yml` — **高リスク領域のリポ固有パスをカテゴリ別に宣言（`RISK_PATHS_BILLING` = 課金・支出 / `RISK_PATHS_OUTBOUND` = 対外公開・対人送信）。「該当なし」でもカテゴリごとに `none` の明示宣言まで必須**（どちらかが `__DECLARE_ME__` のままなら赤）
5. branch protection の required status checks に各門番の check 名（`test` / `lint` / `gitleaks` / `history-check` / `risk-review-gate`）を登録する。**`pr-size` は既定で required に含めない**（可視化ゲート・required 化は各リポの判断）
6. **`check-required-checks.sh` を実行して登録を機械確認する**:
   ```bash
   bash check-required-checks.sh <owner/repo> main
   ```
   登録確認を README のお願いで終わらせない（R-6 の自己適用）。branch protection が張れない環境（private の無償プラン等）は、その旨を導入台帳に明示記録する（FP-5: 劣化の可視化）

## カスタマイズ早見表

| ファイル | 差し替え箇所 | 既定値 |
|---|---|---|
| `test-lint.yml` | `# CUSTOMIZE` ×2（test / lint コマンド） | `make test` / `make lint`（Makefile 不在 = 赤） |
| `gitleaks.yml` | なし（バージョン pin + SHA256 は型の固定値・更新は handbook 改訂で） | gitleaks v8.30.1 |
| `pr-size.yml` | 除外パターン / `MAX_LINES` | lockfile・`i18n/**` 除外 / 250 行 |
| `review-labels.yml` | `RISK_PATHS_BILLING` / `RISK_PATHS_OUTBOUND`（カテゴリ別・宣言必須） | 各 `__DECLARE_ME__`（= 赤） |
| `check-required-checks.sh` | `EXPECTED`（required に登録した check 名） | 5 門番（pr-size 除く） |

## 落とし穴

- **required checks 未登録** — 門番は赤を出すが merge は止まらない。手順 6 の機械確認まで終えて「展開済み」
- **fetch-depth** — 履歴を使う門番（gitleaks / pr-size / history-check / review-labels）は `fetch-depth: 0` が必須（型に焼き込み済み・浅くすると「diff 解決不能 → 緑」の fail-open になる）
- **fork PR** — ゲート判定（read）は fork でも必ず走って赤/緑を出す。承認・免除は**作者が単独で起こせるイベント（synchronize / reopened / ready_for_review、pr-size は edited も）の run では常に無効**で、緑に戻せるのは triage 権限者しか起こせないイベント（labeled / unlabeled）だけ — 作者単独の承認持ち回しは fork でも成立しない。ラベル付与・剥がし（write）は 403 で警告になる（可視化の劣化のみ）。**残余**: 剥がせない古いラベルが triage 権限者の別ラベル操作（labeled / unlabeled の run）で再び有効に見える経路は残る — 共有クレデンシャル環境ではこの線引き自体が identity 分離（機械的保証の前提）待ちであり、このゲートの「可視化+監査」位置づけの範囲内。厳密な SHA 束縛が要る場合は方式2（タイムライン3条件 AND）へ
- **`pull_request_target` は使わない** — untrusted コードに write トークンを渡す典型的脆弱形（全門番 `pull_request` トリガ）
- **gitleaks の赤を消しても秘密は無効化されない** — 一度 push した秘密は必ず rotate する。本線は commit 前のローカル hook・CI は最後の網。検知の許容（allowlist）は base 側 `.gitleaks.toml` だけが効く — PR 側の設定・`.gitleaksignore`・inline `gitleaks:allow` は無効化してある（自己緩和封じ）
- **承認後の push で承認が無効になるのは仕様** — 承認（`risk-reviewed` / `size-exempt`）は「オーナーが見た head SHA」に束縛される。無効化はゲート自身のイベント判定で行われ、ラベル剥がしジョブは可視化のための衛生（「剥がしは機械・貼るのは人間」）
- **ワークフロー自身の改変は機械的には止められない** — `pull_request` トリガは PR head 側のワークフロー定義（RISK_PATHS の写像を含む）で実行されるため、門番を無力化する PR はその無力化された門番で判定される（循環）。防御は PR timeline の監査＋可能なら `.github/workflows/` への CODEOWNERS 必須化。これがこのゲートを「可視化+監査」装置と位置づける理由の一つ

## Layer 2（合成器）の配線スケッチ

各門番は `review_status` JSON（`source` + `results[]`）を artifact として出力できる（history-check / review-labels は出力済み）。親 workflow で各門番の artifact を集め、`scripts/ci/assemble_review_comment.py` に渡すと PR コメント1本に合成される。**配線 workflow は型として置かない** — 最初の導入リポで実配線を検証してから型に昇格する（R-6「実体で検証」の向き）。発展形として「required checks の登録状態を毎 PR で self-check する門番」のアイデアも同レーンで検証する。

## 出典とライセンス

[NOTICE.md](NOTICE.md) を参照（hermes-agent 由来ファイルの区分・MIT 全文・取得日）。
