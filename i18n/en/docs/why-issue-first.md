> **Machine translation.** The Japanese original ([why-issue-first.md](../../../docs/why-issue-first.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# What is Issue-first — why start from an Issue, not a conversation

> This page is not a set of rules. The rules themselves live in [docs/01](01-milestone-loop.md)–[docs/03](03-git-protocol.md) and [docs/05](05-fail-posture.md)–[docs/08](08-lifecycle.md).
> What's written here is the **thinking those rules assume**. It's for people who want to know why the rules are the way they are before memorizing them.

## What happens when you give instructions in conversation

You ask an AI agent to "fix that bug." It gets fixed. The next day, you open a new session.

The agent remembers nothing about yesterday. What got fixed, why it was fixed that way, how far it was verified — all of it vanished along with the closed terminal. What remains is the code change itself, not the judgment that led to it.

Something similar happens between humans. Things decided in chat scroll off into the distance. The difference is that with AI, you can't even ask it to "remember." **Every session starts from zero memory.**

And now there isn't necessarily just one agent. When two run at the same time, they have no way of knowing what the other is doing, and they end up touching the same files.

## What Issue-first is

There's exactly one thing to do.

**Before touching code, open a single GitHub Issue.**

That's it. No special tools, no extra services required. Implementation starts once the Issue exists. There's no implementation without an Issue.

## Why it works

Opening an Issue **fixes the single source of truth for handoff in one place.**

When the work is done, two things remain: the Issue body (what was intended, and what counts as done) and the Pull Request diff (what actually changed). With both of these in place, anyone who joins midstream — a different person, a different agent, or tomorrow's memory-wiped version of yourself — can pick up where things left off just by reading the Issue.

Conversation history disappears. An agent's memory disappears. **The Issue and the PR don't disappear.** So that's where the single source of truth lives.

This isn't about trust — it's about where things are kept. You don't write an Issue because someone is forgetful; you decide on **one place to keep things, built on the assumption that everyone forgets.**

## What to write in the Issue

Only three things are required (in the rules, [`L1-2`](02-issue-loop.md)). The canonical template is at [templates/issue-template.md](../templates/issue-template.md).

**1. Purpose (Why)** — why do this. What breaks if it isn't done.

Write this for yourself a few days from now, and for the next agent that comes in tomorrow. Without a record of why "do this" was decided, there's no place to return to when judgment diverges partway through.

**2. Done when** — what counts as finished.

Write it as checkboxes, in a form **a machine or a real device can judge**. Not "it works properly" but "the test passes," "it renders on the device." This is the only way to make "it's done" verifiable. Because this item exists, PASS / FAIL can be checked off item by item at merge time ([`L1-7`](02-issue-loop.md)).

**3. Predicted files / modules to touch** — which files you intend to touch.

This item isn't for yourself — it's **for other work**. If you know before starting that two pieces of work don't touch overlapping sets of files, they can proceed in parallel. If you don't know, they don't run in parallel ([`L2-3`](01-milestone-loop.md) / [`L2-4`](01-milestone-loop.md)). It's a prediction, so it's fine if it's off — you re-declare the confirmed version when you actually start.

## When an Issue isn't needed

Not everything needs an Issue. The following are exempt ([`L1-1`](02-issue-loop.md)):

- A one-line typo fix
- Non-code files (md / json / yaml, etc.)
- Scratch work outside git's reach
- Exploration, reading, conversation (work that changes nothing)

When in doubt, think of it this way: **if it's likely to span several sessions, open an Issue.** If it wraps up in one sitting, you don't need one.

## What changes when you pair this with AI

Issue-first wasn't invented for AI. It's a practice software development has used for a long time. But pairing it with AI agents makes its value jump, for three reasons.

- **Memory starts at zero** — a human has "oh right, last week..." An agent doesn't. The Issue becomes the only memory
- **Multiple agents run at once** — without declaring who's touching what, collisions are left to chance
- **"It's done" is self-reported** — the only way to prevent unverified completion reports is to write down the completion criteria before starting

## Common questions

**Do I really need an Issue for every small fix?**

No. See "When an Issue isn't needed" above. The rule of thumb is whether it's likely to span several sessions.

**Won't this mean too many Issues?**

Yes, it will. But what causes trouble is "Issues left open," not closed ones — a closed Issue is useful as a record. Representing lane state with just five words (WIP / HOLD / MERGED / SUPERSEDED / ABANDONED) exists precisely so open and finished work can be told apart at a glance ([`L1-4`](02-issue-loop.md)).

**Does this matter if I'm developing alone?**

If you're using an agent, yes. Even working solo, handoff happens the moment you cross a session boundary. Conversely, if all your work finishes within a single session, Issue-first buys you almost nothing.

**Isn't writing the Issue a waste of time?**

You're writing three items. Skip them, and later you'll spend time reconstructing "what did I actually verify" and "how far did I get." Which is the better deal depends on how long the work is — the shorter the work, the less you need an Issue. That's why "when it isn't needed" is decided up front.

## Where the rules live

| What you want to know | Rule |
|---|---|
| The Issue-first principle itself, and the scope of exceptions | [`L1-1`](02-issue-loop.md) |
| The three required items in an Issue body | [`L1-2`](02-issue-loop.md) |
| How the predicted files to touch get used (whether parallel work is possible) | [`L2-3`](01-milestone-loop.md) / [`L2-4`](01-milestone-loop.md) |
| The five words that represent lane state | [`L1-4`](02-issue-loop.md) |
| How completion criteria get checked off at merge | [`L1-7`](02-issue-loop.md) |
| The template for Issue comments (WIP / HOLD / completion record, etc.) | [templates/issue-template.md](../templates/issue-template.md) |

Two more premises: [Why cut modules small](why-small-modules.md) / [Why build simple](why-simple-systems.md)

Back to the front door: [README](../../../README.md)
