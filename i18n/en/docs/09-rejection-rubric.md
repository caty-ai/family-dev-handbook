> **Machine translation.** The Japanese original ([09-rejection-rubric.md](../../../docs/09-rejection-rubric.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# R Rejection Rubric — The Layer of What to Accept and What to Decline

Where the L layer (L2 / L1 / L0) is the contract for **how to proceed**, and the B layer is the contract for **how to request**, the R layer defines the contract of intent for **what gets merged and what gets declined**. It's used in two ways:

1. **For the builder** — so contributions (including agent-originated proposals, tasks, and PRs) can aim at the right target
2. **For first-pass triage** — as guidance on when it's safe to close something without human judgment, and just as importantly, when it must **not** be closed

Normativity differs by rule: **R-1 / R-4 / R-5 / R-6 are contracts**, while **R-2 / R-3 are criteria lists for acceptance judgment**, and any rejection grounded in R-2 / R-3 always routes through R-1's authority discipline (value judgments are the owner's call alone).

Each rule carries a stable rule ID (`R-1` through `R-6`), and its items are referenced as ①②③… (same format as [E-6](06-epic-lane.md)①). The summary side ([docs/04](04-adoption.md)) references these IDs. For the stance to take when verification isn't possible, see [docs/05](05-fail-posture.md).

Source: this chapter is an adaptation of the "Contribution Rubric" from NousResearch/hermes-agent's AGENTS.md (MIT).

## R-1 The 3 Grounds for Automatic Rejection — Value Judgments Are the Owner's Call Alone

**Applies to recorded proposals** (Issues, PRs, task proposals submitted as records). The only grounds on which these may be closed without human judgment are **the 3 mechanically black-and-white reasons**. Each reason only holds once its conditions and evidence are met:

1. **Already on main** (implemented on main) — point to the commit or line showing the behavior in question already exists on current main. "Something functionally similar exists" does not qualify (that's a value judgment = the owner's call)
2. **Cannot reproduce** (cannot reproduce) — **bug reports only**. Leave a record of the reproduction attempt against current main (commands/steps, observed results, date). Insufficient information is not grounds for rejection — ask and hold
3. **Incoherent** (incoherent) — contradictions, blanks, spam, or other cases where no substantive claim can be read out, and only **after one round of inquiry** still yields nothing readable. A proposal that's merely tedious to read does not qualify

- Rejection on grounds of value judgment — "we don't need this," "doesn't match direction," "out of scope" — is **the owner's (human's) call alone**. An agent may go as far as escalating with a recommendation and rationale (this applies equally to rejections grounded in R-2 / R-3 — they are not among the 3 grounds)
- **When in doubt, don't close** — closing is an exercise of authority, and when verification isn't possible, authority contracts (leaving it open, to the owner) ([FP-7](05-fail-posture.md)'s direction). First-pass triage's job is to read design intent and **avoid mistakenly closing a legitimate contribution**
- **Recording**: for a proposal where a lane was already stood up (WIP declared), termination follows [L1-4](02-issue-loop.md)'s 5-term vocabulary. **For a proposal rejected before a lane is stood up, don't use lane vocabulary** — record only the closing reason (one of the 3 grounds plus the evidence above, or a link to the owner's ruling)
- **Reopening is asymmetric**: a closure under the 3 grounds may be reopened without owner approval once new evidence appears (reopening moves in the direction of contracting authority)
- A proposal that touches any of R-4's 4 patterns is a classic case where automatic closure under the 3 grounds is **not safe** — escalate to a human
- Rejection decisions made while an Epic is running are routed to the owner **asynchronously, without stopping the lane** (don't add stop points beyond [E-3](06-epic-lane.md))

## R-2 Contributions We Welcome — 6 Items

1. **Fix a real bug, across its whole class** — reproduce the symptom on current main, point to the line where it appears, and fix the sibling call paths too, not just the one spot reported (the counterpart to R-4's watchword)
2. **Extend at the edges; conserve at the core** — contributions that extend the edges (features of individual products, individual homes) are welcome. Restraint applies only to the core (shared family infrastructure, the place everyone pays a permanent cost). "Minimize footprint" is about wiring into the core, not about whether a product may grow
3. **Declared refactors are welcome even with a large diff** — the check that "every line must trace back to the request" applies to functional changes; a request for a change declared as a refactor is itself the extraction (hotspot decomposition = the investment described in [L2-6](01-milestone-loop.md)). **What relaxes is only the suspicion attached to diff size** — the declared file set ([L0-2](03-git-protocol.md) default-deny) and the diff cross-check in [L1-7](02-issue-loop.md)④ never relax, refactor or not (a refactor passes by declaring a broad file-touch prediction, not by skipping the declaration). Solo execution of wide-scope refactors ([L2-5](01-milestone-loop.md)) and merge procedure ([L0-7](03-git-protocol.md)) apply unchanged as well
4. **Extend rather than duplicate** — before adding a new module, manager, or hook, check whether an existing tool already serves the purpose (placement is covered by R-5)
5. **Tests assert invariants** — check "how two pieces of data should relate to each other"; don't write change-detection tests that freeze a current value (a list, a count, a hardcoded version)
6. **Verify boundaries, propagation, and I/O along the real path** — changes touching resolution chains, config propagation, permission boundaries, or external I/O must produce E2E evidence exercising the actual path. A mock-only green is not "done." **This item is guidance on how to select evidence; the canonical merge-gate requirement remains [L1-7](02-issue-loop.md)** (this does not add new requirements)

## R-3 What We Decline Even When Well-Made — 7 Items

These are declined not on a quality bar but as **structural judgments**. Being well-made doesn't remove the reason for declining. **A rejection grounded in this rule is not among R-1's 3 grounds — enforcement always remains the owner's call**; an agent may go as far as flagging the suspicion and escalating:

1. **Speculative infrastructure** — hooks, callbacks, or extension points with no concrete consumer. If there's a stated real use case, it isn't speculative (the consumer may live in a different repo)
2. **Adding an environment variable for non-secret configuration** — the place for secrets (`.env`, etc.) is for secrets only. Behavioral settings (timeouts, thresholds, flags, display) belong in a config file
3. **A new skill, hook, or persistent system stood up when an existing tool would suffice** — a new addition with no record of having considered R-5's ladder from its smallest rung is declined
4. **A shortcut for lazy reading of something meant to be read in full** — don't add pagination or excerpt options to loaders for content an agent is meant to read completely (skills, prompts, runbooks). It leads to reading only the first page and skipping the rest
5. **A "fix" that breaks the function it was meant to protect** — a mitigation that kills the purpose of a feature is the wrong mitigation. Read the original commit's intent (`git log -p -S`) before restricting behavior
6. **Wiring without proof, or unauthorized non-secret telemetry** — code wired in without E2E proof, branches never exercised at runtime, or outbound telemetry/identifier attachment without an opt-in gate (**this includes non-secret usage information**). Sending secret information externally is not covered by this item — it follows **[E-5](06-epic-lane.md) and each home's secrecy discipline; this item does not alter the contour of E-5's closed prohibition list**
7. **Pulling an external tool or someone else's product into the core tree** — the maintenance burden then falls on us permanently. Place it in a wrapper or an isolated location (e.g., a quarantined directory for staging, or a separately-managed external repo — examples are non-normative), not in the core. This is a coupling and maintenance judgment; a close is a close even when the quality is high

## R-4 Verify Premises — Before You Call It a Bug

Watchword: **"If you can't point to the line where the bug appears, the premise is unverified."**

The biggest reason a well-made change gets declined isn't quality — it's that it's built on a **wrong premise**, or it **treats intentional design as a defect**. The following 4 patterns cut both ways — they tell review seats where to scrutinize, and they tell first-pass triage when *not* to close:

1. **It's intentional design, not a defect** — what looks like an oversight limitation is often deliberate. Before fixing, ask "isn't that isolation the design?" and read the original commit's intent
2. **The premise doesn't hold up against how the code actually behaves** — trace the real code and runtime behavior before accepting a claim at face value. If you can't show which line's behavior the fix changes, it's unverified
3. **The absence was load-bearing** — adding a piece that looks "obviously missing" can break whatever that omission was protecting
4. **Overreach, or the revival of a settled-past policy** — an extension beyond the agreed baseline, or a rehash of a direction that was deliberately closed, gets declined even if it works. Keep the change to the narrowly agreed scope and propose the rest as a follow-up

Undertone: **verify both the claim and the intent against the codebase, before writing and before merging.** A confirmed reproduction plus a line-level explanation always beats a plausible-sounding argument. When intent is unclear, it's cheaper to ask than to ship a fix that fights the design.

(Concrete examples may be swapped for each home's own incident record — the examples in this text are non-normative. When delegating a review, these 4 patterns can be front-loaded into [B-4](07-delegation-brief.md)'s "name the worst failure mode" perspective.)

## R-5 The Placement Ladder — Minimize Permanent Surface Area at the Lowest Rung

When building a new capability, the lower the rung, the more permanent surface area (cost everyone keeps paying) it adds. **Pick the lowest-numbered rung that correctly solves the problem**:

1. **Extend existing code** — if it's a variant of something already there, the new surface is zero
2. **Script / skill** — an operation expressible as a shell action. No persistent process; runs only when invoked
3. **Conditionally-gated hook** — automation that appears only when its preconditions are configured
4. **Add a feature to an existing repo** — if a place for it already exists, put it there
5. **MCP server / separate repo** — for a truly independent capability, outside the core
6. **New repo / new persistent system** — last resort. **Requires owner (human) approval.** If this comes up while an Epic is running, **treat it as an ad-hoc checkpoint under [E-3](06-epic-lane.md)** and stop there (don't add it to E-3's published table)

- When in doubt, go up a rung (minimize surface area). "The lower rung is easier" is not a reason
- **When you pick a rung, decide the exit trigger for what you're placing, at the same time** ([LC-1](08-lifecycle.md) — the ladder decides where to place it, LC-1 decides how it leaves. Use them as a pair)
- **A third instance of the same kind gets a shared interface** — once three integrations of the same category have accumulated, don't add a fourth one-off; design a common interface and wrap the existing implementations as its first providers. Designing the interface is a boundary change, so it rides [L2-2](01-milestone-loop.md)'s boundary-PR-first rule

## R-6 Enforce Policy with a Check

**Don't leave a policy that must not be broken as a "please."** Passive rules (`.gitignore`, docs, verbal agreements) only stop honest mistakes — a policy you actually want enforced needs to be promoted to a check that turns red when broken.

- **Promotion trigger**: once the same policy has been broken twice, file an Issue to build the check. **Record each break in an Issue or the relevant home's incident record, and file the Issue at the second recorded break** (so the count can be verified after the fact)
- A check should **detect by substance** (match on the actual content/pattern, not directory names or extension spelling — a real case of a misspelling slipping through is the source for this)
- A check's posture should align with existing rules: **a gate that blocks a merge is fail-closed** ([FP-3](05-fail-posture.md)'s direction), **reporting/aggregation/notification plumbing is fail-open** ([FP-4](05-fail-posture.md)). A check doesn't move files ([LC-5](08-lifecycle.md) — it only detects and stops; no auto-repair, no auto-retirement)
- An approval-type check (e.g., a human label) must **verify the approval actually exists** — don't pass just because the text or label is present ([FP-8](05-fail-posture.md)'s direction). Approval verification may have limits (e.g., shared-identity environments) — in that case, state the limit explicitly in the check's description and don't pretend it's "verified" ([FP-5](05-fail-posture.md))
- The canonical types live in this repo's `templates/ci/` (set up in #18)
