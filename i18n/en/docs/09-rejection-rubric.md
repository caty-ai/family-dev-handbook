> **Machine translation.** The Japanese original ([09-rejection-rubric.md](../../../docs/09-rejection-rubric.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# R Rejection Rubric — The Layer for What to Accept and What to Decline

Where the L layers (L2 / L1 / L0) are the contract for **how to proceed**, and the B layer is the contract for **how to ask**, the R layer defines the contract of intent for **what gets merged and what gets declined**. It's used in two ways:

1. **For contributors** — so contributions (including agent-originated proposals, tasks, and PRs) can aim at the target
2. **For first-pass triage** — as guidance on when it's fine to close without a human judgment call, and just as important, on when it must not be closed

Normativity differs by rule: **R-1 / R-4 / R-5 / R-6 are contracts**, **R-2 / R-3 are criteria lists for acceptance judgment**, and enforcement of a rejection grounded in R-2 / R-3 always routes through R-1's authority discipline (value judgments are the owner's call alone).

Each rule carries a stable rule ID (`R-1` through `R-6`), and clauses within it are referenced by ①②③… (the same format as [E-6](06-epic-lane.md)①). The summary side ([docs/04](04-adoption.md)) references these IDs. For the posture to take when something can't be verified, see [docs/05](05-fail-posture.md).

Source: this chapter is an adaptation of the "Contribution Rubric" section of NousResearch/hermes-agent's AGENTS.md (MIT).

## R-1 The 3 Reasons for Automatic Rejection — Value Judgments Are the Owner's Call Alone

**Applies to recorded proposals** (Issues, PRs, task proposals submitted as records). The only reasons these may be rejected without a human judgment call are the **3 mechanically black-and-white reasons**. Each reason only holds once its conditions and evidence are attached:

1. **Already on main** (implemented on main) — point to the commit or line showing the behavior in question already exists on current main. "Something functionally similar exists" does not qualify under this reason (that's a value judgment = the owner's call alone)
2. **Cannot reproduce** (cannot reproduce) — **bug reports only**. Leave a record of the reproduction attempt against current main (command / steps, observed result, date). Insufficient information is not grounds for rejection — query and hold
3. **Incoherent** (incoherent) — contradictory, empty, spam, or otherwise no substantive claim can be made out, and only **after one round of querying still nothing can be made out**. A proposal that's merely tedious to read doesn't qualify

- Rejection on grounds of value judgment — "we don't need this / doesn't match direction / out of scope" — **is the owner's (human's) call alone**. An agent's job stops at escalating with a recommendation and rationale (this applies equally to rejections grounded in R-2 / R-3 — they are not among the 3 reasons)
- **When in doubt, don't close** — "closing" is an exercise of authority; if it can't be verified, err toward the direction that narrows authority (leave it open, up to the owner) (the same direction as [FP-7](05-fail-posture.md)). First-pass triage's job is to read the design intent and **avoid mistakenly closing a legitimate contribution**
- **Record-keeping**: termination of a proposal that already had a lane stood up (WIP declared) follows the 5-vocabulary set in [L1-4](02-issue-loop.md). **For a proposal rejected before a lane is stood up, don't use lane vocabulary** — just record the close reason (one of the 3 reasons plus the evidence above, or a link to the owner's ruling)
- **Reopening is asymmetric**: a closure under the 3 reasons may be reopened without owner approval once new evidence surfaces (reopening moves in the direction that narrows authority)
- Proposals touching any of R-4's 4 patterns are the textbook case where automatic closure under the 3 reasons is **not safe** — escalate to a human
- Rejection decisions made while an Epic is running should be routed to the owner **asynchronously, without stopping the lane** (don't add stop points beyond [E-3](06-epic-lane.md))

## R-2 Welcome Contributions — 6 Clauses

1. **Fix a real bug, across the whole class** — reproduce the symptom on current main, point to the line where it shows up, and fix the sibling call paths too, not just the one spot that was reported (the counterpart to R-4's watchword)
2. **Extend the extremities, guard the core** — contributions that extend the extremities (features of individual products/households) are welcome. Restraint is aimed only at the core (shared family infrastructure, where everyone pays a permanent cost). "Minimize footprint" is about wiring into the core — it says nothing about whether a product may grow
3. **A declared refactor is welcome even with a large diff** — the check that "every line must trace back to the request" applies to functional changes; a request for a change declared as a refactor is itself the extraction (hotspot splitting = the investment described in [L2-6](01-milestone-loop.md)). **Only the suspicion attached to diff size is relaxed** — the declared file set ([L0-2](03-git-protocol.md) default-deny) and the diff cross-check in [L1-7](02-issue-loop.md)④ never relax, refactor or not (a refactor gets through by declaring a broad "files to touch" prediction, not by skipping the declaration). Solo execution of broad refactors ([L2-5](01-milestone-loop.md)) and the merge procedure ([L0-7](03-git-protocol.md)) still apply as-is
4. **Extend, don't duplicate** — before adding a new module, manager, or hook, check whether an existing tool already serves the purpose (placement is covered by R-5)
5. **Tests should assert invariants** — check "how two pieces of data should relate to each other"; don't write change-detection tests that freeze a current value (a list, a count, a hardcoded version)
6. **Verify boundaries, propagation, and I/O over the real path** — changes touching resolution chains, config propagation, permission boundaries, or external I/O must come with E2E evidence exercising the actual path. Don't treat a mock-only green as done. **This clause is guidance on how to pick evidence — the source of truth for merge-gate requirements remains [L1-7](02-issue-loop.md)** (it doesn't add requirements)

## R-3 Decline Even When Well-Executed — 7 Clauses

Things declined as a **structural judgment**, not a quality bar. Being well-executed doesn't remove the reason for declining. **A rejection grounded in this rule is not among R-1's 3 reasons — enforcement always remains the owner's call alone**; an agent's job stops at flagging the suspicion and escalating:

1. **Speculative infrastructure** — hooks, callbacks, or extension points with no concrete consumer. If there's a stated real use case, it isn't speculative (the consumer can live in a separate repo)
2. **Adding an environment variable for non-secret configuration** — secret storage (.env, etc.) is for secrets only. Behavioral settings (timeouts, thresholds, flags, display) belong in a config file
3. **A new skill, hook, or standing system when an existing tool would do** — if there's no record of having considered R-5's ladder from its lowest rung, decline the new addition
4. **A lazy-reading escape hatch for content that should be read in full** — don't add pagination or excerpt options to a loader for content an agent should read completely (skills, prompts, procedure docs). It becomes easy to read only page 1 and skip the rest
5. **A "fix" that breaks the very feature it was supposed to protect** — a mitigation that kills a feature's purpose is the wrong mitigation. Read the original commit's intent (`git log -p -S`) before restricting behavior
6. **Wiring without proof, or unauthorized non-secret telemetry** — code wired in without E2E proof, branches never exercised at runtime, or outbound telemetry / identifier attachment with no opt-in gate (**this includes non-secret usage information**). Sending secret information externally is not covered by this clause — it follows **[E-5](06-epic-lane.md) and each household's secrecy discipline; this clause does not alter the boundary of E-5's closed prohibition list**
7. **Pulling an external tool or someone else's product into the core tree** — the maintenance burden lands on us permanently. Put it in a wrapper or an isolated location (e.g., a quarantined directory for staging, or a separately maintained external repo — these are illustrative, not normative) rather than the core. This is a coupling-and-maintenance judgment, and closing stands even when the quality is high

## R-4 Premise Verification — Before You Call It a Bug

Watchword: **"If you can't point to the line where the bug shows up, the premise is unverified."**

The biggest reason a well-crafted change gets declined isn't quality — it's that it's built on a **wrong premise**, or it treats **deliberate design as a defect**. The following 4 patterns cut both ways — they tell review seats where to scrutinize, and they tell first-pass triage when not to close:

1. **It's deliberate design, not a defect** — a limitation that looks like an oversight is often intentional. Before fixing it, ask "isn't this isolation the design?" and read the original commit's intent
2. **The premise doesn't hold up against how the code actually behaves** — trace the real code and its runtime behavior before accepting the claim. If you can't show which line's behavior the fix changes, it's unverified
3. **An absence was load-bearing** — adding a piece that seems "obviously missing" can break what that omission was protecting
4. **Overreach, or reviving a policy that already passed by** — an extension beyond the agreed-upon base, or rehashing a direction that was deliberately closed off, gets declined even if it works. Keep the change to the narrow, agreed-upon part, and propose the rest as a follow-up

Underlying theme: **verify both the claim and the intent against the codebase, before writing and before merging**. A confirmed reproduction plus a line-level explanation always beats a plausible-sounding argument. When intent is unclear, it's cheaper to ask than to ship a fix that fights the design.

(Concrete examples may be swapped out for each household's incident records — the examples in the body text are illustrative, not normative. When delegating a review, these 4 patterns can be front-loaded as the "name the worst failure mode" perspective in [B-4](07-delegation-brief.md).)

## R-5 The Placement Ladder — Minimize Permanent Surface Area at the Lowest Rung

When building a new capability, the lower the rung, the more permanent surface area (a cost everyone keeps paying) it adds. **Pick the lowest-numbered rung that correctly solves the problem**:

1. **Extend existing code** — if it's a variant of something that already exists, the new surface is zero
2. **Script / skill** — an operation expressible in shell. Doesn't run standing; only runs when invoked
3. **Conditionally gated hook** — automation that only appears once a precondition is configured
4. **Add a feature to an existing repo** — if a place for it already exists, put it there
5. **Split off into an MCP server or a separate repo** — for a genuinely independent capability, outside the core
6. **A new repo or new standing system** — last resort. **Requires owner (human) approval.** If this comes up mid-Epic, **stop it as an ad hoc checkpoint under [E-3](06-epic-lane.md)** (don't append it to E-3's table)

- When in doubt, go up a rung (minimize surface area). "The lower rung is easier" is not a reason
- **When you pick a rung, decide the exit trigger for what you're placing, at the same time** ([LC-1](08-lifecycle.md) — the ladder decides where to put it, LC-1 decides how it leaves. Use them as a pair)
- **A common entry point on the 3rd instance of a kind** — once three integrations of the same category have accumulated, don't add a fourth one-off; design a common interface and wrap the existing implementations as the first providers. Since designing the entry point is a boundary change, it rides on [L2-2](01-milestone-loop.md)'s boundary-PR-first rule

## R-6 Enforce Policy with a Check

**Don't leave a policy that can't afford to be broken as a "please."** Passive rules (.gitignore, documentation, verbal agreements) only stop honest mistakes — a policy you want enforced needs to be promoted to a check that turns red when broken.

- **Promotion trigger**: once the same policy has been broken twice, file an Issue to turn it into a check. **Keep a record of each break in an Issue or in each household's incident record, and file the promotion Issue when the 2nd record lands** (so the count can be verified later)
- A check should **detect by substance** (match on the actual content/pattern, not on directory naming or extension spelling — the source material includes a real case where a misspelling slipped past the check)
- A check's posture should align with existing rules: **a gate that blocks merge is fail-closed** (the direction in [FP-3](05-fail-posture.md)), **reporting/synthesis/notification plumbing is fail-open** ([FP-4](05-fail-posture.md)). A check does not move files ([LC-5](08-lifecycle.md) — it only detects and blocks; no auto-repair, no auto-retirement)
- An approval-type check (a human label, etc.) must **verify that the approval actually exists** — don't pass just because text or a label is present ([FP-8](05-fail-posture.md)'s direction). Approval verification can have limits (e.g., a shared-identity environment) — in that case, spell out the limit in the check's description and don't pretend it's "verified" ([FP-5](05-fail-posture.md))
- The source of truth for templates lives in this repo's [templates/ci/](../templates/ci/)
