> **Machine translation.** The Japanese original ([epic-template.md](../../../templates/epic-template.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# EPIC Issue / Epic Lane Templates

The canonical field schema for the Epic lane ([docs/06](../docs/06-epic-lane.md), E-1 through E-10). Comment formats for single-shot Issues, WIP/HOLD, etc. remain as in [issue-template.md](issue-template.md) (child Issues within an Epic also use that file).

## EPIC Issue body (E-1 / E-2 / E-3 / E-10)

```markdown
## Purpose (Why) — feature axis

<!-- Write the value in human terms. Not module names — what becomes possible -->

## Done when — Epic level

- [ ] <!-- State it so it can be judged from the integrated state (not a simple sum of the children's Done when) -->
- [ ] Integration review (E-6③ full L1-7) passes, epic→main merge

## Child Issue list — module axis

<!-- 1 child = 1 module or 1 repo. Express dependencies via Blocked-by.
     Contract freeze item #0 is required only for Epics that touch module-boundary interfaces (E-2) — for Epics that don't touch them,
     omit row 0, and judge contract-level status via the Done when / external IF description in E-3 -->

| # | Issue | Module / repo | Blocked-by |
|---|---|---|---|
| 0 | #<n> Contract freeze (boundary interface finalized) | <target> | — |
| 1 | #<n> | <target> | #0 |

## Effective declaration set (E-10 — union of children's declaration sets ∪ the EPIC Issue's WIP declaration set)

<!-- Input for parallel-GO judgment (per L2-4) between Epics and against lanes outside the Epic. Update as children are added/removed and as the epic worktree's integration work targets (the E-4 WIP) change -->

- path/to/module-a/
- path/to/module-b/

## Human checkpoint table (E-3 — required section)

<!-- Required triggers (all high-risk-area items + contract-level deviations) must always get their own row, whether or not they apply (write "not applicable" if they don't).
     Agents may add rows unilaterally (though narrowing an existing row counts as relaxation). Deleting or relaxing rows keeps the old table in effect until the owner re-approves (FP-8 / L1-8).
     Passage approval requires an explicit owner comment only — rewriting the status column by itself does not constitute approval (E-3 / FP-8) -->

| # | Where it stops | What to show | Why it needs human judgment | Status |
|---|---|---|---|---|
| 1 | <e.g., after child #3 completes, immediately before external release> | <e.g., staging URL + diff summary> | External release (high-risk area) | Not reached / Approved YYYY-MM-DD + approval comment URL |

## Kickoff approval (E-1 — evidence that the Epic is established)

<!-- Link to the owner's approval comment. Before approval, the Epic is not established (no E-4/E-5 privileges — FP-9).
     The design-review deadline is the same clock as L1-9/E-6① (no later than before the first child Issue's implementation starts) — do not create a separate deadline.
     If not yet done as of kickoff, write "not done" and do not start implementation on any child until it's done and recorded (L1-9 fail-closed) -->

- Design review record (E-6①/L1-9 — seats, requested/actual, verdict): <URL or "not done (required before the first child's implementation starts)">
- Approval comment: <URL> (YYYY-MM-DD)
```

## Epic log comment (E-7 — posted to the EPIC Issue whenever a child Issue terminates)

```markdown
📦 Epic log (<agent name>, YYYY-MM-DD): child #<n> terminated

- What became possible: <1-3 lines>
- Evidence: <link to the child→epic PR + key points (e.g. final test-run values)>
- Unmet Done when / compromises: <list them. If none, state "none" explicitly — cannot be omitted>
- Next: <the child Issue that moves next / what it's waiting on>
```

## Child→epic light-gate record (E-6② — in the body of the child→epic PR)

```markdown
## Light-gate record (E-6②)

candidate SHA: <commit SHA>   <!-- must match the PR head at merge time. If it changes after review, re-review (E-6②, per L1-8) -->
implementer: <agent/model>
reviewers: <seat 1: agent/model (requested/actual)> <seat 2: …>   <!-- number of seats is looked up from the L1-11 table by the child's weight. A child touching a high-risk area gets 5 seats -->
identity check: <different model | different agent>   <!-- L1-3. Blank is blocking -->

Test results (inline final values): <e.g., 24 passed / exit 0 / YYYY-MM-DD>
Key points: <address the Done when in prose. Table format is optional. Link-only evidence does not qualify (keeps the L1-7 principle that "the record alone shows the final result")>

Declared vs. actual diff (L0-6 — required for child→epic too):
git diff --stat <epic>...<candidate SHA>: <output or summary>
Diff from the declared file set: none | <diff and explanation>   <!-- files in the diff but not in the declaration are blocking -->
```

## Epic termination comment (E-9 — posted to the EPIC Issue. Applies the L1-4 five-vocabulary set)

```markdown
🏁 <MERGED|SUPERSEDED|ABANDONED> (<agent name>, YYYY-MM-DD): <1 line>

- Disposition of the epic branch: discarded (deleted) | rescue PR <URL> (E-6③ gate applies)
- Convergence of child Issue states: <each child's terminal state or the destination Issue it was split out to>
- worktree cleanup: done (YYYY-MM-DD)
- evidence / successor: <integration review record, successor Issue, etc.>
```
