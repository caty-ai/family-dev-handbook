> **Machine translation.** The Japanese original ([publication-checklist.md](../../../templates/publication-checklist.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# Repository Publication Checklist

## Purpose

This checklist is the canonical source for recording that a repository publication lane has passed [PB-1](../docs/11-publication.md#pb-1)'s gate with an item-by-item verdict and evidence artifact.

⟨RS-n⟩ = a provenance note tracing back to each household's local pre-publication gate. Each item is self-contained even without a reference target.

An item ID is not a rule ID, but is treated the same way as a stable ID — additions go at the end of each section, and a deletion leaves the number retired.

## Version Rules

Following [PB-2](../docs/11-publication.md#pb-2), in principle record the referenced handbook release tag; only when run in a state not yet included in a tag, record the commit SHA, and once a tag including that state is cut, append it to the completion record.

```text
checklist version: <handbook release tag>
# タグ未包含時だけ
checklist commit: <full commit SHA>
checklist release tag (追記): <その状態を含む handbook release tag>
```

## Consumer Procedure

1. For all 28 items A1–E4, collect the evidence artifact each item specifies.
2. Place the following table **exactly once** in the lane Issue's completion record. The verdict is one of `PASS` / `FAIL` / a reasoned `N/A`, and the evidence column carries either the artifact itself or a resolvable pointer, whichever the item specifies.

   ```markdown
   | ID | 判定 | 証拠 artifact | 注記 |
   |---|---|---|---|
   | A1 | PASS / FAIL / N/A（理由） | <項目指定の証拠> | <必要な補足> |
   ```

3. On a public→private→public republication, cite the most recent completion record, and re-run the items that changed since last time plus the items whose result the republication could change. The new table carries all 28 items — for reused evidence, cite the source; for re-run evidence, record this run's artifact.
4. If you find something ambiguous, missing, or misclassified, report it as a gap to [Issue #100](https://github.com/caty-ai/family-dev-handbook/issues/100).

Only the consumer lanes [PB-5](../docs/11-publication.md#pb-5) designates measure how long the (c) items take.

Once mechanization is implemented for a (b) item, that row's manual procedure is replaced with a run URL.

The class cells preserve the original text from [the finalized Phase 2](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5355210694): **(a)** = mechanical inspection via an existing handbook reusable, today / **(b)** = mechanizable but not yet implemented / **(c)** = a human judgment call that passes only on the owner's label or a ruling record.

## A — Initial Repository Setup (structure and entry points)

| ID | Item | Class | How to pass it today | Evidence artifact |
|---|---|---|---|---|
| A1 | Set up CI with `test` as the gate from the moment the repository is created (T-1). If CI doesn't exist yet, don't fake green — write `CI: not yet` in the README | (b) — no bootstrap conformance check exists; T-1 is prose | Visually confirm the test-lint caller's presence, and run it. If not yet set up, confirm the README's `CI: not yet` | The test-lint caller's first run URL, or the README's explicit `CI: not yet` |
| A2 | An entry point for `make test` / `make lint` exists and propagates the exit code (campaign rule 4 — confirm all the way through that make goes to Error on a forced failure) | (b) — checkable by a bootstrap script; today proven only by seat sandbox runs | Run `make test` and `make lint`, and in an isolated working state, inject an intentional failure and confirm a non-zero exit | A local-run transcript + proof of the forced failure |
| A3 | Don't make the lint target a no-op. Don't place a lint that can never fail behind a green badge | (b) — mechanizable as "lint job must have ≥1 failable step / placeholder-echo detector" | Temporarily introduce a lint violation and, in an isolated working state, confirm lint goes red | Proof that a mutation introducing a lint violation goes red |
| A4 | The 5 gate callers (test-lint / pr-size / review-labels / gitleaks / history-check) exist, are pinned to `@ci-v1`, are byte-identical to the canonical source at `templates/ci`, and haven't duplicated the scanning logic inside the repository | (a) today the *identity* is seat-verified by hand; caller presence is machine-fact | Record the first run URL for each of the 5 callers, and check each file's SHA256 against the canonical source | SHA256 cross-check against the canonical source + first run URL |
| A5 | Wire up T-6's reconciliation and enable it with `require_suite_reconciliation: true`. Leaving the default `false` is an inert gate | (b) — flag presence is greppable; today unchecked | Confirm the caller's input value, run test-lint, and confirm the summary's 3 values reconcile | A green run showing `declared=N executed=N skipped=K` |
| A6 | Register branch protection / required checks, making the gate blocking rather than advisory (confirm `branches/main/protection`'s state) | (c) today (owner-only settings) / (b) verifiable half: a read-only API probe can red-flag absence | An owner label / a ruling record meeting PB-3's issuance requirement | API probe output + a record of the owner's action. A 404 on `branches/main/protection` doesn't distinguish "no protection" from "insufficient permission," so don't pass on an ambiguous probe result. Also measure `rulesets` (the track record from Phase 1 §3.5) |

## B — Display Honesty (README, badges, numbers)

| ID | Item | Class | How to pass it today | Evidence artifact |
|---|---|---|---|---|
| B1 | Only a machine paints green. Static badges follow T-7's closed color allowlist, and every badge URL resolves | (b) — badge-lint (slug points at this repo, endpoint 200, color allowlist) is a concrete gap | Fetch the URL for each badge, and cross-check the target repository, HTTP response, and static color against T-7 | A curl transcript for each badge |
| B2 | A handwritten measured number carries a date and a resolvable source. Treat "a count with no date" as zero | (c) with a (b) assist: a date-adjacency lint can flag bare numbers; truth needs a human | An owner label / a ruling record meeting PB-3's issuance requirement | A grep sweep + a record |
| B3 | Has a supported-environment table ⟨RS-1⟩, a hero image ⟨RS-2⟩, 4-language READMEs with cross-navigation ⟨RS-4⟩, and docs' 3-layer structure | (b) — presence/cross-link lint is trivial; content quality stays (c) | Verify presence and cross-links by running publication-gate and recording the target-file listing. Content quality passes only by an owner label / a ruling record meeting PB-3's issuance requirement | A publication-gate run (today's partial coverage) + a file listing |
| B4 | Set the social preview to 1280×640 ⟨RS-3⟩, and set the Settings description in English ⟨RS-10⟩ | (c) — API-readable but set by owner; (b) probe possible | An owner label / a ruling record meeting PB-3's issuance requirement | An API probe (e.g. `gh api repos/OWNER/REPO --jq .description`) |
| B5 | Make OS-related claims accurate and make skips visible. Use `run_macos` / `macos_skip_reason`, and a skip with no reason goes red | (a) — reusable enforces once caller adopts matrix inputs | Record the test-lint reusable's first matrix run URL | The first matrix run URL that includes a skip lane |
| B6 | Don't leave Issue labels at the default 9 — design them ⟨RS-11⟩. Carry component: / platform: / severity: axes, and don't let priority and severity coexist | (b) — label-census script exists in spirit (.github#19: 11/11→14/14 measured by seats); no reusable | Fetch `gh api repos/OWNER/REPO/labels`'s output, and confirm the axes and the coexistence ban | The census output from `gh api .../labels` |

## C — Secrets and History

| ID | Item | Class | How to pass it today | Evidence artifact |
|---|---|---|---|---|
| C1 | Carry the gitleaks caller through to an actual first run. State explicitly that what the reusable scans is the PR range merge-base..HEAD, not the full history, and separately from that, make a full-history scan before publication ⟨RS-6⟩ **must-pass** | (a) for PR-range; **(b) gap: one-shot full-history scan as a publication-time job** | Record the PR-range reusable's run URL. Until the full-history job is implemented, run `gitleaks git --no-banner --redact --log-opts="--all" .` at the repository root, and record the command, the gitleaks version, the exit code, and the full output in a transcript | The PR-range caller's run URL + a manual full-history-scan transcript |
| C2 | Carry the history-check caller through to an actual first run (the merge-base / unrelated-histories gate; an empty range is fail-closed) | (a) | Record the history-check reusable's first run URL | The first run URL |
| C3 | Place a `.publication-denylist` and make it conform to D8. A committed denylist must not expose the literal of what it protects — choose from 3 forms: a publication-safe notation / gitignore + injecting the secret into CI / a recorded explicit acceptance | (a) for gate execution; **(c) for D8 choice** (which of the 3 options, recorded per repo); (b) gap: a literal-exposure self-scan on the denylist file itself | An owner label / a ruling record meeting PB-3's issuance requirement | A publication-gate run + the recorded D8 choice |
| C4 | Sweep internal information ⟨RS-5⟩. Include family names, personal paths, `_handoffs/`, screenshots, and test logs inside Issues / PRs in scope | (c) — judgment; publication-gate covers denylist-declared patterns only | An owner label / a ruling record meeting PB-3's issuance requirement | A sweep record enumerating the scope covered |
| C5 | Vendor the publication-gate script byte-identical to the canonical source, and make its embedded selftest green as a T-6 counted suite | (a) | Record the publication-gate selftest's run URL, and cross-check blob identity against the canonical source | A blob-identity note + the selftest run URL |

The reason for making C1's full-history scan must-pass, and the grounds for satisfying it with a manual transcript until the job is implemented, live at [#100's owner ruling 2](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5359570954).

## D — Review and Merge Discipline

The Phase 2 original ordered these D1, D2, D3, D7, D4, D5, D6; here they're resorted into ascending order without changing the IDs.

| ID | Item | Class | How to pass it today | Evidence artifact |
|---|---|---|---|---|
| D1 | Secure review seats sized to the change (L1-9 / L1-10), and record requested / actual. Record fallbacks and invalid votes verbatim, and don't count a rejection with no verdict as a vote | (c) — quorum is human process; (a) assist: review-labels reusable enforces label presence | An owner label / a ruling record meeting PB-3's issuance requirement | The seat table inside the completion record |
| D2 | Bind the human-approval gate to the head SHA / event. Don't treat an approval from before a close→reopen as still valid; verify that binding once per repository | (a) — the gate behaves this way today; checklist item is "verify the binding once per repo" | Record the review-labels reusable's run URL, and confirm the correspondence between the head SHA and the label event | A timeline excerpt |
| D3 | Merge with a local `--no-ff` using a noreply identity, and record the diff cross-check against the PR manifest. The precedent for the noreply email and the precedent for adopting local merge from the API-merge identity incident are separate ones | (c) process + (b) gap: a post-merge probe could verify merge-commit authorship/email pattern | An owner label / a ruling record meeting PB-3's issuance requirement | The merge SHA + an identity note inside the completion record |
| D4 | Build a completion record carrying the L1-7 fields and the **T-5 release / previous-release chain**. Record that `deferred` references an Issue, that `N/A` is one of the closed types, and that the tag is annotated | (c) today; **(b) gap: T-5 record-linter** (parse completion comments; verify tag exists+annotated+dereferences to merge SHA; walk 1-hop chain) — the fos#64 L1-8 record fixed exactly what this linter would catch (skipped v0.2.1 hop, non-resolving run IDs) | An owner label / a ruling record meeting PB-3's issuance requirement | The completion-record URL + tag verification |
| D5 | Confirm that every run URL in the record resolves to a run that actually exists, and that the head SHA matches the candidate SHA | (b) — resolvable-evidence linter is a concrete, high-value gap | Re-fetch each run URL and record its existence and the head-SHA match | A note from the manual re-fetch |
| D6 | Place the completion record on the lane Issue, and keep it to exactly one record per lane | (b) partial: "exactly one completion record per closed lane Issue" is machine-checkable | Confirm the lane Issue's comments, and record that there's exactly one completion record | The completion-record URL |
| D7 | A vendored canonical file exceeding pr-size uses only **an owner-granted `size-exempt` label + blob-identity grounds against the canonical source** as its declaration form. Past acceptance of an advisory-red or of no label is grandfathered history — don't treat it as precedent | (c) choice of form is owner rule-making; (a) assist: pr-size gate + blob check | An owner label / a ruling record meeting PB-3's issuance requirement | A `size-exempt` label event from the owner's account + a blob-SHA identity note against the canonical source |

D7's sole declaration form is a deliberate departure reflecting [#100's owner ruling 1](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5359570954).

## E — Organization and Registry Integration

| ID | Item | Class | How to pass it today | Evidence artifact |
|---|---|---|---|---|
| E1 | Place a registry entry in family-os's `modules.json` carrying published state and #62 contract's pin fields, and make the orphan check green on the next weekly run | (a) — family-os machine checks + weekly lane | Record family-os's registry-check run URL | A registry diff + the check-run URL |
| E2 | Render the family footer deterministically, and confirm re-running it produces a zero diff | (a) — renderer + idempotence pattern (fma#24) | Run the renderer and record that re-running it with the same input produces a zero diff | A re-run diff transcript |
| E3 | Either inherit the org-default template or deliberately override it, and confirm the result via GraphQL's `repository.issueTemplates` | (b) — probe script exists as recorded practice, not a reusable | Run the GraphQL query and record the returned template list | The GraphQL output |
| E4 | Has community health files ⟨RS-9⟩ and LICENSE=MIT/Caty ⟨RS-8⟩, and the quickstart runs by copy-and-paste ⟨RS-7⟩ | LICENSE presence (b)-trivial; quickstart (c) — human execution | Verify and record the presence of LICENSE and community health files via the API / the community-standards screen. The quickstart execution verdict passes only by an owner label / a ruling record meeting PB-3's issuance requirement | A screenshot / API dump of community standards + an execution transcript |
