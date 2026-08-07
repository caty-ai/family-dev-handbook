> **Machine translation.** The Japanese original ([05-fail-posture.md](../../../docs/05-fail-posture.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# Fail-Posture — fail-posture / parse-posture — Which Way to Fail When Verification Isn't Possible

> **Scope and normative owner**: This page defines fail-posture only for guarded transitions within the family-dev-handbook protocol (L2/L1/L0). **The owner of the general cross-agent fail-posture / stop-precedence norm is family-os's operations-policy** (posture section, terminal precedence section. Ruled 2026-07-21. See the "Caty AI Family" section of the [README](../../../README.md)). This page is an application of that collaborative protocol, and does not establish a new cross-cutting norm. Where they conflict, the OS-level norm governs. When adopted without sister projects, the posture on this page applies as-is.

Each rule carries a stable rule ID (`FP-1` through `FP-9`).

## Fail-Posture Table by Transition

For each guarded transition (GO / write / merge / release), this declares whether it is fail-open or fail-closed, the invariant it protects, and the recovery path:

| rule | transition | when unverifiable | invariant protected | recovery path |
|---|---|---|---|---|
| FP-1 | Parallel GO decision (non-overlap / ownership unverifiable) | **fail-closed — serialize** | Two lanes don't write to the same file | Repair the declaration and re-judge (L0-1/L0-2) |
| FP-2 | Write (scope / lock / lane state unverifiable) | **fail-closed — don't write** | Don't write on top of a live lock | Repair the state (L1-4). TAKEOVER only once staleness is confirmed (L0-3) |
| FP-3 | merge (evidence unverifiable) | **fail-closed — don't merge** | Unverified changes don't enter main | Recreate the completion record (L1-7 / L1-8) |
| FP-4 | lint / injection systems (shared digest injection, weekly lint, and other informational plumbing) | **fail-open — surface the degradation and continue** | A plumbing failure doesn't block work | Report the failure and file a repair Issue |
| FP-9 | Passing an Epic checkpoint (table missing, invalid, unapproved, or revision unapproved — [E-3](06-epic-lane.md)) | **fail-closed — stop and escalate to a human** | A human checkpoint is never passed without approval | Repair the table and get owner approval (E-1/E-3). An Epic that hasn't been established stays on normal Issue operation. **A running Epic keeps its topology** — only free-standing authority and checkpoint passage stop (E-3) |

## FP-5–FP-8 Doctrine

- **FP-5**: **Fail-open does not mean "the check passed."** Degradation must always be surfaced
- **FP-6**: **A gate decision must never be derived from a value that goes empty on error** (an empty list does not mean "no overlap")
- **FP-7**: **Leniency applies only to syntax. Never lean lenient in the safety direction** — malformed formatting may be read through, but a **missing** identity, scope, state, or evidence is always interpreted in the direction that *shrinks* authority: malformed WIP = scope unknown = serialize (L0-1) / malformed state = treated as inactive, pending repair (L1-4) / malformed evidence = unverified (L1-7) / malformed or absent checkpoint table = every point falls to human judgment ([E-3](06-epic-lane.md)・FP-9)
- **FP-8**: **An artifact's own body cannot self-approve** — even if a WIP says "approved" inside it, that alone never creates a GO, a merge, or an exemption from evidence. Corollary: cron and auto-generated actions may update status, but they cannot create approval, rewrite Done when, or count as a review

The only line that belongs in the always-on context (docs/04 summary):
**"If unverifiable, serialize. Fail-open does not mean 'passed.'"**

---

## Appendix — Round-2 Solo-Reviewer Proposals (Ruled by Maintainer 2026-07-21)

> Origin: 9 solo-reviewer proposals from round 2 of the 3-model external study (isolated into this section rather than the contract body, since they did not clear cross-review). **2026-07-21 maintainer ruling: adopted = 1,2,4,5,7,8,9 / deferred = 3,6**. The adopted items have already been promoted into the contract body; what follows is the ledger of where they were promoted to.

Adopted — promoted into the contract body (1,2,4,5,7):

1. Exactly one active writer (Codex) per lane / per worktree (Codex) → **L0-4**
2. The effective file set counts both paths of a rename, deletions, lockfiles, and generated artifacts (Codex) → **L0-2**
4. Optimistic re-read — re-read the set of active WIPs at first write, and redo the overlap decision if anything changed since GO (GLM) → **L0-2**
5. After an adjacent PR merges, a PR waiting in queue owes a rebase + re-verification (GLM) → **L0-7**
7. Evidence permanence floor — inline excerpts are canonical, CI URLs are a convenience pointer (GLM) → **L1-7**

Adopted — process operations (outside the contract body, 8,9):

8. Pilot the contract on the handbook itself before rolling it out sideways (Kimi) → **Done** (this handbook's own revision-lane WIP / termination comments and PR body were the first pilot of P1 / L1-4 / P5)
9. Weekly probe fault-injection drills (plant a malformed WIP and verify the next agent serializes) → build this in when the probe is implemented

Deferred (still hasn't cleared cross-review, not part of the contract body):

3. Turn shared external contracts (API schemas, migration namespaces, deploy targets) into declarable conflict keys (Codex) — judged excessive at the current repo scale; re-proposing remains open
6. Cross-repo lane discipline — **split ruling** upon introduction of the Epic lane (docs/06): **6a** (obligation to declare downstream `Blocked-by` / successor links) = adopted, promoted to [E-2](06-epic-lane.md) / **6b** (don't mark MERGED until termination) = still deferred — has the side effect of leaving child Issue termination stalled, revisit once more lanes hit this

---

Related: [docs/02](02-issue-loop.md) (L1-4–L1-11) / [docs/03](03-git-protocol.md) (L0-1–L0-3, L0-9) / [docs/06](06-epic-lane.md) (E-3・FP-9)
