> **Machine translation.** The Japanese original ([09-rejection-rubric.md](../../../docs/09-rejection-rubric.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# R Rejection Rubric — The Layer for What We Accept and What We Decline

Where the L layers (L2 / L1 / L0) are the contract for **how to proceed**, and the B layer is the contract for **how to ask**, the R layer sets the contract of intent for **what gets merged and what gets declined**. It serves two purposes:

1. **For builders** — so contributions (including agent-originated proposals, tasks, and PRs) can aim at the actual target
2. **For first-pass triage** — guidance on when it's fine to close something without a human judgment call, and just as important, **when it must not be closed**

Normativity differs by clause: **R-1 / R-4 / R-5 / R-6 are contracts**, while **R-2 / R-3 are criteria lists for acceptance judgment**, and enforcement of a rejection grounded in R-2 / R-3 always routes through R-1's authority discipline (value judgments are the owner's call alone).

Each rule carries a stable rule ID (`R-1` through `R-6`), and sub-items are referenced as ①②③… (same format as [E-6](06-epic-lane.md)①). The summary side ([docs/04](04-adoption.md)) references these IDs. For the stance to take when verification isn't possible, see [docs/05](05-fail-posture.md).

Source: this chapter is an adaptation of the "Contribution Rubric" section from NousResearch/hermes-agent's AGENTS.md (MIT). Acquisition date, provenance classification, and the full license text are consolidated in [templates/ci/NOTICE.md](../../../templates/ci/NOTICE.md).

## R-1 The 3 Reasons for Automatic Rejection — Value Judgments Are the Owner's Call Alone

**This applies to recorded proposals (Issues, PRs, and task proposals submitted as records)**. The only grounds for rejecting these without a human judgment call are the **3 reasons that resolve mechanically, black-and-white**. Each reason only holds once its qualifying conditions and evidence are met:

1. **Already on main** (implemented on main) — you must point to the commit or line showing the behavior in question already exists on current main. "Something functionally similar exists" does not qualify under this reason (that's a value judgment = the owner's call alone)
2. **Cannot reproduce** (cannot reproduce) — **bug reports only**. Leave a record of the reproduction attempt against current main (commands/steps, observed result, date). Insufficient information is not grounds for rejection — query the reporter and hold instead
3. **Incoherent** (incoherent) — reserved for cases where no substantive claim can be made out — contradictions, blank content, spam, etc. — and only **after one round of clarifying query still leaves it unintelligible**. A proposal that's merely tedious to read doesn't qualify

- Rejections based on value judgments — "we don't need this," "doesn't fit our direction," "out of scope" — are **the owner's (human's) call alone**. An agent's job stops at escalating with a recommendation and rationale (this applies equally to rejections grounded in R-2 / R-3 — they are not among the 3 reasons)
- **When in doubt, don't close** — closing is an exercise of authority; when verification isn't possible, default toward the direction that narrows authority (leave it open, escalate to the owner) (the [FP-7](05-fail-posture.md) direction). First-pass triage's job is to read the design intent and **avoid mistakenly closing a legitimate contribution**
- **Recording**: for a proposal that already had a lane established (WIP declared), termination follows [L1-4](02-issue-loop.md)'s 5-vocabulary set. **For a proposal rejected before a lane was ever established, don't use lane vocabulary** — just record the closure reason (one of the 3 reasons plus the evidence above, or a link to the owner's ruling)
- **Reopening is asymmetric**: a closure under the 3 reasons may be reopened without owner approval once new evidence surfaces (reopening narrows authority further, so it's allowed)
- A proposal touching any of R-4's 4 patterns is a textbook case where automatic closure under the 3 reasons is **unsafe** — escalate to a human
- Rejection decisions during an active Epic run should be routed to the owner **asynchronously, without stopping the lane** (don't add stop points beyond [E-3](06-epic-lane.md))

## R-2 Contributions We Welcome — 6 Items

1. **Fixing a real bug, across the whole class** — reproduce the symptom on current main, point to the line where it appears, and fix not just the one reported spot but the sibling call paths as well (the counterpart to R-4's watchword)
2. **Extend at the edges, conserve at the core** — contributions that extend the edges (features of individual products, individual households) are welcome. Restraint is reserved for the core only (shared family infrastructure, the place where everyone pays a permanent cost). "Minimize footprint" is about wiring into the core — it says nothing about whether a product is allowed to grow
3. **A declared refactor is welcome even with a large diff** — the check that "every line must trace back to the request" applies to behavioral changes; a request for a change declared as a refactor is itself the extraction (splitting a hotspot = the investment described in [L2-6](01-milestone-loop.md)). **Only the suspicion attached to diff size is relaxed** — the declared file set ([L0-2](03-git-protocol.md) default-deny) and the diff cross-check in [L1-7](02-issue-loop.md)④ never relax, refactor or not (a refactor gets through by declaring a broad set of files it expects to touch, not by skipping the declaration). Solo execution of a broad refactor ([L2-5](01-milestone-loop.md)) and the merge procedure ([L0-7](03-git-protocol.md)) apply unchanged as well
4. **Extend rather than duplicate** — before adding a new module, manager, or hook, check whether an existing tool already does the job (placement is covered under R-5)
5. **Tests assert invariants** — check "how two pieces of data ought to relate to each other"; don't write change-detection tests that freeze current values (lists, counts, hardcoded versions)
6. **Verify boundaries, propagation, and I/O through real paths** — a change touching resolution chains, config propagation, permission boundaries, or external I/O must present E2E evidence exercising the actual path. A mocks-only green isn't a finished job. **This item is guidance on how to choose evidence; the authoritative source for merge-gate requirements remains [L1-7](02-issue-loop.md)** (this doesn't add new requirements)

## R-3 Things We Decline Even When Well Executed — 7 Items

These are declined as a **structural judgment**, not a quality bar. Being well executed doesn't remove the reason for declining. **A rejection grounded in this clause is not among R-1's 3 reasons — enforcement is always the owner's call alone**; an agent's job stops at flagging the suspicion and escalating:

1. **Speculative infrastructure** — hooks, callbacks, extension points with no concrete user. If there's a stated real use case, it isn't speculative (even if the user lives in a different repo)
2. **Adding an environment variable for non-secret configuration** — secret storage (.env, etc.) is for secrets only. Behavioral settings (timeouts, thresholds, flags, display) belong in a config file
3. **A new skill, hook, or persistent system when an existing tool would suffice** — decline anything new that lacks a record of having first considered R-5's ladder from its smallest rung
4. **An escape hatch for lazy reading of something that should be read in full** — don't add pagination or excerpt options to a loader for content an agent is meant to read completely (skills, prompts, runbooks). It becomes a habit of reading only page one and skipping the rest
5. **A "fix" that breaks the very feature it was supposed to protect** — a mitigation that kills the purpose of a feature is the wrong mitigation. Read the original commit's intent (`git log -p -S`) before restricting behavior
6. **Wiring without proof, or unauthorized non-secret telemetry** — code wired in without E2E proof, branches never exercised at runtime, or outbound telemetry/identifier tagging without an opt-in gate (**this includes non-secret usage information**). Sending secret information externally is not covered by this item and instead follows **[E-5](06-epic-lane.md) and each household's secret discipline — this clause does not alter the shape of E-5's closed prohibition list**
7. **Pulling an external tool or someone else's product into the core tree** — the maintenance burden falls on us permanently. Put it in a wrapper or an isolated location (e.g., a quarantined directory for staging, or a separately maintained external repo — these examples are illustrative, not normative) rather than the core. This is a coupling-and-maintenance judgment, and high quality doesn't change a close into anything but a close

## R-4 Premise Verification — Before Calling It a Bug

Watchword: **"If you can't point to the line where the bug shows up, the premise is unverified."**

The most common reason a well-made change gets declined isn't quality — it's that it's built on a **wrong premise**, or it's **treating deliberate design as a defect**. The following 4 patterns cut both ways — they tell reviewers where to scrutinize, and they tell first-pass triage when *not* to close:

1. **It's deliberate design, not a defect** — a limitation that looks like an oversight is often intentional. Before fixing it, ask "isn't this isolation the actual design?" and read the original commit's intent
2. **The premise doesn't hold up against how the code actually behaves** — trace the real code and its runtime behavior before accepting a claim at face value. If you can't show which line's behavior the fix changes, it's unverified
3. **The absence was load-bearing** — adding a piece that "obviously seems missing" can break whatever that omission was protecting
4. **Overreach, or reviving a settled-past decision** — an extension beyond the agreed baseline, or reopening a direction that was deliberately closed, gets declined even if it works. Keep the change to the narrow scope that was agreed, and propose the rest as a follow-up

Underlying theme: **verify both the claim and the intent against the codebase before writing, and before merging**. A confirmed reproduction plus a line-level explanation beats a plausible-sounding argument every time. When intent is unclear, it's cheaper to ask than to ship a fix that fights the design.

This evidence bar applies to review-seat findings too: **a finding that can't point to a path:line or quote an execution log cannot be marked blocking** (raising it as a non-blocking concern is fine). This is the counterpart to [L1-3](02-issue-loop.md)'s ratchet ban for follow-up rounds.

(Concrete examples may be swapped out for each household's own incident records — the examples in this text are illustrative, not normative. When delegating a review, these 4 patterns can be front-loaded as the "name the worst failure mode" angle from [B-4](07-delegation-brief.md).)

## R-5 The Placement Ladder — Minimize Permanent Surface Area at the Lowest Rung

When building a new capability, the lower the rung, the more permanent surface area (a cost everyone keeps paying) it adds. **Pick the lowest-numbered rung that correctly solves the problem**:

1. **Extend existing code** — if it's a variant of something that already exists, the new surface is zero
2. **Script / skill** — an operation expressible in shell. Not persistent — runs only when invoked
3. **Conditionally gated hook** — automation that only appears once its preconditions are configured
4. **A feature added to an existing repo** — if a place for it already exists, put it there
5. **An MCP server, or split into a separate repo** — for a genuinely independent capability, keep it outside the core
6. **A new repo or new persistent system** — the last resort. **Requires owner (human) approval.** If this comes up during an active Epic run, **stop it as an ad hoc checkpoint under [E-3](06-epic-lane.md)** (don't add it to E-3's published table)

- When in doubt, move up (toward minimal surface area). "The lower rung is easier" is not a reason
- **When you choose a rung, decide the exit trigger for what you're placing at the same time** ([LC-1](08-lifecycle.md) — the ladder decides where to place it, LC-1 decides how it leaves. Use them as a pair)
- **A shared entry point on the third instance of a kind** — once three integrations of the same category have accumulated, don't add a fourth one-by-one; design a common interface and wrap the existing implementations as its first providers. Designing a shared entry point is a boundary change, so it rides on [L2-2](01-milestone-loop.md)'s boundary-PR-first requirement

## R-6 Enforce Policy with a Check

**Don't leave a policy that must not be broken as a mere "please."** Passive rules (.gitignore, documentation, verbal agreements) only stop honest mistakes — a policy you actually want enforced needs to be promoted to a check that turns red when broken.

- **Promotion trigger**: once the same policy has been broken twice, file an Issue to build the check. **Record each break in an Issue or in the household's incident record, and file the Issue at the point of the second recorded break** (so the count can be verified after the fact)
- A check should **detect by substance** (match on the actual content/pattern, not directory names or extension spelling — a real case of someone slipping past via a misspelling is on record in the source)
- A check's posture should align with existing clauses: **gates that block a merge are fail-closed** (the [FP-3](05-fail-posture.md) direction), **reporting/aggregation/notification pipes are fail-open** ([FP-4](05-fail-posture.md)). A check doesn't move files ([LC-5](08-lifecycle.md) — it detects and stops, nothing more; no auto-repair, no auto-retirement)
- An approval-type check (e.g., a human label) must **verify that the approval actually exists** — don't pass something just because text or a label is present (the [FP-8](05-fail-posture.md) direction). Approval verification can have limits (e.g., in a shared-identity environment) — if so, state the limit explicitly in the check's description and don't pretend it's "verified" ([FP-5](05-fail-posture.md))
- The authoritative types live in this repo's [templates/ci/](../../../templates/ci/)
