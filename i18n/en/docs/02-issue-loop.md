> **Machine translation.** The Japanese original ([02-issue-loop.md](../../../docs/02-issue-loop.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# L1 Issue Loop — The Layer That Completes One Piece of Work

Each rule carries a stable rule ID (`L1-1` through `L1-11`). The summary side ([docs/04](04-adoption.md)) references these IDs. The stance to take when verification isn't possible is in [docs/05](05-fail-posture.md).

## L1-1 The Issue-First Principle

Code changes in a repository start from a **GitHub Issue**. Don't implement without an Issue (exceptions: one-line fixes like typos, non-code md/json/yaml, and scratch work outside git).

Reason: the Issue body + PR diff become the **source of truth for handoff across sessions and agents**. Any agent that picks up the work partway through should be able to continue just by reading the Issue.

## L1-2 The Three Required Elements of an Issue Body

Use the [template](../templates/issue-template.md).

1. **Purpose / Why** — why this is being done. Background, and what breaks if it isn't
2. **Done when** — in checkbox form. Written so it can be judged mechanically or by hands-on verification, e.g. "tests green," "verified on device"
3. **Predicted files / modules to touch** — input to L2's parallel-GO decision. Redeclare the confirmed version in a WIP comment when work starts

## The Implement → Review → Merge Flow

```
Issue 起票 → WIP宣言（L0-1）→ worktree で実装 → テスト/lint green
→ クロスレビュー → 指摘対応 → PR（完了記録 = L1-7 を本文に）
→ merge → Issue close → 安定点で git tag
```

## L1-3 Principles of Cross-Review

- **No self-approval** — don't merge on the implementer's approval alone
- **The reviewer who clears a merge must be a different model or agent from the implementer** (e.g. Claude implements → GPT/GLM reviews, Codex implements → Claude reviews). Same model but a **different agent** is valid for merge. The same model and the same agent is insufficient for merge even across different sessions — a different session is only enough for checkpoints other than merge
- By default, the round-1 reviewer stays the reviewer through completion. If a handoff happens, it must be declared, and the incoming reviewer must **re-review the current candidate in full** (don't merge on a partial review stitched together with another)
- Loop implementer → reviewer until blocking findings reach zero
- Review lens: correctness / boundaries (are out-of-scope files being touched?) / test adequacy / revertability

## L1-4 Lane State — A Closed Vocabulary of 5 States

Lane state is declared via a labeled comment on the owning Issue. **The Issue is the source of truth for lane state** (a pending PR points back to the Issue):

`WIP / HOLD / MERGED / SUPERSEDED / ABANDONED`

- **WIP is a state you declare explicitly — it is not the default**
- `STUCK` is **not** a sixth state — it's a trigger condition, and the only legitimate exit is a valid HOLD (or escalation to a human)
- A lane with missing, unknown, or malformed state is treated as **inactive (HOLD-equivalent posture: no writes) pending state repair**. Don't count this lane as "available" in a GO decision — any work that could intersect its declared scope stays serialized until repair ([FP-1](05-fail-posture.md)). Don't fabricate a valid HOLD record out of malformed input (HOLD's required fields can't be manufactured from malformed input) — the first duty of the next agent to touch it is **repairing the state**, not writing ([FP-7](05-fail-posture.md))
- **Termination / blocker declarations take priority over pressure to continue**. If a blocker appears within the same update, that update's completion claim is void

## L1-5 HOLD's Required Fields

HOLD is **resumable, non-terminal**. It's only valid when all of the following are present:

`owner / reason / review-by / lock disposition (retain the lock until review-by, or release it) / remaining work or successor`

- **A HOLD silent on lock disposition is invalid** — because both readings (ghost lock / double-write) become collision paths
- Passing review-by creates a **visible review obligation** (it resurfaces via the weekly ops probe). There's no auto-release and no auto-ABANDONED
- `retained until review-by` does **not** mean "auto-released at review-by" — review-by is the date the review obligation kicks in; the lock stays held until an explicit action (a HOLD update, RELEASE, or the TAKEOVER procedure after going stale)

## L1-6 Retries Are Finite

Retries are capped. Once exhausted, declare **HOLD / ABANDONED with evidence** — exhausting retries never counts as success (HOLD if you intend to continue, ABANDONED if you're cutting it off. Exits via the STUCK trigger follow L1-4: a valid HOLD or escalation to a human).

> Footnote (outside the contract body — a candidate tunable policy): the specific trigger "same failure twice in a row (same review finding or same CI signature) ⇒ STUCK" is a single reviewer's proposal and is not part of this contract. The default is left to maintainer judgment or per-repo choice.

## L1-7 The Completion-Evidence Merge Gate

A PR may only be merged when the PR body contains a **completion record** ([template](../templates/issue-template.md)) satisfying all of the following:

1. **Map every Done-when item to `PASS` / `FAIL` / `N/A` with a reason** — a command having "run" is not a PASS. A FAIL on a required item, or an N/A without a reason, blocks the merge
2. Each item has **persistent evidence with a terminal result** (command or manual procedure + observed outcome + date). **The inline excerpt is authoritative** — the terminal result must be readable from the record alone. A URL to CI or an external log is a convenience pointer; a link alone is not adequate evidence
3. State the **candidate commit SHA** explicitly — it must match the PR head at review time (if it changes before merge, that's a superseding record per L1-8)
4. Cross-check the declared file set against `git diff --stat origin/main...<candidate-SHA>` (a file in the diff but not in the list is blocking — [L0-6](03-git-protocol.md))
5. Link the identities of implementer and reviewer, and confirm **the model or agent differs** (L1-3)

**Evidence exists before the claim is made.** Success that exists only locally is not completion.

## L1-8 Corrections Go Through a Superseding Record

A correction to a completion record means **publishing a full replacement record and reopening review**. No silent edits.

## L1-9 Upstream Heterogeneous Review — Extending No-Self-Approval Upstream

- **Sizes L / H / Epic** (= the heavy side of the size classification in [L2-1](01-milestone-loop.md); architecture changes and requirements definition fall here too) must pass heterogeneous cross-review (L1-10's seats, L1-11's seat counts) **before implementation starts**. The source of truth for size definitions is L2-1 — don't copy it here. For an Epic, the timing is one pass, either "after the EPIC Issue is filed, or at the latest before the first child Issue's implementation starts" (same clock as [E-6①](06-epic-lane.md) — don't let "before filing" and "before implementation starts" coexist as two different readings). Since drift in the initial direction propagates downstream, review should be heaviest upstream
- Applies **only** to the heavy side: single S / M Issues (bug fixes, single features) don't carry an upstream review requirement — just the usual implementation review (L1-3 / L1-11) as before. Widening this scope would bring back per-Issue review waits, contradicting the speed goal ([docs/06](06-epic-lane.md))
- **If upstream review can't be verified as having happened, don't start implementation** (fail-closed — the same direction as halting writes. The record is linked from the EPIC Issue — the kickoff section of the [template](../templates/epic-template.md). For a standalone L / H, link it from the owning Issue)

## L1-10 The Principle of Heterogeneous, Top-Tier Review Seats

- Review seats are chosen from **mutually distinct models**, and distinct from the implementation writer's model ("N heterogeneous seats" means the N seats are mutually heterogeneous — N different agents on the same model is not N heterogeneous seats)
- **Whoever designed or implemented what's under review does not count as a seat** (including the orchestrator — a seat that reviews its own design runs against the intent of L1-3 / FP-8). Same model, different agent is valid as the minimum bar for merge per L1-3, but doesn't count toward L1-11's seat count (the only exception is L1-11's own demotion procedure)
- Seats are filled with **the top-tier class of model launchable in that household**. Enforcement: each household maintains a **roster of review-seat-eligible models** in local config (CLAUDE.md / AGENTS.md, etc.), and the handbook requires ① the roster exists, ② nothing outside the roster is seated, ③ roster updates are visible. Which models (by actual name) go on the roster is not written into the handbook — models turn over, so the source of truth shouldn't have to be chased through handbook PRs
- Review records must always keep **requested / actual model** on file (auditability — evidence exists before the claim)

## L1-11 Seat-Count Scaling

The seat counts in this table apply to **implementation review that clears a merge** and to **upstream review (L1-9)** (L1-3 is the minimum identity condition; this table sets the seat count — the two don't conflict). The child-to-epic gate inside an Epic also looks up this table by **the child's weight** ([E-6②](06-epic-lane.md) — children touching high-risk areas default to 5 seats).

| Target | Seat count |
|---|---|
| S / M (local, single feature) | 2 heterogeneous seats |
| L / H (multiple modules, boundary changes, new features) | 3 heterogeneous seats |
| **High-risk areas** (defined at the [top of docs/06](06-epic-lane.md); a single definition; takes priority over size classification) | 5 heterogeneous seats |
| **Upstream review** (L1-9) for Epics, architecture, and requirements definition | L/H staffing before implementation starts (5 seats if it includes a high-risk area) |

- Fill an absence with **another heterogeneous seat**
- A household that physically cannot secure heterogeneous seats (fewer launchable model families than seats required) can use the **demotion procedure**: a seat filled by the same model with a different agent, **plus explicit approval from the owner (a human)**, plus the demotion noted in the review record. An unapproved demotion counts the same as failing to meet the seat count
- If still short after backfill and demotion, stop at **SEAT-WAIT** (a waiting state prior to review being launched. Distinct from L1-4's HOLD lane state — L1-5's 5 required fields don't apply, so the weekly probe doesn't misclassify it as a HOLD). Make SEAT-WAIT visible via a comment on the owning Issue, stating three things: **owner / seats short / retry-by date** (a SEAT-WAIT missing any of the three is invalid). A SEAT-WAIT comment counts as an activity update under [L0-3](03-git-protocol.md) — letting a seat-short lane go stale → TAKEOVER doesn't add seats, so this surfaces the root cause instead of just advancing the clock
- Adjust the seat-count numbers only through a handbook PR (same treatment as the 72h in [L0-3](03-git-protocol.md))

## Definition of Done

- Tests and lint pass
- A PR carrying an L1-7 completion record has been merged, and the Issue is closed
- **The online repo is the up-to-date source of truth** (it doesn't end with results existing only locally)
- When work spans multiple sessions, the entry point for continuing (what to do next) is left in an Issue comment or a handoff
