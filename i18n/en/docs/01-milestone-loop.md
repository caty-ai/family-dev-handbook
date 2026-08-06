> **Machine translation.** The Japanese original ([01-milestone-loop.md](../../../docs/01-milestone-loop.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# L2 Milestone Loop — the layer that decides whether parallel work is possible

This layer sits **above** the Issue loop (L1). It converts "what to build" into "who touches where," and decides whether parallel work is possible here before handing off to L1.
Each rule carries a stable rule ID (`L2-1` through `L2-6`). The summary side ([docs/04](04-adoption.md)) references these IDs.

## Why this layer is needed

There is exactly one condition under which splitting work is safe — **knowing before you start that the sets of files being touched don't intersect**.
worktrees and Issue locks (L0) are devices that contain the damage once a collision happens; what actually prevents the collision itself is agreeing on boundaries in advance. Skip this layer and run things in parallel, and two branches touching the same hotspot (a giant file) will collide for certain.

## Loop steps

### L2-1 Agree on the goal

- Nail down requirements through dialogue before starting (deep-interview, a planning session, or whatever method the agent has on hand)
- Question, at least once, any requirement that's making the design harder (for how to frame the question, see [Why We Build Simple](why-simple-systems.md)). Decisions to drop or narrow scope are made with the requester's agreement — never thin out the Done when without agreement. Complexity you questioned and then accepted still gets its reasoning recorded in the Issue's Why
- **Weight assessment**: a single bug fix / single feature = one Issue. A new feature / architecture change / multiple modules = **an EPIC Issue + child Issue breakdown + a linked GitHub Milestone**
- When in doubt, lean toward the heavier option. The deciding question is: "**Could this span multiple sessions / multiple agents?**"
- For how EPIC Issue work is run (integration branch, human checkpoints, hourglass review), see [docs/06 Epic Lane](06-epic-lane.md) (E-1 through E-10)

### L2-2 Determine architectural impact

Before starting, always ask: "**Does this work move a module boundary?**"

- **It doesn't** → go straight to Issue breakdown
- **It does** (module splits, directory reorganization, shared interface changes, etc.) → **land a single boundary PR first**
  - Until the boundary PR merges, **no new parallel work starts** in that repo (a serial-only window)
  - Keep the boundary PR itself minimal — don't mix boundary changes with feature changes
  - Within an Epic, the **contract-freeze child Issue #0** plays the role of the boundary PR ([E-2](06-epic-lane.md))

### L2-3 Issue breakdown — file predictions are mandatory

When cutting a child Issue, its body must always include the following ([template](../templates/issue-template.md)):

- **Purpose (Why)**
- **Completion criteria (Done when)**
- **Predicted files / modules touched** ← this feeds the parallel-GO decision. If it can't be predicted, state "unpredictable" explicitly (= that Issue cannot run in parallel)

### L2-4 Parallel-GO decision

Two Issues may run at the same time only if **their declared file sets don't intersect**.

- They intersect → run serially, in order
- Unpredictable → run serially, in order, or run an investigation spike first to make it predictable
- **Intersection can't be verified** (no declaration, malformed, or `UNKNOWN`) → serial (fail-closed — [FP-1](05-fail-posture.md))
- Still want to parallelize? → land a **boundary-separation Issue** first (a refactor that carves out the colliding part)

### L2-5 Isolate broad-scope Issues

Full-repo refactors, a complete design overhaul, blanket reformatting, bulk dependency upgrades, and similar work that **touches a wide swath of the repo run in isolation, alone**. While one is running, all parallel work in that repo stops.

Standard ordering: **clear the normal-feature Issues first → run the broad-scope Issue alone, last, as a batch**.

### L2-6 Invest in hotspots

Giant files that host too many responsibilities (e.g., a 2,500-line file mixing View + gestures + engine calls) are the single biggest enemy of parallel development.

- Keep a "**parallel-safety map**" in each repo's `ARCHITECTURE.md` that records module boundaries and hotspots ([template](../templates/architecture-parallel-map.md))
- File hotspot-splitting refactors as their own priority Issues, framed as "**an investment in parallelizability**" — once split, that area becomes structurally safe to parallelize
