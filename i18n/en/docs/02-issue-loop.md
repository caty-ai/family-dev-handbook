> **Machine translation.** The Japanese original ([02-issue-loop.md](../../../docs/02-issue-loop.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# L1 Issue Loop — the layer that completes a single piece of work

Each rule carries a stable rule ID (`L1-1` through `L1-11`). The summary side ([docs/04](04-adoption.md)) refers back to these IDs. The stance to take when something can't be verified is in [docs/05](05-fail-posture.md).

## L1-1 The Issue-first principle

Code changes in a repository start from a **GitHub Issue**. Don't implement without one (exceptions: one-line fixes like typos, non-code md/json/yaml, and scratch work outside git).

Why: the Issue body plus the PR diff becomes the **source of truth for handoff across sessions and agents**. No matter which agent picks it up midway, reading the Issue should let them continue.

## L1-2 The three required parts of an Issue body

Use the [template](../templates/issue-template.md).

1. **Purpose (Why)** — why this is being done. The background, and what breaks if it isn't
2. **Done when** — as checkboxes. Written so it can be judged mechanically or by hands-on check, like "tests green" or "verified on device"
3. **Predicted files / modules to touch** — the input for L2's parallel-GO judgment. Re-declare the finalized version in the WIP comment when work starts

## The implement → review → merge flow

```
Issue 起票 → WIP宣言（L0-1）→ worktree で実装 → テスト/lint green
→ クロスレビュー → 指摘対応 → PR（完了記録 = L1-7 を本文に）
→ merge → Issue close → 安定点で git tag
```

## L1-3 Principles of cross-review

- **No self-approval** — don't merge on the implementer's own approval alone
- **The review that clears a merge must come from a different model or agent than the implementer** (e.g., Claude implements → GPT/GLM reviews, Codex implements → Claude reviews). Even the same model is fine for merge if it's a **different agent**. The same model and the same agent is not sufficient for merge even across different sessions — a different session is only enough for checkpoints other than merge
- The Round-1 reviewer is the default full-run reviewer. If the reviewer changes, that change must be declared, and the replacement reviewer must **re-review the entire current candidate** (don't merge on a partial review stitched together)
- Loop implementer → reviewer until blocking findings reach 0
- Review angles: correctness / boundaries (are out-of-scope files being touched?) / test adequacy / revertability

## L1-4 Lane states — a closed vocabulary of 5 states

Lane state is declared via a labeled comment on the owning Issue. **The Issue is the source of truth for lane state** (a pending PR points back to the Issue):

`WIP / HOLD / MERGED / SUPERSEDED / ABANDONED`

- **WIP is a state you declare explicitly — it is not the default**
- `STUCK` is **not** a sixth state — it's a trigger condition, and the only legal way out is a valid HOLD (or escalation to a human)
- A lane with a missing, unknown, or malformed state is **treated as inactive (HOLD-equivalent stance: no writes) pending state repair**. Don't count this lane as "available" in a GO judgment — work that could intersect the declared scope stays serial until repair ([FP-1](05-fail-posture.md)). Don't fabricate a valid HOLD record from malformed input (HOLD's required fields can't be manufactured from malformed input) — the next agent to touch this lane's first obligation is **repairing the state**, not writing ([FP-7](05-fail-posture.md))
- **A termination / blocker declaration outweighs pressure to continue**. If a blocker appears within the same update, that update's completion claim is void

## L1-5 HOLD's required fields

HOLD is **resumable, non-terminal**. It's only valid when it carries all of the following:

`owner / reason / review-by / lock disposition (hold the lock until review-by, or release it) / remaining work or successor`

- **A HOLD silent on lock disposition is invalid** — because either reading (ghost lock or double-write) becomes a collision path
- Passing review-by creates a **visible review obligation** (it resurfaces via the weekly ops probe). There is no auto-release or auto-ABANDONED
- `retained until review-by` does **not** mean "auto-released at review-by" — review-by is the date the review obligation kicks in; the lock stays held until an explicit action (a HOLD update, RELEASE, or the TAKEOVER procedure after going stale)

## L1-6 Retries are finite

Retries are capped. Once exhausted, declare a **HOLD / ABANDONED with evidence** — exhausting retries never counts as success (HOLD if continuation is intended, ABANDONED if cutting it off; an exit via the STUCK trigger follows L1-4 — a valid HOLD, or escalation to a human).

> Footnote (outside the contract body — a tunable policy candidate): the specific trigger "two consecutive identical failures (same review finding or same CI signature) ⇒ STUCK" is a single reviewer's proposal and is not part of this contract. The default is left to maintainer judgment or per-repo choice.

## L1-7 The completion-evidence merge gate

A PR may only be merged when a **completion record** ([template](../templates/issue-template.md)) meeting the following is present in the PR body:

1. **Map every Done-when item to `PASS` / `FAIL` / `N/A` with a reason** — a command having "run" is not the same as PASS. A FAIL on a required item, or an N/A without a reason, blocks the merge
2. Each item needs **durable evidence with a terminal result** (the command or manual procedure + observed outcome + date). **The inline excerpt is authoritative** — the terminal result must be readable from the record alone. URLs to CI or external logs are convenience pointers; link-only evidence doesn't qualify
3. State the **candidate commit SHA** explicitly — it must match the PR head at review time (if it changes before merge, that's a superseding record per L1-8)
4. Cross-check the declared file set against `git diff --stat origin/main...<candidate SHA>` (a file in the diff but not in the list is blocking — [L0-6](03-git-protocol.md))
5. Link the identities of implementer and reviewer, confirming **the model or agent differs** (L1-3)
6. **State the CI status** — don't merge while it's red. The sole exception condition for a known, unrelated red is [T-4](10-test-ci-baseline.md)

**Evidence exists before the claim does.** Success that only exists locally is not completion.

## L1-8 Corrections go through a superseding record

Correcting a completion record means **publishing a full replacement record and reopening the review**. No silent edits.

## L1-9 Upstream heterogeneous review — the upstream extension of no-self-approval

- **Size L / H / Epic** (= the heavy side of [L2-1](01-milestone-loop.md)'s size classification criteria; architecture changes and requirements definition fall here too) must pass heterogeneous cross-review (L1-10's seats, L1-11's seat counts) **before implementation starts**. The source of truth for the size definition is L2-1 — it isn't copied here. For Epics, the timing is "either after the EPIC Issue is filed, or at the latest before the first child Issue's implementation starts" — one pass ([E-6①](06-epic-lane.md), the same clock — don't let "before filing" and "before implementation starts" coexist as two readings). Since drift in the initial direction propagates downstream, review gets heavier the further upstream it sits
- Applies **only** to the heavy side: single S/M Issues (bug fixes, single features) don't carry an upstream review requirement — just the usual implementation review (L1-3 / L1-11) as before. Widening this here would bring back per-Issue review waits and conflict with the speed goal ([docs/06](06-epic-lane.md))
- If **whether the upstream review happened can't be verified, don't start implementation** (fail-closed — the same direction as halting writes. The record links from the EPIC Issue — the kickoff section of the [template](../templates/epic-template.md). For standalone L/H Issues, it links from the owning Issue)

## L1-10 The principle of heterogeneous, top-tier review seats

- Review seats must be drawn from **mutually different models**, and different from **the implementation writer's model** ("N heterogeneous seats" means the N seats are mutually heterogeneous — N different agents on the same model is not N heterogeneous seats)
- **Whoever designed or implemented what's under review doesn't count toward a seat** (including the orchestrator — a seat reviewing its own design defeats the point of L1-3 / FP-8). Same model, different agent is valid as the minimum bar for merge per L1-3, but doesn't count toward L1-11's seat total (the only exception is L1-11's downgrade procedure)
- Seats should be filled with **the top-tier class of model that household can launch**. Enforcement: each household maintains a **seat-eligible model roster** in local config (CLAUDE.md / AGENTS.md, etc.), and the handbook requires ① that a roster exists, ② that nothing outside the roster is seated, and ③ that roster updates are visible. Which models (by name) go on the roster is not written into the handbook — models change, so the source of truth shouldn't be chased through a PR
- **The named-catalog clause**: a family-shared **catalog of real model names is a data layer** and lives outside the handbook (as a consequence of the previous bullet — "real names are not written into the handbook" — the separation is the only lawful shape, not merely a permitted one). The catalog is **non-normative** (a member may override it with a recorded reason; an unrecorded deviation is non-conformant) — "**the catalog can neither legalise a seat the law forbids nor make usable a model the member cannot verify live; eligibility is won by the member's configuration, seat counts and constraints are won by the handbook.**" The catalog names no panels and carries no availability fields. The existence of a shared catalog weakens none of this clause's roster requirements, seat rules, or record requirements, nor L1-11's seat counts, downgrade procedure, or SEAT-WAIT vocabulary
- **Seat lineage and correlated-seats**: what "heterogeneous" demands in this clause is a **different model**, not a different lineage — lineage is governed by this item. **On machine-selected paths (draws, substitutions), pairwise-distinct lineage or a recorded exception** is required. Same-lineage seats on an owner-named fixed panel are legal only with a **recorded correlated-seats flag**. The machine-path "recorded exception" and the named-panel correlated-seats flag are **the same exception record**, carrying the 6 fields `scope / pair / reason / approved_by / date / writer condition` (a flag missing fields is invalid). An exception is valid only within its recorded `scope`. It lives in each household's local config (it contains real names, so it is not written into the handbook). **A review record that applies correlated-seats must state so explicitly — an undisclosed same-lineage seating counts the same as an unmet seat count.** This item is distinct from L1-11's downgrade procedure (same model, different agent, plus owner approval) — that one handles seat shortage, this one handles lineage overlap
- Review records must always retain **requested / actual model** (auditability — evidence exists before the claim does)

## L1-11 Seat-count scaling

The seat counts in this table apply to **implementation review that clears a merge** and to **upstream review (L1-9)** (L1-3 is the identity minimum; this table sets the seat count — the two don't conflict). The child→epic gate within an Epic also looks up this table **by the child's weight** ([E-6②](06-epic-lane.md) — a child touching a high-risk area gets priority for 5 seats).

| Target | Seats |
|---|---|
| S / M (local, single feature) | 3 heterogeneous seats (effective per member (household) — see below) |
| L / H (multiple modules, boundary changes, new features) | 3 heterogeneous seats |
| **High-risk areas** (defined at [the top of docs/06](06-epic-lane.md) — a single definition; takes priority over size classification) | 5 heterogeneous seats |
| **Upstream review** (L1-9) for size L / H / Epic | L/H setup before implementation starts (5 seats if it includes a high-risk area) |

- **The S/M=3 floor takes effect per member (household)**: the effect data (3 fields: `owner / effective date or stand-up completion condition / LC-1 trigger`) is held by **one pinned Issue per household in that household's canonical handbook repo (the fork, if forked)**. A household before its effective date is legal at the old floor (2 heterogeneous seats) — the enforcement gap is treated as a "schedule", not a "violation" (don't publish, with immediate effect for everyone, a law that many households cannot satisfy on day one — [R-6](09-rejection-rubric.md): a law everyone breaks from day one cannot be promoted to a fail-closed check). The evidence of "stand-up completion" is an **observable event** (one recorded fresh-context / read-only real review, with requested/actual model), not a judgment call. **A household with no 3-field pinned Issue, or with missing fields, cannot claim "pre-effective" status** ([FP-7](05-fail-posture.md) — a missing record is interpreted in the authority-shrinking direction) — the table's floor (3 heterogeneous seats) applies (the old floor of 2 is a grace claimable only by pointing at recorded effect data)
- A no-show is backfilled with **another heterogeneous seat**
- A household that can't physically secure heterogeneous seats (fewer launchable model families than seats) can use the **downgrade procedure**: a seat filled by the same model with a different agent, **plus explicit approval from the owner (a human)**, plus the downgrade noted in the review record. An unapproved downgrade counts the same as an unmet seat count
- If backfilling or downgrading still falls short, stop at **SEAT-WAIT** (a waiting state before review starts — a distinct term from L1-4's HOLD lane state; L1-5's 5 required fields don't apply, to keep the weekly probe from misdetecting it as a HOLD). Make SEAT-WAIT visible via a comment on the owning Issue, stating three things: **owner / which seats are missing / a retry-by date** (a SEAT-WAIT missing any of the three is invalid). A SEAT-WAIT comment counts as an activity update under [L0-3](03-git-protocol.md) — letting a seat-short lane go stale → TAKEOVER doesn't create more seats, so this surfaces the root cause instead of just advancing the clock
- **SEAT-WAIT applies to lanes only**: never apply an open-ended SEAT-WAIT to a member (household) — a wait with no owning Issue and no retry-by date cannot satisfy the three points above and escapes visibility. A household-level "not yet able to satisfy" is expressed through the per-member effect data above
- Adjusting the seat-count numbers can only be done via a PR to the handbook (same treatment as [L0-3](03-git-protocol.md)'s 72h)

## Definition of done

- Tests and lint pass (the sole explicit exception is [T-4](10-test-ci-baseline.md))
- The PR carrying an L1-7 completion record is merged, and the Issue is closed
- **The online repo is the up-to-date source of truth** (it doesn't end with results that only exist locally)
- If work spans multiple sessions, the entry point for continuing (what to do next) is left in an Issue comment or a handoff
