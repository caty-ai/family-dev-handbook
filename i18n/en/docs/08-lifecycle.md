> **Machine translation.** The Japanese original ([08-lifecycle.md](../../../docs/08-lifecycle.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# LC Workspace Lifecycle — Making the Exit of Placed Items a Contract

While the L layers (L2 / L1 / L0) are contracts for **how work proceeds**, the LC layer defines the contract for **when and how a placed item leaves a place where things accumulate persistently (a shared store, a working directory, a handoff location)**. Each rule is given a stable rule ID (`LC-1` through `LC-5`), and the scope of application for each clause is noted in 〔 〕. The summary side ([docs/04](04-adoption.md)) references these IDs. For the stance to take when verification isn't possible, see [docs/05](05-fail-posture.md).

Background: defining only write-side discipline (Issue-first, where to write) is not enough — **anything without an exit trigger will inevitably accumulate**. The LC layer defines a single "how it leaves" counterpart to the rules for "how it's placed." Role terms are canonical for stage names; English labels are a supplementary notation in parentheses.

## LC-1 Expiry Trigger Principle 〔all adopters〕

**When you place an item, always decide its exit trigger (an expiry or a completion condition) at the same time.**

Operate on the premise that "anything without a trigger becomes permanently retained." The trigger can take the form of an expiry (a date or a day count) or a completion condition (once merged, once triaged, once aggregated). When the placement convention (naming, expiry metadata) can't express it, leave one line in the Issue or declaration at the time of placement.

## LC-2 One-Way Lifecycle 〔homes with persistent areas〕

**git branch / worktree are out of scope for this chapter — the canonical source for cleanup is [L0-4 / L0-8](03-git-protocol.md).**

Items placed in a persistent area flow one-way through **intake → active → complete → archive**. Do not reverse the flow.

- Archive is **immutable** — once something enters, it is not rewritten or deleted
- When restoration is needed, do not delete from the archive — bring it back to the active side **as a new copy**
- Attach a record (manifest) to the archive destination noting what was moved, when, why, and how to restore it

## LC-3 Explicit Exit Conditions 〔homes with persistent workspaces / shared stores〕

For the following **three categories**, **document numeric exit conditions in local configuration**:

1. **Heavy binaries** — non-text items placed that exceed a certain size (e.g., anything over 1MB goes to archive)
2. **Explicit old versions** — items placed with a name or location marking them as an old version (e.g., `old~/` or `.bak` go to archive as soon as detected)
3. **Aggregation of periodic items** — raw source files after periodic-item aggregation (e.g., after monthly digest generation, the raw files go to archive)

**The canonical source for the numbers lives in local configuration, and any numbers appearing in this chapter's body (day counts, sizes, etc.) are all "examples" and do not count as part of the contract** (MUST). The frame (having exit conditions for the three categories) is this chapter's contract; the actual values belong to the local side — the same approach as putting the qualified-model roster in local configuration under [L1-10](02-issue-loop.md).

## LC-4 Three-Part Exit Set for Append-Only Stores 〔MUST only for stores declared append-only〕

**Append-only store** = a storage location that has declared an operating policy of not rewriting or deleting existing content. **This clause applies as a MUST only to homes that have declared a store append-only. Homes with no such store are N/A** — this premise is not imposed on all adopters.

Exiting an append-only store (moving to archive) is the sole explicit exception to the append-only principle, and it must always be done as the following **three-part set**:

1. **Backup** — take a snapshot of the store before the move
2. **Move** — move it to the archive destination (a move, not a copy that leaves the original)
3. **Leave a pointer** — leave a pointer at the original location indicating where, when, and why it was moved

**The actual exit work is always a manual operation by a person / agent.** Do not place automated move or delete operations in this path (→ LC-5).

## LC-5 Inspection Is Warning-Only 〔all adopters〕

**Inspection and linting do not move files.** What's allowed is: detect → periodic report → a person (or the owner) decides. No automatic exit.

The information plumbing for lint is fail-open ([FP-4](05-fail-posture.md)) — "an inspection failure doesn't stop work" (FP-4) and "inspection doesn't move files" (this clause) are a pair; inspection always defaults to read-only.
