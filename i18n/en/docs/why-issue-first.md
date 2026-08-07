> **Machine translation.** The Japanese original ([why-issue-first.md](../../../docs/why-issue-first.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# What Issue-first means — why start from an Issue, not a conversation

> This page isn't a rule. The rules themselves live in [docs/01](01-milestone-loop.md) through [docs/06](06-epic-lane.md).
> What's written here is the **thinking those rules assume**. It's for anyone who wants to know why before memorizing the rules.

## What happens when you give instructions in conversation

You ask an AI agent to "go fix that bug." It gets fixed. The next day, you open a new session.

The agent remembers nothing about yesterday. What got fixed, why that particular fix was chosen, how far it was verified — all of that vanished along with the closed terminal. All that remains is the code change; the judgment behind it is gone.

Something similar happens between humans too. Decisions made in chat scroll off into the distance. The difference is that with AI, you can't even ask it to "remember." **Every session starts from zero memory.**

And these days, it's not just one agent. When two are running at once, they have no way of knowing what the other is doing, and they end up touching the same files.

## What Issue-first is

There's exactly one thing to do.

**Before touching code, open a single GitHub Issue.**

That's it. No special tools, no extra services required. Implementation starts once the Issue exists. There's no implementation without an Issue.

## Why it works

Opening an Issue **fixes the single source of truth for handoff in one place.**

When the work is done, two things remain: the Issue body (what was being attempted, what "done" looks like) and the Pull Request diff (what actually changed). With both of these in place, whoever comes in partway through — a different person, a different agent, or tomorrow's memory-wiped version of yourself — can pick up where things left off just by reading the Issue.

Conversation history disappears. An agent's memory disappears. **Issues and PRs don't disappear.** So that's where the single source of truth lives.

This isn't about trust — it's about where things are stored. It's not that someone writes an Issue because they're forgetful; it's that you **decide on one storage location that assumes forgetting will happen.**

## What goes in an Issue

Only three things are required (rule [`L1-2`](02-issue-loop.md)). The canonical template lives at [templates/issue-template.md](../templates/issue-template.md).

**1. Purpose (Why)** — why you're doing this. What breaks if you don't.

You write this for yourself a few days from now, and for the next agent that walks in tomorrow. If the reason you decided to do this isn't recorded, there's nowhere to go back to when judgment calls diverge partway through.

**2. Done when** — what "finished" looks like.

Write it as checkboxes, in a form **a machine or a real device can judge**. Not "it works properly" but "the test passes" or "it renders on the actual device." This is the only way to make "I'm done" verifiable. Because this exists, you can check PASS/FAIL against it item by item at merge time ([`L1-7`](02-issue-loop.md)).

**3. Predicted files/modules touched** — which files you expect to touch.

This item isn't for you — it's **for other work**. If you know before starting that two pieces of work touch non-overlapping sets of files, you can proceed in parallel. If you don't know, you don't parallelize ([`L2-3`](01-milestone-loop.md) / [`L2-4`](01-milestone-loop.md)). It's a prediction, so it's fine if it's wrong — you re-declare the final version when you actually start.

## When you don't need an Issue

Not everything needs an Issue. The following are exempt ([`L1-1`](02-issue-loop.md)):

- A one-line typo fix
- Non-code files (md / json / yaml, etc.)
- Scratch work outside git's reach
- Exploration, reading, conversation (work that changes nothing)

When unsure, think of it this way: **if it might span multiple sessions, open an Issue.** If it wraps up on the spot, you don't need one.

## What changes when you pair it with AI

Issue-first isn't a concept invented for AI. It's an approach software development has used for a long time. But pairing it with AI agents multiplies its value, for three reasons.

- **Memory starts at zero** — a human has "oh right, last week..." — an agent doesn't. The Issue becomes its only memory
- **Multiple agents run at once** — without declaring who's touching what, collisions become a matter of luck
- **"I'm done" is self-reported** — the only way to prevent unverified completion reports is to write the completion criteria before starting

## Common questions

**Do I need an Issue even for small fixes?**

No. See "When you don't need an Issue" above. The rule of thumb is whether it might span multiple sessions.

**Won't this create too many Issues?**

Yes, it will. But the problem is Issues left open, not Issues that are closed — closed Issues are useful as records. The reason lane state is expressed with only five words (WIP / HOLD / MERGED / SUPERSEDED / ABANDONED) is to make open versus finished distinguishable at a glance ([`L1-4`](02-issue-loop.md)).

**Does this matter if I'm developing solo?**

Yes, if you're using agents. Even solo, handoff happens the moment you cross a session boundary. Conversely, if all your work finishes within a single session, Issue-first buys you almost nothing.

**Isn't writing the Issue a waste of time?**

You're writing three items. Skip them, and you'll later spend time reconstructing "wait, what did I actually verify?" or "how far did I get?" Which one costs more depends on how long the work is — the shorter the work, the less you need an Issue. That's exactly why "when you don't need one" is decided up front.

## Where the rules live

| What you want to know | Rule |
|---|---|
| The Issue-first principle itself, scope of exceptions | [`L1-1`](02-issue-loop.md) |
| The three required parts of an Issue body | [`L1-2`](02-issue-loop.md) |
| How the file-touch prediction gets used (parallel or not) | [`L2-3`](01-milestone-loop.md) / [`L2-4`](01-milestone-loop.md) |
| The five words that express lane state | [`L1-4`](02-issue-loop.md) |
| How completion criteria get checked against at merge | [`L1-7`](02-issue-loop.md) |
| Issue comment templates (WIP / HOLD / completion record, etc.) | [templates/issue-template.md](../templates/issue-template.md) |

Two more foundational pieces: [Why cut modules small](why-small-modules.md) / [Why build simple](why-simple-systems.md)

Back to the front door: [README](../../../README.md)
