> **Machine translation.** The Japanese original ([03-git-protocol.md](../../../docs/03-git-protocol.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# L0 Git Discipline — The Layer That Prevents Physical Collisions

Discipline for the premise that **multiple sessions / multiple agents touch the same repo concurrently** (agreed 2026-07-03, contracted 2026-07-21).
Each rule carries a stable rule ID (`L0-1` through `L0-9`). The summary side ([docs/04](04-adoption.md)) references these IDs. For the stance to take when something can't be verified, see [docs/05](05-fail-posture.md).

## L0-1 Check for overlap before starting + declare WIP (Issue = soft lock)

```bash
gh issue list --state open
gh pr list --state open
```

Check for overlap with this, then write a WIP comment on the Issue you're taking ([template](../templates/issue-template.md)).

A WIP declaration only holds as a soft lock **while it carries all 4 required fields**:
`agent / date / Files to touch / Branch`

A WIP missing a field is not a valid lock — treat it as scope-unknown and serialize any work that touches that lane ([FP-7](05-fail-posture.md)). Other sessions must not start work that intersects a valid WIP's file set.

## L0-2 Semantics of declared paths — don't touch what isn't declared (default-deny)

- Paths are **relative to the repo root**. A filename refers to that file only. A directory with a trailing slash covers everything under it
- Globs and negation (`!` exclusion) are prohibited
- A lane declared `Files to touch: UNKNOWN` is **serial-only** (no concurrency)
- **Undeclared files are out of scope** (default-deny). If you need to touch one, redeclare your WIP *before* the first write outside your declared scope, and redo the intersection check against concurrent lanes ([L2-4](01-milestone-loop.md))
- The **effective file set** includes both paths of a rename, deletions, lockfiles, and generated artifacts (for both declaration and intersection checks)
- **Optimistic re-read** — before the first write in a lane, re-read the active WIP set; if anything changed since the GO decision (WIP added/removed, declaration content changed, redeclaration), redo the intersection check

## L0-3 Lock expiry and handoff (stale = 72h / TAKEOVER)

A lock expires when: its branch is merged/deleted, it goes stale, a `RELEASE` comment is posted, or a `HANDED-OFF` comment is posted.
`RELEASE` / `HANDED-OFF` are **lock lifecycle comments**, not L1-4 lane states (format: [template](../templates/issue-template.md)). **Only the lock owner (the WIP's agent) may issue them** — issuance by anyone else is invalid; the only path for someone else to release a lock is stale + TAKEOVER.

- **stale = 72h with no declaration/update** (measured by GitHub comment timestamps — an update just means posting a new comment. Don't add a custom timestamp field for staleness tracking: don't duplicate platform metadata. The WIP declaration's own `date` field stays required per L0-1). Lanes expecting a long silence may state a longer window **with a reason** at WIP declaration time (an exception, not the default; extending after the fact must be done visibly, as a new comment)
- **stale ⇒ ownership unknown ⇒ never silently treat as free**. The procedure for taking over a stale lane: L0-9 resumption checklist + a **`TAKEOVER` comment** quoting the stale WIP + a new WIP declaration
- Adjusting the 72h figure happens **only via a PR to this handbook**, backed by operational data (weekly probes) (don't change it unilaterally within a lane). What's non-negotiable is the invariant itself — "never silently liberalize staleness" — not the number

HOLD is **not** a lock-expiry event (non-terminal — [L1-5](02-issue-loop.md)). A HOLD comment must state explicitly how the lock is handled (held until review-by, or released) — a HOLD silent on the lock is invalid.

## L0-4 1 session = 1 Issue = 1 branch = 1 worktree

**One** active writer per lane / worktree. Don't work in a shared checkout:

```bash
git worktree add ../<repo>-wt/<issue> -b fix/<issue>-<slug> origin/main
```

## L0-5 main is merge-only

No direct pushes to main. Everything goes through a PR.

## L0-6 List touched files in the PR body + reconcile against the diff

Make sure the diff from the WIP declaration (files added/dropped beyond what was declared) is visible in review.
At merge time, reconcile the declared file set against `git diff --stat` — **a file present in the diff but missing from the list is blocking** (part of the [L1-7](02-issue-loop.md) completion-evidence gate).

## L0-7 Merge one at a time

```
git fetch → rebase origin/main → re-verify (typecheck / tests) → merge
```

After merging, rebase other open branches promptly. Never merge two at once.
**When an adjacent PR merges, a PR waiting in queue is obligated to rebase + re-verify (rerun typecheck / tests)** — a clean rebase alone doesn't discharge that obligation.

## L0-8 Keep branches small and short-lived

Long-lived branches turn into rebase hell. A PR held from merging must state its status via a **HOLD comment** (required fields: [L1-5](02-issue-loop.md)) — don't leave it silently sitting.

## L0-9 Resumption checklist — before the first write in a resumed/handed-off lane

For a resumed / handed-off / TAKEOVER lane, post **one** Issue comment confirming the following 4 checks **before the first write** ([template](../templates/issue-template.md)):

1. **Lock** — is it yours, or has it expired per L0-3?
2. **File scope** — is the declared file set still accurate against current origin/main, **and** non-intersecting with all currently active WIPs/PRs? (rerun `gh issue list` + `gh pr list --state open`. This one item bundles two lookups under a single gate: "is my declared scope still valid?")
3. **branch** — does fetch/rebase go through cleanly? (rebase before merging if behind)
4. **Done when** — unchanged since handoff?

If anything doesn't match: repair / handoff / TAKEOVER / or serialize — pick one. **Never silently continue on top of another agent's live lock.**
The checklist is **fixed at these 4 items**. The posted comment itself is the auditable artifact — don't add more items (checklist fatigue is a named failure mode).

## When something goes wrong

- A conflict appears → resolve it calmly with rebase. If the resolution grows large, comment that fact on the Issue and switch to serial
- You need to touch an undeclared file → redeclare your WIP **before writing** and redo the intersection check (L0-2)
- You accidentally pushed to main → revert with a revert commit and record what happened on the Issue
