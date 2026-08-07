> **Machine translation.** The Japanese original ([01-milestone-loop.md](../../../docs/01-milestone-loop.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# L2 Milestone Loop — the layer that decides whether parallel work is allowed

This layer sits **above** the Issue loop (L1). It converts "what to build" into "who touches what," and decides whether parallel work is allowed before handing things down to L1.
Each rule carries a stable rule ID (`L2-1` through `L2-6`). The summary side ([docs/04](04-adoption.md)) references these IDs.

## Why this layer is needed

There is exactly one condition under which splitting work across people is safe — **knowing before you start that the sets of files being touched don't overlap**.
worktrees and Issue locks (L0) are devices for containing the damage once a conflict happens; what actually prevents the conflict itself is agreeing on boundaries in advance. Skip this layer and run things in parallel, and two efforts touching the same hotspot (a giant file) will collide for certain.

## Loop steps

### L2-1 Agree on the goal

- Nail down the requirements through dialogue before starting (deep-interview, a planning session, or whatever method each agent already has on hand)
- Question, once, any requirement that's making the design harder (for how to frame that question, see [Why We Build Simple Systems](why-simple-systems.md)). Decisions to drop or narrow scope must have the requester's agreement — don't water down Done when without agreement. If you question a piece of complexity and still accept it, record the reason in the Issue's Why
- **Weight assessment (size classification)**: decide the size of the work — **S / M / L / H / Epic** — before starting (criteria below). Size feeds into the number of review seats ([L1-11](02-issue-loop.md)), whether an upstream cross-model review is required before implementation starts ([L1-9](02-issue-loop.md)), and the Epic entry gate ([E-1](06-epic-lane.md))
- Work classified as **Epic** gets an **EPIC Issue + child-Issue breakdown + a linked GitHub Milestone**. Operations (integration branch, human checkpoints, hourglass review) are covered in [docs/06 Epic Lane](06-epic-lane.md) (E-1 through E-10)

#### Size classification criteria

| Size | Definition |
|---|---|
| **S** | Local, low risk — roughly one file, a small fix to existing behavior |
| **M** | A single bug fix or single feature — self-contained within one module, doesn't move any boundary |
| **L** | Touches multiple modules, includes a change to a module boundary |
| **H** | New feature, architecture change, security, migration, or a change directly touching customers / the outside world |
| **Epic** | A bundle broken down into multiple Issues (comes into being only with the owner's kickoff approval = [E-1](06-epic-lane.md)) |

Judge along three axes. **In mixed cases touching more than one axis, the heavier axis wins** (e.g., "single feature but directly customer-facing" = H, "local but a migration" = H):

1. **Blast radius** — number of files / modules touched. Crossing or moving a module boundary means L or higher
2. **Irreversibility** — if it includes a hard-to-undo operation such as a migration, public release, or deletion, it's H
3. **Duration / headcount** — if it could span multiple sessions or multiple agents, it's an Epic candidate

There's also a supporting axis, **high-risk areas** (the canonical, single definition lives in [docs/06](06-epic-lane.md) — don't copy it here). This axis **raises the review seat count independently of size** — when it applies, seat count increases and takes priority over size ([L1-11](02-issue-loop.md)). Treat H in the size table and high-risk areas as distinct things.

- **Tie-breaking rule: when in doubt, go heavier**. When the axes don't settle it, or there isn't enough information, treat the work as one size heavier

### L2-2 Architecture-impact check

Before starting, always ask: "**Does this work move a module boundary?**"

- **No** → go straight to Issue breakdown
- **Yes** (module split, directory reorganization, shared-interface change, etc.) → **send a single boundary PR ahead of everything else**
  - Until the boundary PR merges, **no new parallel work starts** in that repo (a serial window)
  - Keep the boundary PR itself minimal — don't mix boundary changes with feature changes
  - Inside an Epic, the **contract-freeze child Issue #0** plays the role of the boundary PR ([E-2](06-epic-lane.md))

### L2-3 Issue breakdown — predicting touched files is mandatory

When cutting a child Issue, its body must always include the following ([template](../templates/issue-template.md)):

- **Purpose (Why)**
- **Completion criteria (Done when)**
- **Predicted files / modules touched** ← feeds directly into the parallel-GO decision. If it can't be predicted, say so explicitly as "unpredictable" (= that Issue cannot run in parallel)

### L2-4 Parallel-GO decision

Two Issues may run at the same time **only if their declared file sets don't overlap**.

- Overlap → run them serially, in order
- Unpredictable → run them serially, in order, or run a spike first to make it predictable
- **Overlap can't be verified** (no declaration, malformed, or `UNKNOWN`) → serial (fail-closed — [FP-1](05-fail-posture.md))
- If parallel is truly needed → land a **boundary-isolation Issue** first (a refactor that carves out the conflicting part)

### L2-5 Isolating broad-scope Issues

Issues that touch a wide swath of the repo — full rewrites, a complete design overhaul, bulk reformatting, a sweeping dependency update — **run alone**. All parallel work in that repo stops while one is running.

Standard ordering: **clear normal-feature Issues first → save broad-scope Issues for last and run them alone**.

### L2-6 Investing in hotspots

Giant files that host too many responsibilities (e.g., a 2,500-line view that also handles gestures and engine calls) are the biggest enemy of parallel development.

- Keep a "**parallel-safety map**" in each repo's `ARCHITECTURE.md` recording module boundaries and hotspots ([template](../templates/architecture-parallel-map.md))
- Prioritize hotspot-splitting refactors as standalone Issues, framed as "**investing in future parallelizability**" — once split, that area becomes structurally safe to parallelize
