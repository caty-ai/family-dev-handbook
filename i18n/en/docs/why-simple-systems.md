> **Machine translation.** The Japanese original ([why-simple-systems.md](../../../docs/why-simple-systems.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# Why We Build Simply — Complexity Is Removed Through Requirements, Not Solved Through Design

> This page is not a rule. The rules themselves live in [docs/01](01-milestone-loop.md) through [docs/06](06-epic-lane.md).
> What's written here is the **thinking those rules assume**.

## What We're Aiming For

The rules in this handbook (L2 / L1 / L0) are a mechanism for protecting "how to build" and "how to run things in parallel." But before that — at the stage of **deciding what to build** — some things are already settled. Fragility, and the weight of maintenance.

We're aiming for four states.

- **Simple and hard to break** — fewer parts means fewer places to break
- **Tolerant of neglect** — a long lead time before the next maintenance is needed. Keeping it running doesn't require human attention
- **Understandable by anyone** — readable and traceable without explanation, whether by your future self months later or by an agent seeing it for the first time. "Only the person who built it understands it" or "takes a long time to decode later" is treated as a defect in itself
- **A module structure with exactly as many modules as there are responsibilities** — split neither more nor fewer than the responsibilities call for (the same measure as "the number of responsibilities" in [Why We Cut Modules Small](why-small-modules.md))

## When You Get Stuck in Design, Question the Requirements

Partway through building, this happens:

- The logic has gotten unreasonably hard to follow
- It can't be solved by combining modules and seems to need some special mechanism
- You're stuck on the design itself

The first move here isn't "look for a smarter design." It's **questioning the requirement itself**.

Most difficulty is brought in by requirements, not by design. If you can remove one requirement, the design difficulty that requirement demanded disappears entirely — along with the implementation, the tests, and the future maintenance it would have needed. Clever design can only **dilute** difficulty. Revisiting requirements can **eliminate** it.

## Questions to Ask When Questioning

Ask them in order. None of these ask "can we cut a requirement?" — they all ask "**can we remove the premise and eliminate the problem itself?**"

1. **Who really uses this?** — the wider you set the intended user base, the thicker authentication, permissions, error handling, and support become. Once you check who actually uses it, you often find most of that thickness is unnecessary
2. **Does this really need to be online?** — if local execution or a closed network (a VPN, for instance) is enough, then login design for public exposure, attack countermeasures, and availability design never exist as problems in the first place
3. **Can narrowing the use case remove the hard part?** — dropping "handle anything" in favor of limiting inputs or usage can make a whole tangle of difficult branching disappear
4. **Did someone actually ask for this requirement?** — requirements added because "it seemed like it'd be nice to have" are the most expensive ones. Check the answer with whoever requested it — a requirement recorded in an Issue is a record of a past agreement, so it's not something an agent gets to unilaterally judge as "nobody asked for this" and remove

### Example: "Please build an internal SaaS"

Taken at face value, this kicks off design for safe public exposure. Login, password reset, session management, a permissions table — all of it difficult, all of it fragile, all of it ongoing maintenance.

So go back to question 1. "Who uses this?" — if the answer is "just our own team," there's no need to expose it publicly at all. Run it locally, or put it on a closed network, and **the login problem itself disappears**. One question asked before building removed the most fragile part entirely.

This is what "solving by removing the premise" means.

> **Note:** This is an example of "confirming the user-base requirement before building" — it is not about stripping authentication from a system that's meant to be public. Any decision touching the boundary of authentication, permissions, or public exposure — before building, and especially for a live system — falls under **high-risk areas** (the single definition in [docs/06](06-epic-lane.md)), and is subject to human decision-making.

## Questioning Is Free; the Decision to Remove Belongs to the Requester

This is the most important line to draw. **The output of questioning is not the deletion of a requirement — it's a "question" and a "proposal" that goes back to goal agreement ([`L2-1`](01-milestone-loop.md)).**

- An agent can go as far as offering alternatives. **The final decision on what to drop belongs to the requester**
- Don't let an agent unilaterally rewrite or dilute an agreed-upon requirement or Done when. Don't mark a Done when as N/A on the grounds that "we questioned it and judged it unnecessary"
- If you want to drop a requirement partway through: don't rewrite Done when while continuing implementation — **confirm with the requester on the Issue**. Once agreed, update the Why / Done when before resuming
- This is **not a substitute** for the standard way out of a stuck point. The proper exit when implementation is stuck is HOLD per [`L1-4`](02-issue-loop.md) / [`L1-6`](02-issue-loop.md) or escalation to a human — not "question the requirement." **"Couldn't do it" and "turned out to be unnecessary" are different things, and are recorded separately**
- Even when removing a requirement makes the work lighter, that is **not a way to dodge review weight** ([`L1-9`](02-issue-loop.md) / seat count). The agreement to remove something is itself a requirement change, and for heavier work it is subject to upstream review
- For heavy work, the rules already draw this line — requirements definition is subject to cross-model review before implementation starts ([`L1-9`](02-issue-loop.md)), and Done when inside an Epic is a frozen deliverable whose changes are subject to a human checkpoint stop ([`E-3`](06-epic-lane.md)). This page does not loosen that

## Not Everything Can Be Handled This Way

Sometimes the requirement is real and the complexity is unavoidable. Regulatory compliance, audit logs, protection of personal information, billing — these are **requirements we don't have the freedom to remove in the first place**. They aren't things to question; they're things to confirm and satisfy. This page isn't saying "don't build complex things." It's saying "**question the requirement at least once before accepting the complexity**."

If, having questioned it, you accept it — that's fine. Just **leave one line in the Issue's purpose (Why) explaining why you accepted it** (see [`L1-2`](02-issue-loop.md) for how to write a Why). If it's recorded, someone can reopen the question "is this complexity actually necessary?" months later. If it isn't recorded, the complexity becomes a fait accompli.

## Relationship to the Parallel-Work Rules

This premise connects to the world of the rules.

- Removing a requirement shrinks the set of files touched. A smaller set of files makes the **files-to-touch prediction** ([`L2-3`](01-milestone-loop.md)) easier to write, which makes a parallel GO ([`L2-4`](01-milestone-loop.md)) easier to get. A simple system is also a system that's strong under parallel development
- "A module structure with exactly as many modules as there are responsibilities" is the same judgment axis as [Splitting Is an Investment in Parallelizability](why-small-modules.md): split when responsibilities are cohabiting (that page's topic), don't add parts when there's no responsibility to justify them (this page's topic) — same yardstick, **number of responsibilities**, applied in opposite directions
- [`L2-1`](01-milestone-loop.md)'s "when in doubt, go heavy" is a judgment about **process** (whether to make it an Epic, how thick the review is) — it's not about adding features. "Light on requirements, heavy on process" can coexist
- Anyone being able to understand the structure shares the same motive as putting the canonical handoff record in the Issue ([Issue-first](why-issue-first.md)). The benchmark is **the next reader who walks in with zero memory of the work**

## Frequently Asked Questions

**Won't an agent use "questioning requirements" as an excuse to unilaterally cut them?**

Under this page's reading, that's forbidden. Questioning means raising a question and proposing — nothing further. The decision to remove or narrow belongs to the requester (see "Questioning Is Free; the Decision to Remove Belongs to the Requester" above). Diluting Done when without agreement should be treated as the kind of deviation that gets caught when cross-checked against the completion record ([`L1-7`](02-issue-loop.md)).

**Isn't questioning requirements disrespectful to the person who asked?**

What's being questioned isn't the requester — it's the translation between requirement and design. "Who uses this?" isn't a negotiation to lowball the request; it's work to confirm the request's actual purpose. If the purpose can still be met, building less is to the requester's benefit.

**Won't building simply make it impossible to extend later?**

Often the opposite happens. Mechanisms added in advance for future extension usually get used by an extension that arrives from an unexpected direction — never the anticipated one — and end up only getting in the reader's way of understanding. A structure that's small and easy to understand is the most adaptable kind of extensibility there is.

**When should requirements be questioned?**

Twice. First, before starting — when requirements are being locked in during goal agreement ([`L2-1`](01-milestone-loop.md)). This is a dialogue with the requester, so asking in the moment is enough. Second, partway through — when design starts to feel hard to follow, when you feel stuck. Here the requester isn't present, so per the line drawn above, the agent's job goes only as far as "write the question in the Issue and confirm." Getting stuck tends to push both people and agents toward "an even more complicated solution." This page exists to stop that reflex.

## Where the Rules Live

| What you want to know | Rule |
|---|---|
| Where requirements get locked in (goal agreement, weight judgment) | [`L2-1`](01-milestone-loop.md) |
| Where to record the reason for accepted complexity (the Issue's Why) | [`L1-2`](02-issue-loop.md) |
| Files-to-touch prediction, parallel GO judgment | [`L2-3`](01-milestone-loop.md) / [`L2-4`](01-milestone-loop.md) |
| Cross-checking Done when (where unauthorized shrinkage gets caught) | [`L1-7`](02-issue-loop.md) |
| The proper path when stuck (HOLD) | [`L1-4`](02-issue-loop.md) / [`L1-6`](02-issue-loop.md) |
| Review of requirements definition (heavier-side work) | [`L1-9`](02-issue-loop.md) |
| Done when inside an Epic is a frozen deliverable (changes require a human stop) | [`E-3`](06-epic-lane.md) |
| Splitting hotspots is an investment in parallelizability | [`L2-6`](01-milestone-loop.md) |
| In an Epic, one child Issue = one module | [`E-2`](06-epic-lane.md) |
| How to measure a module's "smallness" (number of responsibilities) | [Why We Cut Modules Small](why-small-modules.md) |

Two more premises: [What Is Issue-First](why-issue-first.md) / [Why We Cut Modules Small](why-small-modules.md)

Back to the front door: [README](../../../README.md)
