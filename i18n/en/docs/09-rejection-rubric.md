> **Machine translation.** The Japanese original ([09-rejection-rubric.md](../../../docs/09-rejection-rubric.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# R Rubric of Rejection — Layers of What to Accept, What to Refuse

Where the L layer (L2 / L1 / L0) is a contract for "how to proceed" and the B layer is a contract for "how to ask," the R layer defines the contract of intent — **what gets merged and what gets refused**. It's used in two ways:

1. **For those who build** — so contributions (including agent-originated proposals, tasks, and PRs) can take aim at the target
2. **For first-pass triage** — as guidance on when it's fine to close without human judgment, and just as important, **when it must not be closed**

Normativity differs by article: **R-1 / R-4 / R-5 / R-6 are contracts**, **R-2 / R-3 are criteria lists for acceptance judgment**, and enforcement of a rejection grounded in R-2 / R-3 always routes through R-1's authority discipline (value judgments are the owner's call alone).

Each rule carries a stable rule ID (`R-1` through `R-6`), and clauses are referenced by ①②③… (same format as [E-6](06-epic-lane.md)①). The summary side ([docs/04](04-adoption.md)) references these IDs. Posture when verification isn't possible is covered in [docs/05](05-fail-posture.md).

Source: this chapter is an adaptation of NousResearch/hermes-agent's AGENTS.md "Contribution Rubric" (MIT).

## R-1 The 3 Reasons for Automatic Rejection — Value Judgments Are the Owner's Call Alone

**Applies to recorded proposals** (Issues, PRs, task proposals submitted as records). The only grounds on which these may be rejected without human judgment are **the 3 mechanically black-and-white reasons**. Each reason is established only when its conditions and evidence are met:

1. **Already on main** (implemented on main) — point to the commit or line showing the behavior in question already exists on current main. "Something functionally similar exists" does not qualify for this reason (that's a value judgment = the owner's call alone)
2. **Cannot reproduce** (cannot reproduce) — **bug reports only**. Leave a record of the reproduction attempt against current main (command / steps, observed result, date). Insufficient information is not grounds for rejection — inquire and hold
3. **Incoherent** (incoherent) — limited to cases where no substantive claim can be discerned due to contradiction, blank content, spam, etc., and only **after one round of inquiry still fails to clarify it**. A proposal that's merely tedious to read does not qualify

- **Rejection by value judgment** ("we don't need this," "against direction," "out of scope," etc.) **is the owner's (human's) call alone**. An agent's job stops at escalating with a recommendation and rationale (this also applies to rejections grounded in R-2 / R-3 — they are not among the 3 reasons)
- **When in doubt, don't close** — "closing" is an exercise of authority; when unverifiable, err toward the direction that narrows authority (leave it open, to the owner) ([FP-7](05-fail-posture.md)'s direction). The job of first-pass triage is to read the design intent and **avoid mistakenly closing a legitimate contribution**
- **Record-keeping**: termination of a proposal for which a lane was already established (WIP declared) follows the 5-vocabulary of [L1-4](02-issue-loop.md). **For proposals rejected before a lane is established, don't use lane vocabulary** — record only the closure reason (one of the 3 reasons plus the evidence above, or a link to the owner's ruling)
- **Reopening is asymmetric**: a closure under the 3 reasons may be reopened without owner approval once new evidence appears (reopening is the direction that narrows authority)
- Proposals touching the 4 patterns in R-4 are a classic case where automatic closure under the 3 reasons **is not safe** — escalate to a human
- Rejection decisions made while an Epic is running are routed to the owner **asynchronously, without stopping the lane** (don't add stop points beyond [E-3](06-epic-lane.md))

## R-2 Welcome Contributions — 6 Clauses

1. **Fix a real bug, across the whole class** — reproduce the symptom on current main, point to the line where it appears, and fix not just the reported spot but sibling call paths too (the counterpart to R-4's watchword)
2. **Extend the edges, conserve the core** — contributions that extend the edges (features of each product, each house) are welcome. Restraint applies only to the core (shared family infrastructure, where everyone pays the permanent cost). "Minimize footprint" is about wiring into the core, not about whether a product is allowed to grow
3. **A declared refactor is welcome even with a large diff** — the check that "every line must trace back to the request" applies to functional changes; a request for a change declared as a refactor is itself the extraction (hotspot splitting = an investment under [L2-6](01-milestone-loop.md)). **Only suspicion toward diff size is relaxed** — the declared file set ([L0-2](03-git-protocol.md) default-deny) and the diff match in [L1-7](02-issue-loop.md)④ never relax, even for a refactor (a refactor gets through by declaring a broad Files-to-touch prediction, not by omitting the declaration). Solo execution for broad refactors ([L2-5](01-milestone-loop.md)) and the merge procedure ([L0-7](03-git-protocol.md)) still apply as-is
4. **Extend rather than duplicate** — before adding a new module, manager, or hook, check whether an existing tool won't already serve the purpose (placement is covered by R-5)
5. **Tests assert invariants** — test "how two pieces of data should relate to each other"; don't write change-detection tests that freeze the current value (a list, a count, a hardcoded version)
6. **Verify boundaries, propagation, and I/O along real paths** — for changes touching resolution chains, config propagation, permission boundaries, or external I/O, produce evidence of an E2E run over the actual path. Don't treat mock-only green as done. **This clause is guidance on how to choose evidence — the canonical merge-gate requirement remains [L1-7](02-issue-loop.md)** (it doesn't add a new requirement)

## R-3 What to Refuse Even When Well Made — 7 Clauses

These are refused not as a quality bar but as **a structural judgment**. Being well made doesn't make the reason for refusal disappear. **A rejection grounded in this clause is not among R-1's 3 reasons — enforcement always remains the owner's call alone**; an agent's job stops at flagging the suspicion and escalating it:

1. **Speculative infrastructure** — hooks, callbacks, extension points with no concrete user. If there's a stated real use case, it isn't speculative (the user can be in a different repo)
2. **Adding an environment variable for non-secret configuration** — a place for secrets (.env, etc.) is for secrets only. Behavioral settings (timeouts, thresholds, flags, display) belong in a config file
3. **A new skill, hook, or standing system when an existing tool would suffice** — refuse a new addition with no record of having considered R-5's ladder from its smallest rung
4. **A lazy-read escape hatch for something that should be read in full** — don't add pagination or excerpt options to a loader for content an agent should read completely (skills, prompts, procedure docs). It leads to reading only page one and skipping the rest
5. **A "fix" that breaks the feature it was supposed to protect** — a mitigation that kills the purpose of a feature is the wrong mitigation. Read the original commit's intent (`git log -p -S`) before restricting behavior
6. **Unproven wiring, or unauthorized non-secret telemetry** — code wired in without E2E proof, branches never exercised at runtime, or outbound telemetry / identifier attachment without an opt-in gate (**includes non-secret usage information**). Sending secret information externally is not covered by this clause — it's governed by **[E-5](06-epic-lane.md) and each house's secrecy discipline — this clause doesn't alter the contours of E-5's closed prohibition list**
7. **Pulling an external tool or someone else's product into the core tree** — the maintenance burden falls on us permanently. Place it in a wrapper, an isolated location (e.g., a quarantined directory for staging, or an externally managed separate repo — these examples are non-normative), not in the core. This is a coupling-and-maintenance judgment, and closure is closure even when the quality is high

## R-4 Verify the Premise — Before Calling It a Bug

Watchword: **"If you can't point to the line where the bug appears, the premise is unverified"**

The biggest reason a well-made change gets refused isn't quality — it's that it's built on **a wrong premise**, or it's **treating intentional design as a defect**. The following 4 patterns cut both ways — they tell a review seat where to scrutinize, and they tell first-pass triage when not to close:

1. **It's intentional design, not a defect** — a limitation that looks like an oversight is often intentional. Before fixing, ask "isn't that isolation the design itself?" and read the original commit's intent
2. **The premise doesn't hold up against how the code actually behaves** — trace the actual code and its runtime behavior before accepting the claim. If you can't show which line's behavior the fix changes, it's unverified
3. **The absence was load-bearing** — adding a piece that's "obviously missing" can break what that omission was protecting
4. **Overreach, or reviving a policy that's already been settled past** — an extension beyond an agreed baseline, or rehashing a direction deliberately closed, gets refused even if it works. Keep the change to the narrow agreed part and propose the rest as a follow-up

Underlying theme: **verify both the claim and the intent against the codebase before writing, before merging**. A confirmed reproduction plus a line-level explanation always beats a plausible-sounding argument. When intent is unclear, it's cheaper to ask than to submit a fix that fights the design.

(Concrete examples may be swapped for each house's own incident records — the examples in the body are non-normative. When delegating a review, these 4 patterns can be front-loaded as the "name the worst failure mode" angle in [B-4](07-delegation-brief.md).)

## R-5 The Placement Ladder — Minimize Permanent Surface Area at the Lowest Rung

When building a new capability, lower rungs mean more permanent surface area (cost everyone keeps paying). **Choose the lowest-numbered rung that correctly solves the problem**:

1. **Extend existing code** — if it's a variant of something that already exists, the new surface is zero
2. **Script / skill** — an operation expressible in shell. No standing process — runs only when invoked
3. **Conditionally gated hook** — automation that appears only when its precondition is configured
4. **Add a feature to an existing repo** — if a place for it already exists, put it there
5. **Split into an MCP server or a separate repo** — for a truly independent capability, outside the core
6. **A new repo or new standing system** — last resort. **Requires the owner's (human's) approval**. If this arises while an Epic is running, **halt it as an ad-hoc checkpoint under [E-3](06-epic-lane.md)** (don't append it to E-3's table)

- When in doubt, go up a rung (minimize surface area). "The lower rung is easier" is not a reason
- **Once you choose a rung, decide the exit trigger for what you're placing, at the same time** ([LC-1](08-lifecycle.md) — the ladder decides where to place it, LC-1 decides how it exits. Use them as a pair)
- **A shared receiving interface on the 3rd instance of a kind** — once 3 integrations of the same category have accumulated, don't add them one at a time; design a shared interface and wrap the existing implementation as the first provider. Designing the receiving interface is a boundary change, so it rides on the boundary-PR-first rule of [L2-2](01-milestone-loop.md)

## R-6 Enforce Policy with a Check

**Don't leave a policy that must not be broken as a mere "please."** Passive rules (.gitignore, documentation, verbal agreements) only stop honest mistakes — a policy you want enforced should be promoted to a check that turns red when broken.

- **Promotion trigger**: once the same policy has been broken twice, file an Issue to build the check. **Keep a record of each break in an Issue or each house's incident record, and file the promotion Issue when the 2nd instance is recorded** (so the count can be verified after the fact)
- A check should **detect by substance** (match on the actual content/pattern, not on directory names or extension spelling — a real case of slipping through via a misspelling is in the source)
- Align a check's posture with existing articles: **a gate that blocks a merge is fail-closed** ([FP-3](05-fail-posture.md)'s direction), **reporting/aggregation/notification pipelines are fail-open** ([FP-4](05-fail-posture.md)). A check doesn't move files ([LC-5](08-lifecycle.md) — it only detects and stops; no auto-repair, no auto-retirement)
- An approval-type check (e.g., a human label) must **verify the approval actually exists** — don't pass it just because the text or label is present ([FP-8](05-fail-posture.md)'s direction). Verification of approval may have limits (e.g., a shared-identity environment) — in that case, state the limit explicitly in the check's description and don't pretend it's "verified" ([FP-5](05-fail-posture.md))
- The canonical form definitions live in this repo's `templates/ci/`
