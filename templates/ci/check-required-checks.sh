#!/usr/bin/env bash
# 展開検証: branch protection の required status checks 登録を機械確認する。
#
# なぜ: 門番を置いても required checks に登録し忘れると「赤は出るが merge は止まらない」。
# この登録確認を README のお願いで終わらせない (handbook docs/09 R-6 の自己適用 —
# 「強制したい方針は、破られたら赤になる check に昇格させる」)。
#
# 使い方: bash check-required-checks.sh <owner/repo> [branch]   (要 gh CLI・認証済み)
# 姿勢: 読めない・未設定 = 赤 (fail-closed)。branch protection が張れない環境
#       (private の無償プラン等) では、その旨を導入台帳に明示記録する (FP-5: 劣化の可視化)。
# 型の正本: caty-ai/family-dev-handbook templates/ci/

set -euo pipefail

REPO="${1:?usage: check-required-checks.sh <owner/repo> [branch]}"
BRANCH="${2:-main}"

# CUSTOMIZE: required に登録する check 名。handbook#80 (reusable workflow_call 化) 以降、
# 各門番は「caller job / reusable job」の形式で check 名が決まる (caller は templates/ci/*.yml、
# reusable は caty-ai/family-dev-handbook/.github/workflows/reusable-*.yml@ci-v1 側の job)。
# pr-size は既定で required に含めない (可視化ゲート — 各リポの判断で追加)。
EXPECTED=(
  "test-lint / test"
  "test-lint / lint"
  "gitleaks / gitleaks"
  "history-check / history-check"
  "risk-review-gate / risk-review-gate"
)

CONTEXTS=$(gh api "repos/${REPO}/branches/${BRANCH}/protection" \
  --jq '.required_status_checks.contexts[]?' 2>/dev/null) || {
  echo "RED: branch protection for ${REPO}@${BRANCH} is unreadable or not configured."
  echo "     If protection cannot be enabled on this plan, record that explicitly in the adoption ledger (FP-5)."
  exit 1
}

MISSING=0
for CHECK in "${EXPECTED[@]}"; do
  if ! grep -Fxq "$CHECK" <<<"$CONTEXTS"; then
    echo "MISSING required check: ${CHECK}"
    MISSING=1
  fi
done

if [ "$MISSING" -ne 0 ]; then
  echo "RED: some gates are not registered as required status checks — they will show red but will not block merges."
  echo "     Register them: repo Settings → Branches → Branch protection rules → Require status checks."
  exit 1
fi

echo "GREEN: all expected gates are registered as required status checks on ${REPO}@${BRANCH}."
echo "registered contexts:"
printf '%s\n' "$CONTEXTS" | sed 's/^/  - /'
