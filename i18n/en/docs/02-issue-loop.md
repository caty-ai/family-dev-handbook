> **Machine translation.** The Japanese original ([02-issue-loop.md](../../../docs/02-issue-loop.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# L1 Issue Loop — the layer that completes a single piece of work

Each rule carries a stable rule ID (`L1-1` through `L1-11`). The summary side ([docs/04](04-adoption.md)) references these IDs. The stance to take when verification isn't possible is in [docs/05](05-fail-posture.md).

## L1-1 The Issue-first principle

Code changes in the repository **start from a GitHub Issue**. Don't implement without an Issue (exceptions: one-line fixes like typos, non-code md/json/yaml, and scratch work outside git).

Reason: the Issue body + PR diff become the **SoT for handoff across sessions and agents**. No matter which agent picks things up midway, reading the Issue should let them continue.

## L1-2 Three required elements of an Issue body

Use the [template](../templates/issue-template.md).

1. **Purpose (Why)** — why this is being done. The background, and what breaks if it isn't
2. **Done when** — checkbox form. Written so it can be judged mechanically or by hands-on verification, like "tests green" or "confirmed on device"
3. **Predicted files / modules to touch** — the input for L2's parallel-GO decision. Re-declare the confirmed version in a WIP comment when work starts

## The flow from implementation to review to merge

```
Issue 起票 → WIP宣言（L0-1）→ worktree で実装 → テスト/lint green
→ クロスレビュー → 指摘対応 → PR（完了記録 = L1-7 を本文に）
→ merge → Issue close → 安定点で git tag
```

## L1-3 Principles of cross-review

- **No self-approve** — don't merge on the implementer's own approval alone
- **A review that clears a merge must come from a different model or agent than the implementer** (e.g., Claude implements → GPT/GLM reviews, Codex implements → Claude reviews). Even the same model is valid for merge if it's a **different agent**. The same model and the same agent is not sufficient for merge even across different sessions — a different session is only enough for checkpoints other than merge
- The default is for the round-1 reviewer to be the reviewer who sees it through to completion. If a handoff happens, it must be declared, and the incoming reviewer must **re-review the whole of the current candidate** (don't merge on a partial review stitched onto a previous one)
- Loop the implementer → reviewer cycle until blocking findings reach 0
- Review lens: correctness / boundaries (whether out-of-scope files were touched) / test adequacy / revertability

## L1-4 Lane state — a closed vocabulary of 5 states

Lane state is declared via a labeled comment on the owning Issue. **The Issue is the source of truth for lane state** (a pending PR points back to the Issue):

`WIP / HOLD / MERGED / SUPERSEDED / ABANDONED`

- **WIP is a state that must be explicitly declared — it is not the default**
- `STUCK` is **not** a sixth state — it's a trigger condition, and the only legitimate way out is a valid HOLD (or escalation to a human)
- A lane whose state is missing, unknown, or malformed is treated as **inactive (HOLD-equivalent posture: no writes) and awaiting state repair**. Don't count this lane as "available" in a GO decision — work that could intersect with its declared scope stays serialized until repair ([FP-1](05-fail-posture.md)). Don't fabricate a valid HOLD record from malformed input (a HOLD's required fields can't be manufactured from malformed input) — the next agent to touch the lane has repairing the state, not writing, as its first obligation ([FP-7](05-fail-posture.md))
- **A termination / blocker declaration takes priority over pressure to continue.** If a blocker appears within the same update, that update's claim of completion is void

## L1-5 HOLD's required fields

HOLD is **resumable, non-terminal**. It's only valid when all of the following are present:

`owner / reason / review-by / lock disposition (hold the lock until review-by, or release it) / remaining work or successor`

- **A HOLD that's silent about lock disposition is invalid** — because either reading (ghost lock, or double-write) becomes a collision path
- Passing review-by triggers a **visible review obligation** (resurfaced by the weekly ops probe). There's no auto-release or auto-ABANDONED
- `retained until review-by` does **not** mean "auto-released at review-by" — review-by is the date the review obligation kicks in; the lock stays held until an explicit action (a HOLD update, RELEASE, or the TAKEOVER procedure after going stale)

## L1-6 Retries are finite

Retries are finite. Once exhausted, declare **HOLD / ABANDONED with evidence** — exhaustion never counts as success (HOLD if you intend to continue, ABANDONED if you're cutting it off. The exit via a STUCK trigger follows L1-4: a valid HOLD or escalation to a human).

> Footnote (outside the contract body — a candidate policy still open for tuning): the specific trigger "two consecutive identical failures (same review finding or same CI signature) ⇒ STUCK" is a single reviewer's proposal and is not part of this contract. The default is left to maintainer judgment or per-repo choice.

## L1-7 The completion-evidence merge gate

A PR may only be merged when a **completion record** ([template](../templates/issue-template.md)) satisfying the following is present in the PR body:

1. **Map every Done-when item to `PASS` / `FAIL` / `N/A` with a reason** — a command having "run" is not a PASS. A FAIL on a required item, or an N/A without a reason, blocks the merge
2. **Persistent evidence with a terminal result** for each item (command or manual procedure + observed outcome + date). **The inline excerpt is authoritative** — the terminal result must be readable from the record alone. URLs to CI or external logs are convenience pointers; link-only evidence doesn't qualify
3. State the **candidate commit SHA** explicitly — it must match the PR head at review time (if it changes before merge, that's an L1-8 replacement record)
4. Cross-check the declared file set against `git diff --stat origin/main...<candidate SHA>` (a file in the diff but not in the list is blocking — [L0-6](03-git-protocol.md))
5. Link the identities of the implementer and reviewer, confirming **the model or agent differs** (L1-3)

**Evidence exists before the claim does.** Success that exists only locally is not completion.

## L1-8 Corrections go through a superseding record

A correction to a completion record means **publishing a full replacement record and reopening the review**. No silent edits.

## L1-9 Upstream cross-review — the upstream extension of no-self-approve

- **Epics, architecture changes, and requirements definitions** (the heavy side of [L2-1](01-milestone-loop.md)) must pass a cross-review by distinct models (seats from L1-10, seat counts from L1-11) **before implementation starts**. Timing: this can happen "after the EPIC Issue is filed, but no later than before the first child Issue's implementation starts" — a single review ([the same clock as E-6①](06-epic-lane.md) — don't let "before filing" and "before implementation starts" coexist as two competing readings). Because drift in the initial direction propagates downstream, review should be heaviest upstream
- Applies **only** to the heavy side: a single Issue (bug fix, single feature) doesn't carry an upstream review — implementation review (L1-3 / L1-11) alone still applies as before. Widening this would resurrect per-Issue review waits and contradict the speed objective ([docs/06](06-epic-lane.md))
- If the upstream review's execution **can't be verified, don't start implementation** (fail-closed — the same direction as halting writes. The record is linked from the EPIC Issue — the kickoff section of the [template](../templates/epic-template.md))

## L1-10 The top-level principle of distinct review seats

- Review seats must be chosen from **models that differ from each other**, and **differ from the implementation writer** ("N distinct seats" means the N seats are mutually distinct — N separate agents on the same model are not N distinct seats)
- **Whoever designed or implemented what's under review doesn't count as a seat** (this includes the orchestrator — a seat reviewing its own design runs against the intent of L1-3 / FP-8). Same model, different agent is valid as a minimum condition for merge per L1-3, but doesn't count toward L1-11's seat count (the only exception is L1-11's downgrade procedure)
- Seats should be filled with **the top-tier model launchable in that household**. Enforcement: each household maintains a **roster of eligible review-seat models** in its local config (CLAUDE.md / AGENTS.md, etc.), and the handbook requires: ① the roster exists ② nothing outside the roster is seated ③ roster updates are visible. The handbook doesn't specify which models (by name) belong on the roster — models change, so the source of truth shouldn't have to be chased through PRs
- Review records must always retain **requested / actual model** (for auditability — evidence exists before the claim does)

## L1-11 Seat-count scale

The seat counts in this table apply to **implementation review that clears a merge** and to **upstream review (L1-9)** (L1-3 is the minimum identity condition; this table sets the seat count — the two don't conflict). The child-to-epic gate within an Epic also uses this table, keyed to **the child's weight** ([E-6②](06-epic-lane.md) — a child touching a high-risk area gets priority for 5 seats).

| Target | Seat count |
|---|---|
| S / M (local, single feature) | 2 distinct seats |
| L / H (multiple modules, boundary change, new feature) | 3 distinct seats |
| **High-risk areas** (defined at [the top of docs/06](06-epic-lane.md) — a single definition, takes priority over size classification) | 5 distinct seats |
| **Upstream review** (L1-9) for Epics, architecture, requirements definitions | L/H staffing before implementation starts (5 seats if it includes a high-risk area) |

- An absence is backfilled with **another distinct seat**
- A household that can't physically secure distinct seats (fewer launchable model families than the seat count) can use the **downgrade procedure**: a seat filled by the same model / a different agent, **plus explicit owner (human) approval**, plus the downgrade noted in the review record. An unapproved downgrade counts the same as failing to meet the seat count
- If backfilling and downgrading still don't meet the count, stop at **SEAT-WAIT** (a waiting state prior to review launch. This is a separate term from L1-4's HOLD lane state, and L1-5's five required fields don't apply — the distinction exists so the weekly probe doesn't misdetect it as a HOLD). Make SEAT-WAIT visible via a comment on the owning Issue, stating three things: **owner / the seat shortfall / a retry-by date** (a SEAT-WAIT missing any of the three is invalid). A SEAT-WAIT comment counts as an activity update under [L0-3](03-git-protocol.md) — going stale → TAKEOVER on a seat-short lane doesn't add seats, so this surfaces the root cause instead of just advancing the clock
- Adjusting the seat-count numbers can only be done via a PR to the handbook (the same treatment as the 72h in [L0-3](03-git-protocol.md))

## Definition of done

- Tests and lint pass
- The PR carrying an L1-7 completion record is merged, and the Issue is closed
- **The online repo is the current source of truth** (don't end in a state where results exist only locally)
- When work spans multiple sessions, the entry point for continuing (what to do next) is left in an Issue comment or a handoff
