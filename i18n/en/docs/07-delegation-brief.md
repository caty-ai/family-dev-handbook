> **Machine translation.** The Japanese original ([07-delegation-brief.md](../../../docs/07-delegation-brief.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# B Delegation Brief — Making a Single Delegation a Contract

Where the L layer (L2 / L1 / L0) is the contract between lanes and people, the B layer defines **the contract for the request text when an agent hands off a single piece of work to a subagent (an implementation worker, a review seat, another CLI agent)**. Each rule carries a stable rule ID (`B-1` through `B-5`). The summary side ([docs/04](04-adoption.md)) references these IDs. The canonical template lives at [templates/brief-template.md](../templates/brief-template.md). For the stance to take when verification isn't possible, see [docs/05](05-fail-posture.md).

Background: lane handoffs are protected by the Issue as SoT ([L1-1](02-issue-loop.md)), but **the quality of each individual delegation can't be protected by lane discipline alone**. The delegate doesn't have your conversation history (fresh context) — anything not written in the request text might as well not exist. The B layer turns the request text itself into a small contract.

## B-1 The Mandatory 3-Layer Brief Structure

A request for a substantive delegation (one involving implementation, modification, or generation of code or documentation) must always include the following three sections:

1. **Implementation Spec (Goal)** — the goal, constraints, front-loaded context, and the scope that may be touched
2. **Implementation Check (Self-verification)** — the verification checklist the worker runs on themselves before delivery
3. **Review Criteria (Reviewer criteria)** — what the downstream review will look at

Reason: handing over the spec alone makes "it's done" unverifiable. By handing over, **at the point of delegation**, what counts as done (self-verification) and what to scrutinize (review criteria), the deliverable can be judged by evidence rather than by claim (the same direction as [L1-7](02-issue-loop.md)).

Note: a brief that includes a code change must include, in its Implementation Check, **"tests added or changed, and their results" as a standard item** ([T-3](10-test-ci-baseline.md). If no test was added, report the reason per T-3's closed enumeration).

## B-2 Applicability — When In Doubt, Include It

- **Mandatory**: delegations involving implementation, modification, or generation. Include it even at size S, as long as the output stays in the repository
- **Exempt**: read-only searches, look-ups, short questions (where the output is read once and discarded)
- When in doubt, include it (err heavy — the same stance as the weight judgment in [L2-1](01-milestone-loop.md))

## B-3 The Issue Is Canonical — the Brief Is Derived

- The brief's Goal / Done when / touchable scope are derived from the assigned Issue's **Why / Done when / predicted files to touch** ([L1-2](02-issue-loop.md))
- If the brief and the Issue disagree, **the Issue wins**. Whoever notices the discrepancy fixes the Issue first, then delegates — never let them silently diverge (the same direction as [L1-8](02-issue-loop.md))
- It's normal for one Issue to produce multiple briefs (separate briefs for implementation, fix rounds, and review seats)

## B-4 Front-Load Context — Don't Make Them Go Exploring

- Front-load into the brief any facts the delegate needs (paths, specs, constraints, prohibitions, environment quirks). Don't rely on the delegate to explore for them
- Reason: exploration results vary by delegate. Read-only seats or sandboxed environments sometimes can't explore at all. Front-loading is the only way to get the same quality of outcome whether the context is fresh or read-only
- When delegating a review, **name the worst-case failure mode explicitly** ("the worst thing this change could do is cause X"). This gives a sharper target than "find bugs"
- For delegations that need blinding (independent review seats), **don't mix in** other seats' findings or your own prior analysis. What you front-load should be facts, not conclusions

## B-5 Keep the Format Machine-Checkable

- The three sections must stay in a form that **can be machine-judged by fixed heading strings** (don't dissolve them into free-form prose). Heading strings may be localized per household, but once decided, keep them fixed
- It's recommended to put a check on the delegation tool side (e.g., a hook) that blocks on missing sections before work starts. Implementing that check is out of scope for this handbook (it belongs to each household's tooling layer)
- **B-1 through B-4 remain valid as a contract even in environments without such a check** — fail-open does not mean "the format is optional" (the same direction as [docs/05](05-fail-posture.md))
