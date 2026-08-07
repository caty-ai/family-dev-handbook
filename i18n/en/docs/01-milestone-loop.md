> **Machine translation.** The Japanese original ([01-milestone-loop.md](../../../docs/01-milestone-loop.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# L2 Milestone Loop — the layer that decides whether parallel work is possible

The layer placed **above** the Issue loop (L1). It converts "what to build" into "who touches where," decides whether parallel work is possible right here, and only then hands things down to L1.
Each rule carries a stable rule ID (`L2-1` through `L2-6`). The summary side ([docs/04](04-adoption.md)) references these IDs.

## Why this layer is needed

There is exactly one condition under which splitting work is safe — **knowing before you start that the sets of files each side touches don't overlap.**
worktrees and Issue locks (L0) are devices that limit the damage once a collision happens; what actually prevents the collision itself is agreeing on boundaries up front. Skip this layer and run things in parallel, and two efforts touching the same hotspot (a giant file) will collide for certain.

## Loop steps

### L2-1 Goal agreement

- Nail down requirements through dialogue before starting (deep-interview / planning sessions / whatever method each agent already has on hand)
- Question, once, any requirement that's making the design harder (for how to frame the question, see [Why We Build Simple](why-simple-systems.md)). Decisions to cut or narrow scope are made with the requester's agreement — don't water down Done when without agreement. If you question a piece of complexity and still accept it, record the reason in the Issue's Why
- **Weight assessment (size classification)**: decide the size of the work as **S / M / L / H / Epic** before starting (criteria below). Size feeds into the number of review seats ([L1-11](02-issue-loop.md)), whether an upstream cross-model review is required before implementation starts ([L1-9](02-issue-loop.md)), and the Epic entry gate ([E-1](06-epic-lane.md))
- Work classified as **Epic** gets **an EPIC Issue + child-Issue decomposition + a linked GitHub Milestone**. Operations (integration branch, human checkpoints, hourglass review) are covered in [docs/06 Epic Lane](06-epic-lane.md) (E-1 through E-10)

#### Size classification criteria

| Size | Definition |
|---|---|
| **S** | Localized — roughly one file, a small fix to existing behavior |
| **M** | A single bug fix, a one-off change within an existing feature — self-contained within one module, doesn't move boundaries |
| **L** | Touches multiple modules, includes a module-boundary change |
| **H** | A new feature (something that stands as new user value), an architecture change, security, migration, a change directly tied to customers / external parties |
| **Epic** | A bundle that decomposes into multiple Issues (becomes official only with the owner's kickoff approval = [E-1](06-epic-lane.md)) |

Judge along three axes. **For mixed cases touching multiple axes, the heavier axis wins** (e.g., "single feature but directly tied to external parties" = H, "localized but a migration" = H):

1. **Blast radius** — the number of files / modules touched. Crossing or moving a module boundary means L or higher
2. **Irreversibility** — if it includes hard-to-undo operations like migrations, external releases, or deletions, it's H
3. **Duration / headcount** — if it could span multiple sessions / multiple agents, it's an Epic candidate

There's also a supporting axis, **high-risk area** (the canonical single definition lives in [docs/06](06-epic-lane.md) — don't copy it here). This is an axis that **raises the review seat count independently of size** — when it applies, seat count increases and takes priority over size ([L1-11](02-issue-loop.md)). Treat H on the size table and a high-risk area as distinct things (a change can qualify under both axes at once — size sets the base seat count, and high-risk-area status adds on top).

- **Tie-break rule: when in doubt, go heavier**. When the axes don't resolve a clean judgment, or there isn't enough information, treat it as one size heavier **within the S–H range**. This ladder never promotes something to Epic — that's decided solely by whether it needs decomposition into multiple Issues (axis 3, [E-1](06-epic-lane.md))

### L2-2 Architecture impact assessment

Always ask before starting: "**Does this work move a module boundary?**"

- **No** → go straight to Issue decomposition
- **Yes** (module split, directory reorganization, shared interface change, etc.) → **run a single boundary PR first**
  - Until the boundary PR merges, **halt all new parallel work** in that repo (a serial window)
  - Keep the boundary PR itself minimal — don't mix boundary changes with feature changes
  - Inside an Epic, **child Issue #0, the contract freeze**, plays the role of the boundary PR ([E-2](06-epic-lane.md))

### L2-3 Issue decomposition — mandatory file-touch prediction

When cutting a child Issue, its body must always include the following ([template](../templates/issue-template.md)):

- **Purpose (Why)**
- **Completion criteria (Done when)**
- **Predicted files / modules touched** ← feeds the parallel-GO decision. If it can't be predicted, state "unpredictable" explicitly (= that Issue cannot run in parallel)

### L2-4 Parallel-GO decision

Two Issues may run at the same time **only if their declared file sets don't intersect.**

- If they intersect → run serially, in order
- If unpredictable → run serially, in order, or run an investigative spike first to make it predictable
- **If the intersection can't be verified** (no declaration, malformed, `UNKNOWN`) → run serially (fail-closed — [FP-1](05-fail-posture.md))
- If you still need parallelism → land **a boundary-separation Issue** first (a refactor that carves out the colliding part)

### L2-5 Isolating broad-scope Issues

Full rewrites, complete design overhauls, mass reformatting, sweeping dependency updates, and similar — **Issues that touch a wide swath of the repo run alone.** While one is running, halt all parallel work in that repo entirely.

Standard ordering: **clear normal feature Issues first → save broad-scope Issues for last, run solo.**

### L2-6 Investing in hotspots

A giant file carrying too many responsibilities at once (e.g., a 2,500-line view doing gestures and engine calls) is the biggest enemy of parallel development.

- Keep a "**parallel-safety map**" in each repo's `ARCHITECTURE.md` recording module boundaries and hotspots ([template](../templates/architecture-parallel-map.md))
- Prioritize splitting-refactor work on hotspots as its own Issue, framed as "**an investment in future parallelizability**" — once split, that area becomes structurally safe for parallel work
