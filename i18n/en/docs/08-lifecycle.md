> **Machine translation.** The Japanese original ([08-lifecycle.md](../../../docs/08-lifecycle.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# LC Workspace Lifecycle — the layer that turns departure of stored things into a contract

While the L layer (L2 / L1 / L0) is a contract for **how work proceeds**, the LC layer defines the contract for **when and how something that was placed in a persistently accumulating location (shared store, working directory, handoff spot) leaves it**. Each rule carries a stable rule ID (`LC-1` through `LC-5`), and the scope each clause applies to is stated in 〔 〕. The summary side ([docs/04](04-adoption.md)) references these IDs. Stance under unverifiable conditions is covered in [docs/05](05-fail-posture.md).

Background: defining only write-side discipline (Issue-first, where to write things) is not enough — **anything without a departure trigger will inevitably pile up**. The LC layer defines a single "how it leaves" contract to pair with the "how it's placed" rules. Stage names use the role term as canonical, with the English label as a parenthetical aid.

## LC-1 Deadline Trigger Principle 〔all adopting projects〕

**When placing something, always decide its departure trigger (a deadline or a completion condition) at the same time.**

Operate on the premise that "anything without a trigger becomes permanently retained." A trigger can take the form of a deadline (a date or a number of days) or a completion condition (once merged, once triaged, once aggregated). When the placement convention (naming, deadline metadata) can't express it, leave one line in the Issue or declaration made at the time of placement.

## LC-2 One-Way Lifecycle 〔houses with persistent storage areas〕

**git branch / worktree are out of scope for this chapter — the canonical source for cleanup is [L0-4 / L0-8](03-git-protocol.md) (delete after merge).**

Things placed in a persistent storage area flow one-way through **intake → active → complete → archive**. Never flow backward.

- Archive is **immutable** — once something enters, it is not rewritten or deleted
- When restoration is needed, don't remove it from the archive — bring it back to the active side **as a new copy**
- Attach a record (manifest) to the archive destination noting what was moved, when, why, and how to restore it

## LC-3 Explicit Departure Conditions 〔houses with a persistent workspace / shared store〕

For the following **three categories**, **write numeric departure conditions into local configuration**:

1. **Heavy binaries** — non-text items placed that exceed a given size (e.g., anything over 1MB goes to archive)
2. **Explicit old versions** — items placed under a name or location identifiable as an old version (e.g., `旧〜/` or `.bak` goes to archive as soon as detected)
3. **Aggregation of periodic items** — the source items behind a periodic item, once aggregated (e.g., after a monthly digest is generated, the raw files go to archive)

**The canonical numbers live on the local configuration side — every number that appears in this chapter's body text (day counts, sizes, etc.) is an "example" and does not count as part of the contract** (MUST). The contract of this chapter is the frame (that departure conditions exist for the three categories); the actual numbers belong to the local side — the same approach as putting the qualified model roster in local configuration under [L1-10](02-issue-loop.md).

## LC-4 Three-Piece Departure Set for Append-Only Stores 〔MUST, limited to stores declared append-only〕

**Append-only store** = a storage location that has declared an operating policy of never rewriting or deleting existing content. **This clause applies as a MUST only to houses that have declared a store append-only. Houses without such a store are N/A** — this premise is not imposed on all adopting projects.

Departure from an append-only store (a move to archive) is the sole explicit exception to the append-only principle, and it must always be done as the following **three-piece set**:

1. **Backup** — take a snapshot of the store before the move
2. **Move** — move it to the archive destination (a move, not a copy that leaves the original behind)
3. **Leave a pointer** — leave a pointer at the original location indicating where it moved to, when, and why

**The actual work of departure is always a manual operation by a human / agent.** Do not place automated moves or deletions in this path (→ LC-5).

## LC-5 Inspection Is Warning-Only 〔all adopting projects〕

**Inspection / lint does not move files.** What it may do is: detect → periodic report → a human (or owner) decides. No automated departure.

The information plumbing for lint is fail-open ([FP-4](05-fail-posture.md)) — "an inspection failure does not halt work" (FP-4) and "inspection does not move files" (this clause) are a pair, and inspection always defaults to read-only.
