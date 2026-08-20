# PB 公開準備 — リポジトリ公開をチェックリストでゲートする層

L 層（L2 / L1 / L0）が「作業をどう進めるか」、R 層が「何を受け入れるか」、T 層が「正しさの証明をどう蓄積するか」の契約であるのに対し、PB 層は**リポジトリを公開するレーンが、公開前の確認を項目ごとの証拠で完了したことをどう示すか**を契約にする。各ルールに安定 rule ID（`PB-1`〜`PB-5`）を付し、条ごとに適用対象を〔 〕で明記する。完了記録の正本は [docs/02](02-issue-loop.md)、検証できない時の姿勢は [docs/05](05-fail-posture.md)、出荷と証拠の規律は [docs/10](10-test-ci-baseline.md) に置く。正本の配置は [R-5](09-rejection-rubric.md) の置き場所のはしご、後続の check 化は [R-6](09-rejection-rubric.md) の一般規律に従い、価値判断は [R-1](09-rejection-rubric.md) を越えない。

本層の `PB-1`〜`PB-5` は README のコア契約 `P1`〜`P5`（v0.1.0・凍結）とは別物。

背景: 家系リポジトリの整合 campaign では、表示の正直さ、CI の実効性、秘密・履歴、レビュー、完了記録、組織連携をリポジトリごとに手作業で検証した。この実績を [Issue #100](https://github.com/caty-ai/family-dev-handbook/issues/100) の Phase 1〜4 で棚卸しし、[Phase 2 の28項目](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5355210694)と[Phase 4 の条文骨子](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5355215540)へ整理したうえで、[オーナー決裁](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5359570954)により宣言形・必須度・パイロット順序を確定した。本章は、その結果を公開レーンのゲートとして定める。

<a id="pb-1"></a>

## PB-1 ゲート束縛 — 公開は項目ごとの証拠で止める〔private→public 切替・新規 public 作成 = MUST〕

**リポジトリを公開するレーンは、[PB-2](#pb-2) の正本チェックリストでゲートする。完了記録には、チェックリストのヘッダーを様式の正本とする項目ごとの PASS / FAIL / N/A 表と、各項目が指定する証拠 artifact を置く。検証不能な項目は未通過とし、公開しない。**

理由: campaign では全項目に現実の失敗例があり、散文の注意書きだけでは防げなかった。項目単位の証拠を求めることで、確認していない状態を「確認済み」と扱う経路を閉じる。これは [docs/05](05-fail-posture.md) の fail-closed 姿勢を公開レーンへ適用し、表示の正直さを [T-7](10-test-ci-baseline.md) と同じ意味に保つものである。

境界の明文化:

- 家系リポジトリの fork、または第2 public リモートを新規に公開する場合は対象
- 外部の第三者が公開しているリポジトリの fork は対象外。適用する価値判断はオーナー専決（[R-1](09-rejection-rubric.md) の価値判断規律）
- public→private→public の再公開はチェックリストを再走する。直近記録を引用した差分再走の方法はチェックリストのヘッダーに従う
- GitHub 外のミラーとパッケージレジストリへの公開は対象外
- 既に公開済みのリポジトリへの遡及は対象外。ただし次に関係箇所を触るレーンでは [T-1](10-test-ci-baseline.md) と同型の opportunistic な準用を行い、棚卸し専用レーンは立てない

<a id="pb-2"></a>

## PB-2 チェックリストの置き場と版 — 走った正本を固定する〔公開チェックリスト本体・全公開レーン〕

**チェックリストの正本は [templates/publication-checklist.md](../templates/publication-checklist.md) とし、その版は handbook のリリースタグに従属する。公開レーンは原則として参照したリリースタグを完了記録に記す。タグにまだ含まれない状態で走った場合に限り commit SHA を記し、後にその状態を含むリリースタグを同じ完了記録へ追記する。**

理由: [handbook#80](https://github.com/caty-ai/family-dev-handbook/issues/80#issuecomment-5344053714) では、配布 caller が `ci-v1` タグの実在前に pin されるレースが起きた。正本の場所だけでなく、実際に走った内容を解決できる版まで固定しなければ、同じ名前のチェックリストで異なる判定が生じる。

<a id="pb-3"></a>

## PB-3 分類の境界 — 通過形を分類ごとに閉じる〔公開チェックリストの全項目〕

**(a) 項目は機械証拠である run URL、(b) 項目は機械化が実装されるまでチェックリストが項目ごとに名指しする手動手順とその記録、(c) 項目はオーナーのラベルまたは記録された決裁によってのみ通過する。(c) 項目は自己申告では絶対に通過しない。**

(c) の発行者要件は次の3形だけである:

1. オーナーアカウントによるラベルイベント
2. オーナー本人が投稿したコメント
3. リレー記録に対する、オーナーによる事後の検証可能な追認（追認リンク必須）

これ以外は未通過とする。項目ごとの必須度・宣言形はチェックリストが定める。

理由: harness#121 では「オーナー決裁」と書かれた自己申告に、検証可能なオーナー本人の許可が存在しない実害が起き、[事後追認](https://github.com/caty-ai/caty-agent-harness/issues/121#issuecomment-5341374987)で一度だけ救済された。決裁の内容だけでなく発行者を第三者が検証できなければ、オーナー専決（[R-1](09-rejection-rubric.md) の価値判断規律）は成立しない。

<a id="pb-4"></a>

## PB-4 記録の完全性 — 1レーン1記録を解決可能に保つ〔公開レーンの完了記録〕

**公開レーン1本につき完了記録はちょうど1つとし、レーン Issue に置く。公開レーンに限り [L1-7](02-issue-loop.md) の完了記録の置き場をレーン Issue とする特則であり、PR 本文には記録本体でなくレーン Issue へのポインタ1行を置く。[T-5](10-test-ci-baseline.md) の release / previous release 連鎖を適用し、run URL は実在する run に解決して head SHA が候補 SHA と一致しなければならない。**

理由: [family-memory-architecture#33](https://github.com/caty-ai/family-memory-architecture/issues/33#issuecomment-5354966162) では完了記録が追跡 Issue に置かれ、PR だけを見る scanner では見落とすことが分かった。一方、persona-growth-loop#16 では[先行記録](https://github.com/caty-ai/persona-growth-loop/issues/16#issuecomment-5341012500)と[事後記録](https://github.com/caty-ai/persona-growth-loop/issues/16#issuecomment-5345278041)の相反する完了記録が2つ残るアノマリーが起きた。置き場と個数を固定し、[L1-8](02-issue-loop.md) の訂正は差し替え記録として同じ連鎖に残すことで、単一の監査入口を保つ。証拠の解決可能性は campaign の [L1-8 訂正記録](https://github.com/caty-ai/family-os/issues/64#issuecomment-5353192649)と同じ基準である。

<a id="pb-5"></a>

## PB-5 パイロット条項（時限） — 実運用のギャップを正本へ返す〔チェックリスト運用の立ち上げ期〕

**オーナーが指名した第1・第2消費者レーンは、各項目の運用ギャップを [Issue #100](https://github.com/caty-ai/family-dev-handbook/issues/100) に報告し、正本チェックリストへ反映する。パイロット反映前に走るレーンは、実際に走ったチェックリスト状態を PB-2 に従って記録する。**

消費者の指名記録は [#100 のオーナー決裁コメント](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5359570954) とする。本条のマージ提案は原則、第1消費者のギャップ還流をチェックリストへ反映した後に行う。先行はオーナー専決（[R-1](09-rejection-rubric.md) の価値判断規律）とする。

第1・第2消費者レーンのギャップ報告が #100 に揃い、正本チェックリストへ反映された時点で本条は失効する。条文からの削除は後続 PR で行い、規範変更 = 出荷相当として [T-5](10-test-ci-baseline.md) を適用する。

理由: 手動手順の費用と曖昧さは実際の公開レーンで初めて測れる。2本の消費者レーンから還流して正本を直す一方、どの状態で判定したかを残すことで、パイロット中の変更を過去の判定へ黙って遡及させない。
