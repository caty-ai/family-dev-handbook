> **Machine translation.** The Japanese original ([03-git-protocol.md](../../../docs/03-git-protocol.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# L0 Git Discipline — the layer that prevents physical collisions

Discipline that assumes **multiple sessions / multiple agents touch the same repo concurrently** (agreed 2026-07-03, contractualized 2026-07-21).
Each rule carries a stable rule ID (`L0-1`–`L0-9`). The summary side ([docs/04](04-adoption.md)) references these IDs. The stance to take when verification isn't possible is in [docs/05](05-fail-posture.md).

## L0-1 Check for overlap before starting + declare WIP (Issue = soft lock)

```bash
gh issue list --state open
gh pr list --state open
```

Check for overlap with this, then write a WIP comment on the Issue you're taking ([template](../templates/issue-template.md)).

A WIP declaration only holds as a soft lock **while it carries all four required fields**:
`agent / date / Files to touch / Branch`

A WIP missing a field is invalid as a lock — treat it as scope-unknown and serialize any work that touches that lane ([FP-7](05-fail-posture.md)). Other sessions must not start work that intersects the file set of a valid WIP.

## L0-2 Semantics of declared paths — don't touch what isn't declared (default-deny)

- Paths are **relative to the repo root**. A file name refers to only that file. A directory with a trailing slash covers everything under it
- Globs and negation (`!` exclusion) are forbidden
- A lane declaring `Files to touch: UNKNOWN` is **serial-only** (no concurrency)
- **Files not declared are out of scope** (default-deny). If you find you need to touch one, redeclare your WIP *before* the first write outside your declared scope, and redo the intersection check against concurrent work ([L2-4](01-milestone-loop.md))
- The **effective file set** counts both paths of a rename, deletions, lockfiles, and generated artifacts (for both declaration and intersection checks)
- **Optimistic re-read** — before the first write in a lane, re-read the active WIP set; if anything has changed since the GO decision (WIP added/removed, declaration content changed, redeclared), redo the intersection check

## L0-3 Lock expiry and handoff (stale = 72h / TAKEOVER)

A lock expires when: the branch is merged / deleted, it's stale, there's a `RELEASE` comment, or a `HANDED-OFF` comment.
`RELEASE` / `HANDED-OFF` are **lock lifecycle comments**, not the L1-4 lane state (format in the [template](../templates/issue-template.md)). **Only the lock owner (the WIP's agent) can issue them** — anyone else's issuance is invalid; the only path for someone else to remove a lock is stale + TAKEOVER.

- **stale = 72h with no declaration/update** (measured by GitHub comment timestamps — an update just means writing a new comment. Don't add a separate timestamp field for staleness tracking: don't duplicate platform metadata. The WIP declaration's own `date` field stays required as in L0-1). A lane that expects a long silence may state a longer window **with a reason** at WIP declaration time (this is an exception, not the default. Any later extension must be made visible as a new comment)
- **stale ⇒ owner unknown ⇒ never silently treat as free**. The procedure to take over a stale lane: L0-9 resume checklist + a **`TAKEOVER` comment** quoting the stale WIP + a new WIP declaration
- Adjusting the 72h number happens **only via a PR to this handbook**, backed by operational data (weekly probes) (don't change it unilaterally within a lane). What's non-negotiable is the invariant "never silently liberalize staleness" — not the number itself

HOLD is **not** a lock-expiry trigger (non-terminal — [L1-5](02-issue-loop.md)). A HOLD comment must state how the lock is handled (held until review-by, or released) explicitly — a HOLD silent on the lock is invalid.

## L0-4 1 session = 1 Issue = 1 branch = 1 worktree

**One active writer** per lane / worktree. Don't work in a shared checkout:

```bash
git worktree add ../<repo>-wt/<issue> -b fix/<issue>-<slug> origin/main
```

## L0-5 main is merge-only

No direct pushes to main. Everything goes through PRs.

## L0-6 List touched files in the PR body + reconcile with the diff

Make sure the review can see any drift from the WIP declaration (files added/removed beyond what was declared).
At merge time, cross-check the declared file set against `git diff --stat` — **a file present in the diff but absent from the list is blocking** (part of the [L1-7](02-issue-loop.md) completion-evidence gate).

## L0-7 Merge one at a time

```
git fetch → rebase origin/main → 再検証（typecheck / tests）→ merge
```

After a merge, promptly rebase other open branches. Never merge two at once.
**When an adjacent PR merges, any PR waiting in the queue is obligated to rebase + re-verify (rerun typecheck / tests)** — a clean rebase alone doesn't discharge that obligation.

Scripts and automation that touch git must **make identity / config explicit via env every time, and never read or write the user's git state** (don't depend on global / local config, the real index, or HEAD — use a temporary index if needed). This is the structural generalization of the API-merge incident recorded under the executing account's name.

## L0-8 Keep branches small and short-lived

Long-lived branches turn into rebase hell. A PR held back from merging must state its status via a **HOLD comment** (required fields in [L1-5](02-issue-loop.md)) — don't leave it silently sitting.

## L0-9 Resume checklist — before the first write in a resumed/handed-off lane

For a lane that's been resumed / handed off / taken over, post **one** Issue comment with the results of the following four checks **before the first write** ([template](../templates/issue-template.md)):

1. **Lock** — is it yours, or has it expired per L0-3?
2. **File scope** — is the declared file set still accurate against current origin/main, **and** does it not intersect any currently active WIP/PR (rerun `gh issue list` + `gh pr list --state open`. This item bundles two queries under one gate: "is my declared scope still valid?")
3. **Branch** — does fetch / rebase go through cleanly (rebase before merge if behind)?
4. **Done when** — has it changed since handoff?

If anything doesn't check out: repair / hand off / TAKEOVER / serialize — pick one. **Never silently continue on top of another agent's live lock.**
The checklist is **fixed at these four items**. The posted comment itself is the auditable artifact — don't add more items (checklist fatigue is a named failure mode).

## If something goes wrong

- Conflict appears → don't panic, resolve with rebase. If the resolution is getting large, comment that fact on the Issue and switch to serial
- Need to touch a file outside your declaration → redeclare WIP **before writing**, and redo the intersection check (L0-2)
- Accidentally pushed to main → revert with a revert commit, and record what happened on the Issue
