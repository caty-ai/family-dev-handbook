#!/usr/bin/env bash
# Audit T-5 release drift in one GitHub repository without cloning it.
#
# Scope: v*-named tags and Releases only. Non-v*-named Releases are deliberately outside
# this lane. The script reads API state and never mutates tags, Releases, or repository data.
# Exemptions come only from .github/release-sync-ignore on the target's default branch:
# exact tag names, one per line, # comments, no globs. The active list is printed every run.
# Classes: RED = missing/draft/orphan Release; WARNING = legacy/non-SemVer tag, staged/stray draft.
#
# Fail posture: every gh read uses --paginate --slurp. All responses are parsed and shape-
# checked before any finding is printed. Any failed read or unparseable payload exits 2 with
# zero findings. Push permission is required because lesser tokens cannot see drafts; the
# audit refuses to turn narrowed visibility into fabricated findings (FP-6 / FP-7).
#
# Moved-tag boundary: no reliable original-target diff exists. tagger.date >
# release.created_at is a noisy current-state heuristic and was rejected because of false
# positives. A tag ruleset forbidding update/deletion of v* is the mechanical defense.
#
# Usage: bash check-release-drift.sh <owner/repo>   (requires gh CLI, jq, authenticated token)
# Source of truth: caty-ai/family-dev-handbook templates/ci/

set -euo pipefail

if [ "$#" -ne 1 ] || [[ "$1" != */* ]]; then
  echo "usage: check-release-drift.sh <owner/repo>" >&2
  exit 2
fi

REPO=$1
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

fail_read() {
  echo "ERROR: $1; refusing to report any findings." >&2
  if [ -s "$TMP_DIR/api.err" ]; then
    printf '  last API stderr: ' >&2
    tail -n 2 "$TMP_DIR/api.err" >&2
  fi
  exit 2
}

read_api() {
  local label=$1 endpoint=$2 output=$3
  shift 3
  if ! gh api --paginate --slurp --method GET "$endpoint" "$@" > "$output" 2> "$TMP_DIR/api.err"; then
    fail_read "cannot read $label from the GitHub API"
  fi
  jq -e . "$output" >/dev/null 2>&1 || fail_read "$label returned unparseable JSON"
}

# One preflight snapshot supplies both authority and the default branch.
read_api "repository metadata" "repos/$REPO" "$TMP_DIR/repo.json"
if ! PUSH_PERMISSION=$(jq -r \
  'if length == 1 and (.[0] | type) == "object" and (.[0].permissions.push | type) == "boolean" and (.[0].default_branch | type) == "string" and (.[0].default_branch | length) > 0 then .[0].permissions.push else error("malformed repository metadata") end' \
  "$TMP_DIR/repo.json"); then
  fail_read "repository metadata is malformed"
fi
if [ "$PUSH_PERMISSION" != "true" ]; then
  echo "ERROR: token cannot see drafts — refusing to report; .permissions.push must be true." >&2
  exit 2
fi
DEFAULT_BRANCH=$(jq -r '.[0].default_branch' "$TMP_DIR/repo.json")

# A missing exemption file is the declared empty-list case. Any other error is fatal.
set +e
gh api --paginate --slurp --method GET \
  "repos/$REPO/contents/.github/release-sync-ignore" \
  -f "ref=$DEFAULT_BRANCH" > "$TMP_DIR/ignore.json" 2> "$TMP_DIR/ignore.err"
IGNORE_RC=$?
set -e
if [ "$IGNORE_RC" -eq 0 ]; then
  jq -e . "$TMP_DIR/ignore.json" >/dev/null 2>&1 || fail_read "release-sync exemption file returned unparseable JSON"
  if ! jq -r \
    'if length == 1 and (.[0] | type) == "object" and (.[0].content | type) == "string" then .[0].content else error("malformed contents payload") end' \
    "$TMP_DIR/ignore.json" | tr -d '\n' | base64 --decode > "$TMP_DIR/ignore.raw"; then
    fail_read "release-sync exemption file is malformed"
  fi
elif grep -Fq '(HTTP 404)' "$TMP_DIR/ignore.err"; then
  : > "$TMP_DIR/ignore.raw"
else
  fail_read "cannot read .github/release-sync-ignore from $REPO@$DEFAULT_BRANCH"
fi

awk '{ sub(/\r$/, ""); sub(/^[[:space:]]+/, ""); sub(/[[:space:]]+$/, "") }
     /^[[:space:]]*#/ || /^[[:space:]]*$/ { next }
     { print }' "$TMP_DIR/ignore.raw" > "$TMP_DIR/ignore.active"

read_api "full tag list" "repos/$REPO/git/matching-refs/tags/" "$TMP_DIR/tags.json"
read_api "full Release list" "repos/$REPO/releases" "$TMP_DIR/releases.json"

# Validate complete payload shapes before emitting the exemption list or any finding.
jq -e '
  type == "array" and all(.[]; type == "array") and
  all(.[][];
    type == "object" and
    (.ref | type) == "string" and (.ref | startswith("refs/tags/")) and
    (.object | type) == "object" and
    ((.object.type == "tag") or (.object.type == "commit")) and
    (.object.sha | type) == "string" and (.object.sha | length) > 0)
' "$TMP_DIR/tags.json" >/dev/null || fail_read "tag list payload is malformed"

jq -e '
  type == "array" and all(.[]; type == "array") and
  all(.[][];
    type == "object" and
    (.tag_name | type) == "string" and
    (.draft | type) == "boolean")
' "$TMP_DIR/releases.json" >/dev/null || fail_read "Release list payload is malformed"

jq -r '.[][] | [(.ref | sub("^refs/tags/"; "")), .object.type] | @tsv' \
  "$TMP_DIR/tags.json" > "$TMP_DIR/tags.tsv" || fail_read "tag list cannot be normalized"
cut -f1 "$TMP_DIR/tags.tsv" > "$TMP_DIR/tag-names"
jq -r '.[][] | [(.tag_name | @base64), (.draft | tostring)] | @tsv' \
  "$TMP_DIR/releases.json" > "$TMP_DIR/releases.tsv" || fail_read "Release list cannot be normalized"

echo "Active release-sync exemptions for $REPO (default branch: $DEFAULT_BRANCH):"
if [ -s "$TMP_DIR/ignore.active" ]; then
  sed 's/^/  - /' "$TMP_DIR/ignore.active"
else
  echo "  (none)"
fi
echo "Scope: non-v*-named Releases are deliberately out of scope."

is_ignored() {
  grep -Fxq -- "$1" "$TMP_DIR/ignore.active"
}

is_semver() {
  local tag=$1
  local semver_re='^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-((0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)(\.(0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?(\+([0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*))?$'
  [[ "$tag" =~ $semver_re ]]
}

release_state() {
  local tag=$1
  jq -r --arg tag "$tag" '
    [.[][] | select(.tag_name == $tag)] as $matches |
    if any($matches[]; .draft == false) then "published"
    elif any($matches[]; .draft == true) then "draft"
    else "none"
    end
  ' "$TMP_DIR/releases.json"
}

has_draft_release() {
  local tag=$1
  jq -e --arg tag "$tag" 'any(.[][]; .tag_name == $tag and .draft == true)' \
    "$TMP_DIR/releases.json" >/dev/null
}

RED_COUNT=0
WARNING_COUNT=0

while IFS=$'\t' read -r TAG OBJECT_TYPE; do
  [[ "$TAG" == v* ]] || continue
  if is_ignored "$TAG"; then
    continue
  fi

  STATE=$(release_state "$TAG")
  if [ "$STATE" = "draft" ]; then
    echo "RED: draft Release occupies existing tag $TAG; a human must publish or delete the draft."
    RED_COUNT=$((RED_COUNT + 1))
  elif [ "$OBJECT_TYPE" = "tag" ] && is_semver "$TAG" && [ "$STATE" = "none" ]; then
    echo "RED: annotated SemVer tag $TAG has no GitHub Release."
    echo "  remediation: cd <clone> && gh release create $TAG --verify-tag --notes-from-tag"
    RED_COUNT=$((RED_COUNT + 1))
  fi

  if [ "$STATE" = "published" ] && has_draft_release "$TAG"; then
    echo "WARNING: stray draft Release alongside published Release for $TAG"
    WARNING_COUNT=$((WARNING_COUNT + 1))
  fi

  if [ "$OBJECT_TYPE" = "commit" ]; then
    echo "WARNING: $TAG is a lightweight v* legacy tag. Delete + re-tag is destructive and human-only; no runnable command is provided."
    WARNING_COUNT=$((WARNING_COUNT + 1))
  fi

  if ! is_semver "$TAG"; then
    echo "WARNING: $TAG is a non-SemVer v* tag (new pushes are rejected by release-sync)."
    WARNING_COUNT=$((WARNING_COUNT + 1))
  fi
done < "$TMP_DIR/tags.tsv"

while IFS=$'\t' read -r TAG_B64 DRAFT; do
  TAG=$(printf '%s' "$TAG_B64" | base64 --decode) || fail_read "Release tag name cannot be decoded"
  [[ "$TAG" == v* ]] || continue
  if is_ignored "$TAG" || grep -Fxq -- "$TAG" "$TMP_DIR/tag-names"; then
    continue
  fi
  if [ "$DRAFT" = "true" ]; then
    echo "WARNING: draft Release for $TAG is staged for a not-yet-pushed tag."
    WARNING_COUNT=$((WARNING_COUNT + 1))
  else
    echo "RED: published orphan Release $TAG has no matching tag in the full tag list."
    RED_COUNT=$((RED_COUNT + 1))
  fi
done < "$TMP_DIR/releases.tsv"

if [ "$RED_COUNT" -gt 0 ]; then
  echo "RESULT: RED ($RED_COUNT red, $WARNING_COUNT warning)."
  exit 1
fi
if [ "$WARNING_COUNT" -gt 0 ]; then
  echo "RESULT: GREEN with $WARNING_COUNT warning(s); zero RED drift."
  exit 0
fi
echo "RESULT: GREEN; zero RED drift and no warnings."
