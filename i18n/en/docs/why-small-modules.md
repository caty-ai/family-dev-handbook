> **Machine translation.** The Japanese original ([why-small-modules.md](../../../docs/why-small-modules.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# Why We Cut Modules Small — Splitting Is an "Investment in Parallelizability"

> This page is not a set of rules. The rules themselves live in [docs/01](01-milestone-loop.md) through [docs/06](06-epic-lane.md).
> What's written here is the **thinking those rules assume**.

## Whether work can run in parallel is decided before you start

The parallelization test in this handbook is simple. **If the set of files two pieces of work touch doesn't overlap, they can run in parallel** ([`L2-4`](01-milestone-loop.md)).

But what happens when a 2,500-line screen file has layout, gesture handling, and engine calls all living together? Whatever you try to do in that area, you'll always end up touching that file. **No matter what you do, it overlaps — so it's always serial.**

The problem here isn't the test itself. **It's that the way the code was split makes it impossible to pass the test.**

In other words, "whether work can run in parallel" isn't decided by motivation or scheduling — it's decided long before anyone starts. **The shape of the code sets the ceiling on parallelizability.**

## Splitting isn't "tidying up" — it's an investment

Normally, splitting refactors are treated as a quality concern — "make it more readable," "clean it up" — and get pushed behind feature work.

This handbook treats it differently. Splitting a giant file where multiple responsibilities live together (a **hotspot**) is filed as its own priority Issue, treated as **an investment in parallelizability** ([`L2-6`](01-milestone-loop.md)).

We call it an investment because it pays back in three ways.

**1. Parallel work becomes possible**

Once split, Issues touching that area stop overlapping with each other. **The moment you split it, parallel work in that area becomes structurally safe** ([`L2-6`](01-milestone-loop.md)). One split keeps paying off for every piece of work that follows.

**2. Agents can focus on the work in front of them**

A file with a single responsibility means an agent only has to read that one thing. **The less there is to read, the less attention gets scattered, and the more the agent can focus purely on the task at hand.** Whatever model you're using, a narrower field of view makes it easier to see the work through to the end.

The reverse is also true: when three responsibilities are crammed into 2,500 lines, fixing just one of them still means reading all three. Two unrelated responsibilities fill up the context every single time.

> **Note:** This isn't a requirement the rules impose — it's a design intention. We don't have numbers measuring exactly how much it helps.

**3. Pieces can be swapped out later, like blocks**

When code is split by responsibility, a break in one piece can be pulled out and fixed without touching anything else. It's close to snapping a block in and out — you don't have to reach into the surroundings.

This is also why this handbook builds "**revert-ability**" into its merge review criteria ([`L1-3`](02-issue-loop.md)), and why [`L2-2`](01-milestone-loop.md) says "don't mix boundary changes with feature changes." The reasoning is the same: once they're mixed, you can't roll back just one of them.

So splitting isn't "cleanup for later" — it's "investment done first."

## "Small" isn't about line count — it's about how many responsibilities live there

If you think of a small module in terms of line count, you'll get the judgment wrong. What matters is **how many responsibilities are co-located**.

A 300-line file with three responsibilities living together will have three kinds of Issues overlapping there. A 1,000-line file with a single responsibility will only ever overlap with Issues of that same kind.

That's why the hotspot table in the parallel-safety map ([templates/architecture-parallel-map.md](../templates/architecture-parallel-map.md)) has a column for "**responsibilities living here**," not just a line-count guideline. Line count is a signpost, not the basis for the decision.

## When you move a boundary, that's all you do

Work that changes how a module is split — moving a boundary — affects every other piece of work. So it's handled differently ([`L2-2`](01-milestone-loop.md)).

- A PR that moves a boundary gets merged **alone, first, before anything else**
- Until it merges, no new parallel work starts in that repository (a serial window)
- **Keep the boundary PR itself minimal. Don't mix boundary changes with feature changes**

That last line is what actually matters in practice. When a boundary change and a feature change are mixed into one PR, the reviewer can't tell whether a given diff exists because of the boundary or because of the feature. And if a problem shows up later, you can't roll back just the boundary.

## Where this gets recorded

Each repository keeps a "parallel-safety map" in its `ARCHITECTURE.md` ([`L2-6`](01-milestone-loop.md); template at [templates/architecture-parallel-map.md](../templates/architecture-parallel-map.md)). It holds two tables.

- **Module boundary table** — which path owns which responsibility
- **Hotspot table** — which files carry multiple responsibilities, and which Issue is slated to split them

When a boundary-moving PR merges, **update this map in the same PR**. The moment the map drifts from reality, the evidence behind every parallel-GO decision becomes a lie.

## You don't have to design this yourself

Reading this far, you might think you're on the hook for doing module design yourself. You're not.

**Hand this handbook to an agent, and the places that need splitting will surface as Issues on their own.** There are three mechanisms behind this.

- **Every time an Issue is filed, it must predict the files it will touch** ([`L2-3`](01-milestone-loop.md)). Work whose scope is too broad to predict is treated as non-parallelizable right there. Where things are jammed up surfaces with every single piece of work
- **There's a fixed procedure for hitting a giant file** ([`L2-6`](01-milestone-loop.md)). Because it says "file the split Issue first," the agent just follows that procedure. It doesn't have to judge from scratch every time
- **When building something new, it's 1 child Issue = 1 module** ([`E-2`](06-epic-lane.md)). Responsibilities are far less likely to get mixed together from the start

That said, **the splitting work itself still has to happen**. Feeding the handbook in doesn't tidy the code by itself. What changes is that splitting stops being "cleanup for someday" and becomes "the path you're always forced down the moment you want to parallelize." The accurate way to put it: **it stops getting deferred**.

## How this handbook itself is split

This repository is built on the same principle.

- **One file per layer of rules** — L2 = [docs/01](01-milestone-loop.md), L1 = [docs/02](02-issue-loop.md), L0 = [docs/03](03-git-protocol.md), failure posture = [docs/05](05-fail-posture.md), Epic = [docs/06](06-epic-lane.md). Even the longest one is just over 100 lines
- **Rules and templates stay separate** — comment formats and templates live under [templates/](../templates/issue-template.md)
- **References use stable rule IDs** — files point to each other with IDs like `L2-4`. Moving a file doesn't break the reference
- **The same definition never lives in two places** — the definition of high-risk areas lives only in [docs/06](06-epic-lane.md), and the distribution summary block lives only in [docs/04](04-adoption.md)

That last point matters the most. If a definition lives in two places, the moment one of them gets fixed, nobody can tell which one is correct anymore. So we decide up front that there's exactly one source of truth, and everything else just points to it. It's the same reason the README doesn't carry a roadmap — it just hands off to the Issue list.

## Common questions

**I can't get the split right from the start.**

You won't. That's why we call it an "investment." If the current split causes overlap, file that as a split Issue and pay it down over time. You don't need everything sorted before you start.

**What if I split things too small?**

The file count grows, and a single change ends up scattered across many files. Now you're in a state where things don't overlap, but touch everywhere — which makes review harder to follow. Since the judgment call is based on the number of responsibilities, **if there's only one responsibility, don't split it**.

**What do I do about an existing giant file?**

You don't have to touch it right now. Record it in the hotspot table of the parallel-safety map, and file the split Issue first once you actually want to parallelize work in that area. Recording it is itself a handoff to whoever makes that call next.

**Does any of this even matter if I'm developing alone?**

It does. The moment you run two AI agents, that's parallel development. On top of that, the more cleanly responsibilities are separated, the easier it is to write the "predicted files to touch" for a given Issue — which also lowers the cost of the third item in [Issue-first](why-issue-first.md).

## Where the rules live

| What you want to know | Rule |
|---|---|
| Parallel-GO if the sets of touched files don't overlap | [`L2-4`](01-milestone-loop.md) |
| When moving a boundary, merge one boundary PR first, alone | [`L2-2`](01-milestone-loop.md) |
| Splitting hotspots is an investment in parallelizability | [`L2-6`](01-milestone-loop.md) |
| Broad changes (e.g. sweeping refactors) run solo | [`L2-5`](01-milestone-loop.md) |
| In an Epic, 1 child Issue = 1 module | [`E-2`](06-epic-lane.md) |
| Parallel-safety map template | [templates/architecture-parallel-map.md](../templates/architecture-parallel-map.md) |

Two more premises: [What is Issue-first](why-issue-first.md) / [Why we build simple systems](why-simple-systems.md)

Back to the front door: [README](../../../README.md)
