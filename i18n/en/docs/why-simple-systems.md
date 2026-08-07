> **Machine translation.** The Japanese original ([why-simple-systems.md](../../../docs/why-simple-systems.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# Why Build Simple — Complexity Gets Removed at the Requirements Level, Not Solved by Design

> This page is not a rule. The rule text itself lives in [docs/01](01-milestone-loop.md)–[docs/03](03-git-protocol.md) and [docs/05](05-fail-posture.md)–[docs/08](08-lifecycle.md).
> What's written here is the **thinking those rules assume**.

## What we're aiming for

The rules in this handbook (L2 / L1 / L0) are a mechanism for protecting "how to build, how to run things in parallel." But there's a stage before that — **deciding what to build** — where fragility and maintenance weight are already locked in.

We're aiming for four things.

- **Simple and hard to break** — fewer parts means fewer places to break
- **Tolerant of neglect** — a long lead time before the next maintenance need, and no human attention required to keep it running
- **Understandable by anyone** — readable and traceable, without explanation, by your future self months later or by an agent seeing it for the first time. "Only the person who built it understands it" or "takes forever to decode later" is treated as a defect in itself
- **A module structure sized to the number of responsibilities** — split neither more nor less than the responsibilities warrant (measured the same way as "number of responsibilities" in [Why Cut Modules Small](why-small-modules.md))

## When you get stuck on design, question the requirements

While building, this happens sometimes:

- The logic has gotten impossibly convoluted
- Combining modules can't solve it, and some special mechanism seems necessary
- You're stuck on the design itself

The first move here is not "look for a smarter design." It's **questioning the requirement itself**.

Most difficulty is brought in by requirements, not design. If you can remove one requirement, the design difficulty that requirement demanded disappears entirely — along with the implementation, the tests, and all future maintenance for it. Design cleverness can only **dilute** difficulty; revisiting a requirement can **eliminate** it.

## Questions to ask when doubting a requirement

Ask these in order. None of them is "can we cut this requirement" — all of them are searching for whether **removing the premise removes the problem itself**.

1. **Who actually uses this?** — the broader you set the intended user base, the heavier authentication, permissions, error handling, and support become. Checking the actual users can reveal that most of that weight is unnecessary
2. **Does this really need to be online?** — if local execution or a closed network (e.g., a VPN) is enough, the login design, attack defenses, and availability design needed for public exposure never exist as a problem in the first place
3. **Can narrowing the use case remove the hard part?** — dropping "handle anything" in favor of limiting inputs or usage can wipe out branches that were previously intractable
4. **Did someone actually ask for this requirement?** — requirements added because "it seemed like it'd be nice to have" are the most expensive kind. Confirm the answer with whoever asked — a requirement recorded in an Issue is a record of past agreement, so it's not something an agent gets to unilaterally judge as "nobody asked for this" and remove

### Example: "Build us an internal SaaS tool"

Taken at face value, this kicks off design work for safe public exposure. Login, password reset, session management, permission tables — all of it hard, all of it fragile, all of it ongoing maintenance.

So go back to question 1: "Who uses this?" — if the answer is "just our own team," there's no need to expose it publicly at all. Run it locally or put it on a closed network, and **the login problem itself disappears**. One question asked before building removed the most fragile part entirely.

This is what "solving by removing the premise" means.

> **Note:** this is an example of "confirming the scope-of-users requirement before building" — not an argument for stripping authentication from a system that's meant to be public. Decisions touching boundaries like authentication, permissions, or public exposure — before building, and especially for a live system — fall under **high-risk areas** (the single definition in [docs/06](06-epic-lane.md)) and are subject to human sign-off.

## Questioning is free; the decision to remove belongs to the requester

This is the most important line to draw. **The output of questioning is not a requirement deletion — it's a question and a proposal that returns to goal agreement ([`L2-1`](01-milestone-loop.md)).**

- An agent can go as far as proposing alternatives. **The final call on what to drop belongs to whoever made the request**
- Don't let an agent unilaterally rewrite or dilute agreed-upon requirements or Done when on its own. Don't mark Done when as N/A on the grounds that "I questioned it and decided it was unnecessary"
- If you want to drop a requirement mid-work: don't rewrite Done when while proceeding with the implementation — **confirm with the requester on the Issue**. Once agreed, update the Why / Done when before resuming
- This is **not a substitute** for the standard way out of a stall. The proper exit when implementation gets stuck is HOLD under [`L1-4`](02-issue-loop.md) / [`L1-6`](02-issue-loop.md) or escalation to a human — not "question the requirement." **"Couldn't do it" and "turned out to be unnecessary" are different things and get recorded separately**
- Even when removing a requirement lightens the work, that is **not a way to dodge** review weight ([`L1-9`](02-issue-loop.md) / seat count). The agreement to remove something is itself a requirement change, and for heavier work it's subject to upstream review
- For heavier work this line is already drawn by the rules — requirements definition is subject to cross-model review before implementation starts ([`L1-9`](02-issue-loop.md)), and Done when inside an Epic is a frozen deliverable, where any change is a stop-point for a human checkpoint ([`E-3`](06-epic-lane.md)). This page doesn't loosen any of that

## Not everything can be done this way

Sometimes the requirement is real and the complexity is unavoidable. Regulatory compliance, audit logs, personal-data protection, billing — these are **requirements we don't have the freedom to remove in the first place**. They aren't something to question; they're something to confirm and satisfy. This page isn't saying "don't build complex things" — it's saying "**question the requirement at least once before accepting the complexity**."

If, after questioning, you accept it — that's fine. Just **leave one line in the Issue's purpose (Why) explaining why you accepted it** (see [`L1-2`](02-issue-loop.md) for how to write a Why). If it's recorded, someone months later can ask "is this complexity actually needed?" If it isn't recorded, the complexity becomes an unquestioned fait accompli.

## Relationship to the parallel-work rules

This premise connects to the world of the rules.

- Removing a requirement shrinks the set of files touched. A smaller file set makes the **files-to-touch prediction** ([`L2-3`](01-milestone-loop.md)) easier to write, which makes a parallel GO ([`L2-4`](01-milestone-loop.md)) more likely. A simple system is also a system that's strong under parallel development
- "A module structure sized to the number of responsibilities" uses the same judgment axis as [Splitting Is an Investment in Parallelizability](why-small-modules.md). Split when responsibilities are cohabiting (that page's concern); don't multiply parts when there's no responsibility driving it (this page's concern) — opposite directions, but both measured by **number of responsibilities**
- [`L2-1`](01-milestone-loop.md)'s "when in doubt, treat it as heavy" is a judgment about **process** (whether to make it an Epic, how thick the review is), not about adding features. "Light requirements, heavy process" can coexist
- Making the structure understandable by anyone shares the same motive as placing the canonical handoff record in the Issue ([Issue-first](why-issue-first.md)). The benchmark is **the next reader arriving with zero memory of this**

## Frequently asked questions

**Won't an agent use "questioning the requirement" as an excuse to cut requirements on its own?**

Reading this page that way is forbidden. Questioning means raising a question and proposing — nothing further. The decision to remove or narrow belongs to the requester (see "Questioning is free; the decision to remove belongs to the requester" above). Treat diluting Done when without agreement as the kind of deviation that gets exposed when checked against the completion record ([`L1-7`](02-issue-loop.md)).

**Isn't questioning a requirement disrespectful to whoever asked for it?**

What's being questioned isn't the requester — it's the translation between requirement and design. A question like "who uses this?" isn't haggling down the request; it's confirming the request's real purpose. If the purpose can still be met, less to build is better for whoever asked.

**Doesn't building simple mean you can't extend it later?**

Often the opposite is true. Mechanisms added ahead of time in anticipation of future extension usually end up unused because the actual extension comes from an unexpected direction — and all they do is get in the way of the reader's understanding. A structure that's small and easy to understand is the most adaptable kind of extensibility there is.

**When should you question a requirement?**

There are two moments. The first is before starting — when nailing down requirements during goal agreement ([`L2-1`](01-milestone-loop.md)). That's a dialogue with the requester, so asking there is enough. The second is mid-work — when the design starts getting convoluted or you feel stuck. The requester isn't present for that one, so per the line drawn above, an agent's job stops at "write the question in the Issue and confirm." Getting stuck tends to push both people and agents toward "an even more complicated solution." This page exists to stop that reflex.

## Where the rules live

| What you want to know | Rule |
|---|---|
| Where requirements get fixed (goal agreement, weight判定) | [`L2-1`](01-milestone-loop.md) |
| Where to record the reason for accepted complexity (Issue's Why) | [`L1-2`](02-issue-loop.md) |
| Files-to-touch prediction / parallel GO判定 | [`L2-3`](01-milestone-loop.md) / [`L2-4`](01-milestone-loop.md) |
| Checking Done when (where unilateral shrinking gets exposed) | [`L1-7`](02-issue-loop.md) |
| The proper path when stuck (HOLD) | [`L1-4`](02-issue-loop.md) / [`L1-6`](02-issue-loop.md) |
| Review of requirements definition (heavier-work territory) | [`L1-9`](02-issue-loop.md) |
| Done when inside an Epic is a frozen deliverable (changes stop for a human) | [`E-3`](06-epic-lane.md) |
| Splitting hotspots is an investment in parallelizability | [`L2-6`](01-milestone-loop.md) |
| In an Epic, one child Issue = one module | [`E-2`](06-epic-lane.md) |
| How to measure a module's "smallness" (number of responsibilities) | [Why Cut Modules Small](why-small-modules.md) |

Two more premises: [What Is Issue-First](why-issue-first.md) / [Why Cut Modules Small](why-small-modules.md)

Back to the front door: [README](../../../README.md)
