> **Machine translation.** The Japanese original ([why-small-modules.md](../../../docs/why-small-modules.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# Why Cut Modules Small — Splitting Is an "Investment in the Ability to Parallelize"

> This page is not a rule set. The rule text itself lives in [docs/01](01-milestone-loop.md)–[docs/03](03-git-protocol.md) and [docs/05](05-fail-posture.md)–[docs/08](08-lifecycle.md).
> What's written here is the **thinking those rules assume**.

## Whether work can be parallelized is decided before you start

The parallelization test in this handbook is simple: **if the set of files two pieces of work touch doesn't intersect, they can run in parallel** ([`L2-4`](01-milestone-loop.md)).

But what happens when a 2,500-line screen file has layout, gesture handling, and engine calls all living together? Whatever you try to do in that area, you'll always end up touching that file. **Everything intersects, so everything stays serial.**

The problem here isn't the test itself. **The way the code was cut makes it impossible to pass the test.**

In other words, "can this be parallelized" isn't decided by motivation or scheduling — it's decided long before anyone starts work. **The shape of the code sets the ceiling on how much can be parallelized.**

## Splitting is not "tidying up" — it's an investment

Splitting up a file is usually treated as a quality concern — "make it more readable," "make it cleaner" — and gets pushed behind feature work.

This handbook treats it differently. Splitting a giant file where multiple responsibilities live together (a **hotspot**) gets filed as its own priority Issue, treated as an **investment in the ability to parallelize** ([`L2-6`](01-milestone-loop.md)).

We call it an investment because it pays back in three ways.

**1. Parallel work becomes possible**

After the split, Issues touching that area stop intersecting with each other. **The moment you split it, parallel work in that area becomes structurally safe** ([`L2-6`](01-milestone-loop.md)). One split keeps paying off for every piece of work that comes after it.

**2. Agents can focus on the work in front of them**

A file with a single responsibility means an agent only has to read that one thing. **The less there is to read, the less attention gets scattered, and the more the agent can focus on just the task at hand.** Whatever model you're using, a narrower field of view makes it easier to run the task through to completion.

The reverse is also true: when three responsibilities share 2,500 lines, fixing just one of them means reading all three. Two unrelated responsibilities fill up the context every single time, whether you need them or not.

> **Note:** This isn't a requirement the rules impose — it's a design intent. We don't have numbers on how much it actually helps.

**3. Like blocks, pieces can be swapped out later**

When code is split by responsibility, a broken piece can be pulled out and fixed on its own when it breaks. It's closer to snapping a block in and out than touching everything around it.

This is also why this handbook includes "**revertability**" as a merge review criterion ([`L1-3`](02-issue-loop.md)), and why [`L2-2`](01-milestone-loop.md) says not to mix boundary changes with feature changes. When they're mixed together, you can no longer revert just one of them.

That's why splitting isn't "tidying up for later" — it's "investing up front."

## "Small" means number of responsibilities, not line count

If you think of a small module in terms of line count, you'll misjudge it. What matters is **how many responsibilities share the same space**.

A 300-line file with three responsibilities living together will still have three kinds of Issues intersecting there. A 1,000-line file with a single responsibility will only ever have Issues of the same kind intersecting.

That's why the hotspot table in the parallel-safety map ([templates/architecture-parallel-map.md](../templates/architecture-parallel-map.md)) has a column for "**responsibilities that live together**," not just a line-count guideline. Line count is a signpost, not the basis for the decision.

## When you move a boundary, do only that

Changing how modules are cut — moving a boundary — affects every other piece of work. So it's handled differently ([`L2-2`](01-milestone-loop.md)):

- A PR that moves a boundary gets merged **alone, first**
- Until it merges, no new parallel work starts in that repository (a serial window)
- **Keep the boundary PR itself minimal. Don't mix boundary changes with feature changes**

That last line is the one that actually matters in practice. When boundary changes and feature changes are mixed into one PR, a reviewer can no longer tell whether a given diff exists because of the boundary or because of the feature. And if a problem shows up later, there's no way to revert just the boundary.

## Where this gets written down

Each repository keeps a "parallel-safety map" in its `ARCHITECTURE.md` ([`L2-6`](01-milestone-loop.md); template at [templates/architecture-parallel-map.md](../templates/architecture-parallel-map.md)). It holds two tables:

- **A module boundary table** — which path owns which responsibility
- **A hotspot table** — which files carry multiple responsibilities, and which Issue is slated to split them

When a boundary-moving PR merges, **update this map in the same PR**. The moment the map drifts from reality, the evidence behind every parallel-GO decision becomes false.

## You don't have to design this yourself

Having read this far, you might think you need to design the module structure yourself. You don't.

**Hand this handbook to an agent, and the places that need splitting surface as Issues on their own.** Three mechanisms make that happen:

- **Every time an Issue is filed, it has to predict which files it will touch** ([`L2-3`](01-milestone-loop.md)). Work whose scope is too broad to predict gets treated as non-parallelizable on the spot. Where things are jammed up surfaces every time work happens
- **There's a fixed procedure for hitting a giant file** ([`L2-6`](01-milestone-loop.md)). It says "file the split Issue first," so the agent follows that step. No one has to decide from scratch each time
- **New code follows one child Issue = one module** ([`E-2`](06-epic-lane.md)). Responsibilities are far less likely to get tangled together from the start

That said, **the splitting work itself still has to happen**. Handing this over doesn't make the code tidy itself. What changes is that splitting stops being "tidying you'll get to eventually" and becomes "the path you're always routed through once you want to parallelize." **It stops being deferred** — that's the accurate way to put it.

## How this handbook itself is cut

This repository is built on the same principle.

- **One file per layer of rules** — L2 = [docs/01](01-milestone-loop.md), L1 = [docs/02](02-issue-loop.md), L0 = [docs/03](03-git-protocol.md), failure posture = [docs/05](05-fail-posture.md), Epic = [docs/06](06-epic-lane.md), delegation brief = [docs/07](07-delegation-brief.md), lifecycle = [docs/08](08-lifecycle.md). Even the longest one is only just over 100 lines
- **Rules and templates stay separate** — comment formats and templates live in [templates/](../templates/issue-template.md)
- **Cross-references use stable rule IDs** — files point at each other with IDs like `L2-4`. Moving a file doesn't break the references
- **No definition lives in two places** — the definition of high-risk areas lives only in [docs/06](06-epic-lane.md), and the distribution summary block lives only in [docs/04](04-adoption.md)

That last point matters the most. When a definition exists in two places, the moment only one of them gets fixed, nobody can tell which one is right anymore. That's why we decide up front that there's exactly one source of truth, and everything else is just a reference. It's the same reason the README doesn't carry a roadmap and instead hands that off to the Issue list.

## Common questions

**I can't cut things perfectly from the start.**

You won't be able to. That's exactly why we call it an "investment." If the current cut causes intersections, file it as a split Issue and pay it back one step at a time. You don't have to get everything right before you start.

**What happens if I cut things too small?**

The file count grows, and a single change ends up scattered across many files. You end up with a different problem — nothing intersects, but you're touching everything anyway — and reviews get harder to follow. The yardstick is the number of responsibilities, so **if there's only one responsibility, don't split it**.

**What do I do about an existing giant file?**

You don't have to touch it right now. Record it in the hotspot table of the parallel-safety map, and file the split Issue first once you actually want to parallelize work in that area. Recording it is itself a handoff to whoever makes that call next.

**Does this even matter if I'm developing alone?**

It does. The moment you run two AI agents, that's parallel development. On top of that, the more cleanly responsibilities are separated, the easier it is to write the "predicted files touched" for any given Issue — which also brings down the cost of the third item in [Issue-first](why-issue-first.md).

## Where the rules live

| What you want to know | Rule |
|---|---|
| Parallel-GO if the touched file sets don't intersect | [`L2-4`](01-milestone-loop.md) |
| When moving a boundary, merge one boundary PR first, alone | [`L2-2`](01-milestone-loop.md) |
| Splitting hotspots is an investment in the ability to parallelize | [`L2-6`](01-milestone-loop.md) |
| Wide-scope changes (full rewrites, etc.) run solo | [`L2-5`](01-milestone-loop.md) |
| In an Epic, one child Issue = one module | [`E-2`](06-epic-lane.md) |
| Parallel-safety map template | [templates/architecture-parallel-map.md](../templates/architecture-parallel-map.md) |

Two more foundational pieces: [What is Issue-first](why-issue-first.md) / [Why build simple](why-simple-systems.md)

Back to the front door: [README](../../../README.md)
