> **Machine translation.** The Japanese original ([06-epic-lane.md](../../../docs/06-epic-lane.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# Epic Lane — the layer that bundles human confirmation at Epic granularity

On larger work, if human owner confirmation is inserted at every Issue, the human becomes the bottleneck. This layer bundles human confirmation into just three points — the Epic's entry (kickoff), pre-agreed stop points, and exit (integration confirmation) — **without loosening at all** the gates between agents (cross-review, evidence, declaration scope).
Each rule carries a stable rule ID (`E-1` through `E-10`). The summary side ([docs/04](04-adoption.md)) references these IDs. Review seat rules are in [L1-9 through L1-11](02-issue-loop.md); the posture for when verification isn't possible is in [docs/05](05-fail-posture.md) (especially FP-9).

## Definition of high-risk areas (a single definition referenced by both E-3 and L1-11)

Work touching the following is called a **high-risk area**:

**External publication / sending to people, billing/spending, irreversible operations (data deletion, migration, rewriting shared history), permission/authentication/secret boundaries, pre-release gates**

There are two responses to a high-risk area: always stop as a human checkpoint (E-3), and increase review seats to five ([L1-11](02-issue-loop.md)). Don't keep two separate lists — this single spot is the canonical source. **This definition applies beyond the Epic lane** (L1-11's seat-count determination references this section across all sizes and all lanes — adopters who don't use the Epic lane should still read this section).

## E-1 Criteria and establishment of becoming an Epic

- Weight determination uses [L2-1](01-milestone-loop.md) as-is (don't invent a new criterion). This section only declares the entry point: "work that L2-1 classified as an EPIC Issue operates under this layer"
- **An Epic is established by the owner's (human's) kickoff approval** — the approval target is the EPIC Issue body (including the E-3 checkpoint table; [template](../templates/epic-template.md)). Approval happens via the owner's comment on the EPIC Issue, and that comment is the evidence of establishment
- An Epic before approval is not an Epic: neither E-4's integration branch nor E-5's freedoms **arise** (it stays under normal Issue operation — [FP-9](05-fail-posture.md)). Don't break the correspondence: becoming an Epic = granting of freedoms = an explicit human judgment

## E-2 Separation of axes — feature-axis Epic × module-axis child Issues

- **Epic = feature axis** (write value in human language. e.g., "make call response faster"). **Child Issue = module axis** (1 child Issue = 1 module or 1 repo. gateway-side children and app-side children are separated)
- An Epic that touches an interface at a module boundary must **run a contract-freeze child Issue first, as number 0** (Epic-internal application of [L2-2](01-milestone-loop.md). Only the contract both sides touch — API schema, protocol, etc. — is fixed first, in a single pass)
- **Implementation on other child Issues may not begin until number 0 is merged into the epic branch** (an Epic-internal serial section — same intent as L2-2's "no new parallel work until the boundary PR merges"). After number 0 merges, all child branches must rebase before continuing implementation
- After contract freeze, child Issues whose declared file sets are non-overlapping may run in parallel (this rides directly on [L2-4](01-milestone-loop.md))
- For a cross-repo Epic, place a child Issue in each repo with the EPIC Issue as the hub. Dependencies between child Issues are declared via `Blocked-by` / successor links (adoption of pending item 6a from the [docs/05 appendix](05-fail-posture.md). **Only the declaration-obligation part is adopted** — "don't set to MERGED until the terminus" (6b) remains pending, and a child Issue may still be set to MERGED normally at its own terminus)

## E-3 Human checkpoint table

A **mandatory section** of the EPIC Issue ([template](../templates/epic-template.md)). Each row = "where it stops / what to show / why it needs human judgment."

- The owner approves the table at kickoff (the same event as E-1) → from then on, execution **stops only at points in the table** and runs straight through everywhere else
- **Mandatory triggers that must appear in the table**: **every item in the high-risk areas** listed at the top, **plus contract-level deviations**. Whether something is contract-level is determined mechanically by a 3-part check: "does it touch **the artifact frozen in E-2's number 0, the EPIC Issue's Done when, or the external interface description**." For an Epic that doesn't set up a number 0, Done when and the external-IF description are treated as the frozen artifact — don't derive a gate decision from an empty set ([FP-6](05-fail-posture.md))
- **Passing a checkpoint requires the owner's explicit comment of approval** (same form as E-1's kickoff approval — leave the approval comment URL in the template's status field). Rewriting the status field alone does not constitute approval ([FP-8](05-fail-posture.md))
- **Deviations that are internal implementation decisions do not stop**: a design change that doesn't move the contract, external IF, or Done when is recorded in the Epic log (E-7) without stopping, and reviewed in bulk at integration confirmation. Making this a stop trigger would resurrect per-Issue human confirmation and self-contradictorily defeat the purpose of this layer
- If an unforeseen "matter requiring human judgment" arises, **stop as an ad-hoc checkpoint** (fail-closed)
- **Revisions to the table are asymmetric**: an agent may **add** a row unilaterally, effective immediately. **Deleting, loosening, or conditionalizing** a row is treated as a replacement record under [L1-8](02-issue-loop.md), and **the old table stays in effect until the owner's explicit approval comment** ([FP-8](05-fail-posture.md) — self-editing the body does not produce approval). Judge by **effect**, not form: even something shaped like an addition — e.g. adding a row that says "child #5 onward doesn't need this row's stop" — that narrows the scope of an existing row counts as a loosening and has no effect until the owner re-approves (tighten-only — same direction as [docs/04](04-adoption.md))
- An Epic **without a table, missing mandatory trigger rows, malformed, or unapproved** has not launched as an Epic (E-1). If a checkpoint decision becomes necessary in this state, **stop and escalate to a human** ([FP-9](05-fail-posture.md)). If the table becomes invalid **while an Epic is running**, stop with the same posture, but preserve the topology — what stops is E-5's freedoms and checkpoint passage, not reverting child lanes to normal Issue operation heading straight to main (that would bypass E-6③'s integration gate)

## E-4 Epic integration branch and topology

- Create an `epic/<EPIC Issue number>` branch plus an **integration-only** worktree. Merging into main happens **once by default, at Epic completion** (L0-5 / [L0-7](03-git-protocol.md) applies as-is to epic→main)
- **Writer assignment** (consistency with [L0-4](03-git-protocol.md)):
  - Child lanes keep the usual **1 child Issue = 1 branch = 1 worktree**, work in their own worktree, and post a WIP declaration (the [L0-1](03-git-protocol.md) 4 fields) to their own child Issue. **Child branches branch off the epic branch** (the `origin/main` in [L0-4](03-git-protocol.md)'s command example is the default for lanes outside an Epic — inside an Epic, read it as `epic/<number>`. Branching off main would mix the entire diff against main into the child→epic PR and break E-6②'s diff reconciliation)
  - The epic worktree is **dedicated** to integration work (merging, conflict resolution, pulling in main), and its only writer is **the single person who posted the WIP declaration on the EPIC Issue** (Files to touch covers only the integration work). Child lanes do not work in the epic worktree
  - Overlap determination happens at two layers: (a) between children within the Epic (L2-4 applied) (b) against lanes outside the Epic (E-10). The basis for default-deny ([L0-2](03-git-protocol.md)) is **the child Issue's declared set**
- **The only means of merging child→epic is fixed to "a PR whose base is the epic branch"** (this leaves diff reconciliation and review records on GitHub). Merges happen one at a time — once an adjacent child merges into epic, any child waiting in the queue owes a rebase-and-reverify (L0-7 applied)
- **Periodic pull-in of main**: when a lane outside the Epic merges into main, the epic branch promptly pulls in main and reverifies (the Epic version of L0-7's rebase obligation; the pull-in is done by the epic worktree's writer). This periodic pull-in, together with E-8's time limit, is how long-lived-branch rebase hell ([L0-8](03-git-protocol.md)) gets handled
- **An intermediate merge (a mid-way epic→main merge) is an exception**, and is permitted only when: ① it's recorded in advance as an E-3 checkpoint, and ② each occurrence is subjected to E-6③'s integration gate (full [L1-7](02-issue-loop.md)). A mid-way merge that doesn't satisfy both conditions violates E-4

## E-5 Sandbox freedoms

Once an Epic is established (E-1), inside a child lane's worktree/child branch, anything within the declared scope is free: commit granularity, redoing work, refactoring, child-branch operations, and rewriting **unmerged history on one's own branch** (including force-push).

**"Own branch" = the not-yet-merged-into-epic history of one's own child Issue branch.** Nothing else counts as one's own branch.

**Invariant prohibitions** (this enumeration is what outlines the freedom — when summarizing, don't loosen it into something like "anything short of destructive acts is free"):

1. Direct push to main ([L0-5](03-git-protocol.md))
2. Writing outside the declared scope ([L0-2](03-git-protocol.md) default-deny — the basis is the child Issue's declared set)
3. Deleting or altering another lane's or another worktree's contents
4. **Rewriting the epic integration branch's history (force-push, reset)** — within its Epic, epic is the equivalent of main. To replace content already merged into epic, use [L1-8](02-issue-loop.md)'s replacement record plus re-review (no silent re-merge)
5. Sending secret information externally
6. Executing an E-3 checkpoint item without approval

## E-6 Hourglass review — 3 spots, different units

The definition of review-seat heterogeneity and seat count is in [L1-10 / L1-11](02-issue-loop.md).

1. **Design review = once per Epic (before implementation begins — can happen after the EPIC Issue is filed, but no later than before the first child Issue's implementation starts. Same clock as [L1-9](02-issue-loop.md))**: the setup is L/H (3 heterogeneous seats). **5 seats only for an Epic that includes a high-risk area** (L1-11). Don't make child Issues recurse into a full design meeting
2. **Implementation review = every time, per child Issue (a light gate for child→epic)**: seat count is looked up in the [L1-11](02-issue-loop.md) table using **that child Issue's own weight** (not the Epic's weight — attaching heavy review to every child kills velocity). **However, if a child Issue touches a high-risk area (defined at the top), L1-11's 5 seats take priority and the seat count cannot be reduced**. **What can be lightened is only the seat count and the record format — never the existence of evidence.** Mandatory records for a child→epic PR: **inline excerpt of the terminal test-green result / heterogeneous cross-review ([L1-3](02-issue-loop.md), including identity check) / candidate commit SHA / reconciliation of the declared file set vs `git diff --stat` ([L0-6](03-git-protocol.md) — a file in the diff but not in the declaration is blocking)**. The candidate SHA must **match the PR head at merge time** — if it changed after review, re-review ([L1-8](02-issue-loop.md) applied. E-5's force-push freedom does **not include** replacing an already-reviewed SHA). The only thing that may be omitted is the table-format mapping to Done when (prose covering the key points is fine — however, L1-7's principle that "the terminal result must be readable from the record alone" still holds — evidence that's just a link doesn't qualify)
3. **Integration review = once, for epic→main**: the full integration diff gets **the review setup matching the Epic's weight, plus a full [L1-7](02-issue-loop.md) completion record**. The owner's final confirmation also happens here (E-7)

## E-7 Epic log and digest

- Every time a child Issue reaches its terminus, post one comment to the EPIC Issue: **what got done / evidence (link to the child→epic PR plus key points) / Done when gaps and compromises (write "none" explicitly if there are none) / what's next**. Listing gaps and compromises may not be omitted — this prevents the digest from becoming a rosy summary
- The owner's final confirmation happens via **the log's digest + the integration diff + confirmation of the working deliverable** (read this as a demo for anything runnable, or as rendering/link-check for docs)
- For scope already approved at an E-3 checkpoint, present **only the diff since the approval point** at final confirmation (giving checkpoint approval cumulative effect — don't shift the human's entire confirmation burden to the end)

## E-8 Time limits — read the two clocks separately

- **Branch lifespan (what's enforced)**: the epic branch should reach main within **1–2 weeks** (starting from the date of E-1's kickoff-approval comment). If it looks like it'll run over, either split the Epic or set up a checkpoint for an intermediate merge (E-4's exception procedure). This number is adjusted only via a PR to the handbook (same treatment as [L0-3](03-git-protocol.md)'s 72h). "A few child Issues" as a scale sense is a guideline, not a rule
- **Staleness (the lock's clock)**: [L0-3](03-git-protocol.md) applies as-is to the EPIC Issue's WIP too (default 72h). Since an Epic can be expected to have long silences, use L0-3's **exception-declaration path** (state a longer window with a reason in the WIP declaration) as needed. "1–2 weeks" is the branch lifespan and is **not** the staleness window — this means both: don't treat an epic that's been silent for 5 days as stale just because it's within its lifespan, and conversely, an epic that exceeds 72h without declaring a window is stale as usual

## E-9 Epic termination — completion, abandonment, handoff

- [L1-4](02-issue-loop.md)'s 5-vocabulary set (WIP / HOLD / MERGED / SUPERSEDED / ABANDONED) applies to the EPIC Issue's lane state too
- **Completion** = epic→main has passed E-6③ and been merged, all child Issues have reached their terminus, and the epic branch/worktree have been cleaned up
- **Abandonment/discontinuation (ABANDONED / SUPERSEDED)** must not end with just a declaration. The termination comment must always record: ① **disposition of the epic branch** — discard (delete) or a **rescue PR** for the valuable parts (a partial merge of epic→main, passed through E-6③'s integration gate — don't loosen it just because it's a rescue) ② **convergence of child Issue state**, merged and unmerged (SUPERSEDED / ABANDONED / carved out into an independent Issue) ③ worktree cleanup. However, **don't unilaterally terminate a child lane holding a live WIP lock from the epic side** — convergence happens only via notification to the lock owner plus the owner's own termination declaration, or via TAKEOVER after going stale ([L0-3](03-git-protocol.md))
- **Handoff**: taking over an epic lane is done via **TAKEOVER on the EPIC Issue** ([L0-3](03-git-protocol.md)) plus the resumption checklist ([L0-9](03-git-protocol.md)). If surviving child lanes exist, the person taking over must first re-read the child WIPs and must not do integration work on top of a live lock (the Epic version of L0-2's optimistic re-read)

## E-10 Running multiple Epics concurrently

- An Epic's **effective declared set = the union of child Issues' declared file sets ∪ the EPIC Issue's WIP declared set** (include the epic worktree's integration-work scope — E-4 — in the overlap determination too. Aggregate and record this in the EPIC Issue body, updating it as children are added or removed)
- Parallel-GO determination between Epics, or between an Epic and a single-shot lane, applies [L2-4](01-milestone-loop.md) using this effective declared set (GO only if non-overlapping, serialize if unverifiable — [FP-1](05-fail-posture.md))
- An Epic touching a broad range of a repo runs **solo**, per [L2-5](01-milestone-loop.md)
- epic→main merges happen one at a time, per [L0-7](03-git-protocol.md). When an adjacent Epic (or single-shot lane) merges into main, a running Epic owes a pull-in of main and reverification (E-4's periodic pull-in)
