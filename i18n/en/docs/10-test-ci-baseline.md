> **Machine translation.** The Japanese original ([10-test-ci-baseline.md](../../../docs/10-test-ci-baseline.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# T Test & CI Baseline — the Layer that Mechanically Accumulates Proof of Correctness

Where the L layers (L2 / L1 / L0) are the contract for **how work proceeds**, and the R layer is the contract for **what gets accepted**, the T layer defines the contract for **the minimum a repository must do to keep proving its own correctness through tests and CI — initial setup, accumulating regression tests, baking it into the delegation format, never merging while red, closing out shipping with a tag, a test-output contract, and honest badges and numbers**. Each rule carries a stable rule ID (`T-1` through `T-7`), and the scope of application for each clause is noted in 〔 〕. The summary side ([docs/04](04-adoption.md)) references these IDs. The general principle of enforcing a gate as a check is [R-6](09-rejection-rubric.md); the stance to take when verification isn't possible is [docs/05](05-fail-posture.md).

Background: a public repository's credibility gets judged from the outside, instantly, by "does it have tests, is CI green." The merge evidence gate ([L1-7](02-issue-loop.md)) and check enforcement ([R-6](09-rejection-rubric.md)) already embody this thinking, but **no layer required the initial setup and accumulation of tests and CI**. Accumulating tests is something only an operating rule can create — it isn't a feature CI provides on its own. Meanwhile, this protocol's implementation always passes through a delegation brief (the [B layer](07-delegation-brief.md)), so baking it into the format is enough to make it stick.

## T-1 Initial Setup — Stake Out the Harness First〔a new repo that contains code = MUST / an existing repo = the next lane that touches its code / a non-code repo = justified N/A〕

**A new repository that contains code sets up a test runner and a CI workflow at creation time. The required gate is `test`; for languages with type checking, include `typecheck` in the same gate. Stake out the harness first, even with zero tests.**

Reason: adding it later turns "a repo with no test culture" into an established fact. Once the harness exists, T-2 / T-3 automatically pile up tests from then on. The default CI type is [templates/ci/](../../../templates/ci/README.md) (a hand-rolled workflow also satisfies the clause). Register the CI you set up as a required status check so it's confirmed mechanically (deployment steps 5-6 of templates/ci. Where branch protection can't be enabled, hold the line operationally).

Retrofitting an existing repository is **opportunistic** — the next lane that touches its code adds one line to that Issue and sets up T-1 at the same time. Don't stand up a lane dedicated to inventory sweeps (don't pre-pay effort on a repo nobody is using — [the simplicity principle](why-simple-systems.md)).

A repo of nothing but docs, assets, or config is a **non-code repo: justified N/A** (the same vocabulary as [L1-7](02-issue-loop.md)) — leave a one-line note of the judgment on the Issue at creation time. Don't fill the harness with a hollow dummy test (don't manufacture your own "zero targets, green" — the pitfall documented at [templates/ci/](../../../templates/ci/README.md)).

## T-2 Regression-Test Default〔bug fixes of size M / L / H. A child Issue inside an Epic is judged by the child's own weight〕

**A bug-fix PR at size M / L / H ([L2-1](01-milestone-loop.md)'s weight judgment; a child Issue inside an Epic is scored by the child's own weight, the same as [E-6](06-epic-lane.md)) comes with a reproduction test for the bug (red before the fix, green after) by default.**

Size S (a typo, roughly a single local file) is exempt. Under-reporting size to dodge the requirement is caught on the sizing side by "round up when in doubt" (L2-1). The test obligation for feature additions is out of scope for this clause — it's carried by [T-3](#t-3) and each Issue's own Done when.

Write the reason for not being able to include one in **two tiers**:

1. **The default 3 types** (a closed enumeration — mechanically judged):
   - **Environment-dependent** — only reproducible on real hardware, a real device, or a specific OS
   - **External-service-dependent** — needs a real response from an external API or external system
   - **Reproduction cost too high** — the cost to build it doesn't match the value of the fix (owner sign-off only)
2. **Anything outside the 3 types is the owner's call alone** — leave one line on the PR recording the fact and reason for the owner's call. A free-form reason is valid only for the owner's-call case

It's a closed enumeration to keep free-form "reasons I couldn't write one" from multiplying endlessly as excuses.

<a id="t-3"></a>

## T-3 Brief Hookup — Baking Accumulation into the Format〔a delegation that includes a code change = whichever of B-1's applicable cases changes the repository's code〕

**A delegation brief that includes a code change must include, in its "Implementation Check (Self-verification)," "tests added or changed, and their results" as a standard item** (the canonical format lives at [templates/brief-template.md](../templates/brief-template.md)).

A delegation that added no test includes "none added + reason" in its delivery report. Write the reason from a **closed enumeration**:

1. **Falls under T-2's exemption** (size S) — a one-line note to that effect is enough
2. **The change has nothing to test** (config or declarations only, etc.)
3. **An existing test already covers the change** — must point to that test
4. **One of T-2's 3 types** (environment-dependent / external-service-dependent / reproduction cost too high = owner sign-off)
5. **Falls under T-2's second-tier owner's call** — must point to that sign-off record

Reason: accumulating tests only becomes automatic once it's baked into the delegation format. The delegate works from fresh context, so any expectation not written in the brief might as well not exist (the same direction as [B-4](07-delegation-brief.md)).

## T-4 Fail-Closed Merge — Never Merge While Red〔every repo = MUST〕

**Merging while CI is red is prohibited.** This clause sets the **sole explicit exception** to [docs/02](02-issue-loop.md)'s Definition of Done item "tests and lint pass," and CI status is recorded in the completion record (L1-7).

There is exactly one exception: **a red that is known and unrelated to this PR** (e.g., a red caused by a pre-existing bug on main). The conditions for it to hold are **all mandatory**:

1. **Proof of unrelatedness** — attach, inline in the completion record, a record that the same red reproduces on base (the state without this PR's changes) (evidence, not a claim — L1-7②)
2. **Binding the red's identity** — write the failing check name + workflow run identifier + observed date, tied to the candidate SHA
3. **A reference to the relevant Issue** — if there's no Issue to reference, file one first. The Issue must carry an [LC-1](08-lifecycle.md) exit trigger (an expiry or a completion condition), and this exception lapses once the trigger lapses
4. **Verifiable proof the owner's call is real** — leave it in a form a **third party can confirm is real**, such as a PR comment from the owner's own account. A description in the completion record's body alone does not make the exception hold ([FP-8](05-fail-posture.md) / [R-6](09-rejection-rubric.md))

Making the boundary explicit:

- **An intermittent red (flaky) is not included under "known and unrelated"** — including one requires, on top of the 4 conditions above, the owner making and recording that call each time
- **Don't write "green" for a state where CI doesn't exist** — a lane touching code in a repo where CI isn't set up doesn't merge until that same lane satisfies T-1 (if there's no time, e.g. an emergency fix, the owner can grant a grace period by sign-off, leaving an Issue for T-1 setup carrying an LC-1 exit trigger. This sign-off, too, is recorded in the same externally verifiable form as condition 4)
- **`CI: N/A` is valid only when CI doesn't examine the change in question** (the reason must state the grounds for being out of scope for inspection). A change that CI does run against is never marked N/A, even if it's non-code
- In a repo with required status checks in place, **don't exercise the exception by lifting the requirement** — record it as an explicit action by the owner instead

A red with no reference, or an exception that can't be verified, is not an exception (fail-open never means *passed* — [docs/05](05-fail-posture.md)).

## T-5 Release Default — Close Out Shipping with a Tag〔a merge that includes a ship-equivalent change = MUST / anything else = justified N/A〕

**Every completion record ([L1-7](02-issue-loop.md)) carries a release field.** Its value is one of the following three closed vocabulary items, and a lane that lands a **ship-equivalent change** (a merge that changes behavior users act on, a public API, a distributed artifact, or a norm users must follow) on main cannot choose `N/A`. **A merge you are unsure how to judge is treated as ship-equivalent** (the same direction as [L2-1](01-milestone-loop.md)'s "round up when in doubt" — doubt is never let off the hook into the lighter side, N/A):

1. **`release: vX.Y.Z`** — a declaration to cut a tag at this merge's stable point. The tag must be **annotated + SemVer**, and it is cut on **the commit this merge left on main** (for squash / rebase merges, the new SHA on main). At the time of the record, the tag does not exist yet — the field records a declaration, and **the lane cannot declare MERGED until the tag is cut and its URL appears in the MERGED comment** ([L1-4 termination](../templates/issue-template.md)). This tag-URL obligation is fulfilled only when a Release also **exists on GitHub Releases** (even a bare tag makes `/releases/tag/<name>` return 200 — the URL's existence does not mean a Release exists). In a repo carrying release-sync ([templates/ci/](../../../templates/ci/README.md)), the obligation is normally met by the **green run** after the tag push, but verification remains the lane's duty — **a missing or red run, or no carrier, does not constitute fulfillment**. An unfulfilled lane **stays open as WIP without terminating**, so it rides [L0-3](03-git-protocol.md)'s stale clock, and a forgotten tag stays visible even in a repo where no further lane arrives (a MERGED lacking a tag URL or Release existence is **malformed** and its termination does not hold = [L1-4](02-issue-loop.md)'s inactive treatment). Appending this fulfillment report is fulfilling the declaration, not a correction under [L1-8](02-issue-loop.md). The tag name **should, in principle, match the declared identifier** — only when scope shifted after review and the version itself changed may it be cut under a different name, with the difference and the reason recorded in one line in the MERGED comment (never silently cut a different version). Changing the declaration itself to `deferred` goes through L1-8's superseding record (no silent rewrite). Where a lane has no authority to cut tags itself, a **HOLD** with the owner set as the tag-authority holder (the [5 fields of L1-5](02-issue-loop.md)) is a lawful way out
2. **`release: deferred`** — a declaration not to cut a tag now. It must carry a **reference to an Issue with a reason plus an exit trigger** (an expiry or a completion condition = [LC-1](08-lifecycle.md)) — if there is no Issue to reference, file one first (the same shape as **T-4**③: since a merged PR's body never resurfaces in anyone's view, this belongs on the resurfacing surface — an Issue). A `deferred` lacking an Issue reference or a trigger is invalid (= blocking, the same as a missing field). **A `deferred` whose trigger has lapsed loses its "right not to tag"** — the lane's own MERGED stays valid, but **the next ship-equivalent merge cannot choose `deferred` (`vX.Y.Z` is required)**. Lapsing itself does not block the next completion record (blocking it would leave no way to clear an unfulfilled declaration that has neither a declared identifier nor a target commit — the same reasoning as **T-4**③ limiting itself to lapsing the exception, not the record). Making an overdue deferred visible is the referenced Issue's job. A deferred **resolves once a later ship-equivalent merge fulfills `vX.Y.Z`**, closing the referenced Issue (re-declare with a new trigger if work remains)
3. **`release: N/A`** — only for a merge that is not ship-equivalent. The reason must be written from a **closed enumeration**: ① docs only, carrying no norm users must follow ② internal cleanup that changes neither behavior, a public API, nor a distributed artifact ③ CI or dev-environment wiring only ④ an intermediate merge that never reaches main (an Epic child→epic gate = [E-6](06-epic-lane.md)②). **Anything outside these types is the owner's call alone** — record the fact and reason for that call in one line (the same shape as **T-2**). An N/A with no reason is invalid (= blocking, the same as a missing field). In a repo that distributes norms (this handbook, for instance), a docs change *is* the ship-equivalent case — don't use "docs-only" as an excuse for N/A

**A missing field, an empty value, an unedited placeholder, or a value outside the 3-word vocabulary all count as unfilled and are blocking** (the same strength as **T-4**'s CI field). The shape isn't "try not to forget" — it's "forgetting means the completion record doesn't pass." This applies the T layer's own thinking (baking it into the format makes it stick): CI became layered across T-1–T-4, but release had no layer at all until now, and this closes that gap.

Tag contents and signing:

- The release notes (the tag message or the GitHub Release) must cite **at least one pointer to verifiable evidence** (a CI run, the PR with its completion record, etc.) — consistent with the principle of never placing a number that can't be verified (the [R layer](09-rejection-rubric.md)). This is a separate context from the completion record's own evidence discipline ([L1-7](02-issue-loop.md)②, "link-only evidence doesn't qualify") — the record itself stays inline as the source of truth, and the tag only needs a pointer
- **A repo with a signature-verification mechanism (an updater, etc. — anything that mechanically verifies tag signatures) must use signed tags; keys are per-repo.** In a repo that requires signatures, the MERGED fulfillment report must include one word stating whether it's signed (so a missing signature is visible from the record). Otherwise, annotated is enough, and signing is SHOULD
- How far a version bumps (MAJOR / MINOR / PATCH) follows the general SemVer rule; this clause does not constrain it

Making the boundary explicit:

- **Guarding against `deferred` abuse** — once the same repo has run two `deferred`s in a row on ship-equivalent merges, the third ship-equivalent merge cannot choose `deferred` (a tag must be cut). The streak is counted along **the column of ship-equivalent merges** (an N/A merge is not part of that column), and **fulfilling `vX.Y.Z` resets it**. So the count can be verified after the fact, **every completion record** must state, in one line, the same repo's previous ship-equivalent merge's release value and fulfillment status (the `previous release` field). The count is settled by **following the previous lane's `previous release` back one step** — if the previous one was deferred, and the one before that was also deferred, this time `vX.Y.Z` is required (the same direction of escalation as [R-6](09-rejection-rubric.md)'s "make the count verifiable after the fact")
- **Wiring the fulfillment check** — beyond its own release field, a completion record must confirm that **the same repo's previous ship-equivalent merge's release declaration has been fulfilled** ([L1-7](02-issue-loop.md)⑦). **"Fulfilled" is settled by the following**: `vX.Y.Z` = the tag has been cut, MERGED carries the URL, and the Release exists (**missing any of the tag, URL, or Release existence means unfulfilled = blocking**) / `deferred` = while the trigger is alive it's pending fulfillment and doesn't block; once lapsed it still isn't blocking, and instead narrows the next choice as in item 2 above / `N/A` = out of scope, since it isn't part of the ship-equivalent column. The release field **is not a substitute for actually running the tag** — the field is the record of the decision, and an unfulfilled `vX.Y.Z` declaration is closed off on both fronts: it blocks MERGED (item 1 above) and blocks the next lane
- **Enforcement strength is uniform across every repo** — in a repo with no ship-equivalent changes, every merge naturally lands on N/A, so there is no real burden on a private scratch repo. Whether public and private repos should differ in strength is a separate question for a future review; once that lands, this clause's 〔 〕 will follow
- **The Epic child→epic gate ([E-6](06-epic-lane.md)②) is exempt from the tagging obligation** — the field itself is still required, same as every record, with a value from type ④ above (`N/A (pre-epic-integration)`). Tagging is required at the epic→main integration merge (E-6③, full L1-7)
- Retroactively applying this to past untagged merges is out of scope (this clause governs merges "from now on"; past ones are each repo owner's call)
- The record-vs-reality PR-side check and scheduled drift sweep are tracked in [Issue #106](https://github.com/caty-ai/family-dev-handbook/issues/106) (a follow-up with an LC-1 exit trigger)

## T-6 Test-Output Contract — Put the Fact of Execution in One Machine-Readable Line〔new repository with code = MUST / existing repository = establish it in the same Issue on the next lane that touches code, tests, or a CI test job (the same opportunistic rule as T-1) / non-code repository with no runner = justified N/A〕

**A test runner must satisfy an output contract that lets a machine determine what ran, what did not, and why.** Five conditions must hold:

1. **Summary line (the body of the contract)** — the runner emits the following line in its output. This regular expression itself is the canonical format:

   ```
   suites: declared=([0-9]+) executed=([0-9]+) skipped=([0-9]+)
   ```

   Definitions: `declared` = total number of registered suites / `executed` = number that actually ran through PASS or FAIL / `skipped` = number honestly reported as SKIP. The invariant is **`declared = executed + skipped`**. Breaking it is a silent drop = red. The runner aggregates the numbers dynamically — **embedding fixed values (such as constant output with echo) violates this clause** (because a machine cannot verify their derivation, this is an inspection item in the adoption review). The line appears at least once in the output; if it appears more than once, **the last match is authoritative**. A decision to remove a suite from `declared` (unregister it) is recorded in one line in the Issue for the lane doing so — an unrecorded unregister is treated the same as a silent drop
2. **Result vocabulary** — result displays produced by a **family-written runner or wrapper** use the three words `PASS` / `FAIL` / `SKIP`. Raw framework-native output from pytest / unittest / vitest and similar tools is **outside this vocabulary constraint** (the machine gate reads the summary line and exit code, so framework output may pass through unchanged)
3. **Closed exit-code set** — `0` = no FAIL / `1` = one or more FAIL / `2` = usage or input error / `127` = **missing required dependency** (detect it in preflight, name the cause on stderr as `missing-dep: <name>`, and then exit — never misreport a missing dependency as a test failure or input error). A missing optional environment (no physical device, etc.) is not 127; it is **SKIP** and is counted in the summary's `skipped`
4. **Emit the summary even on abnormal exit** — structure the runner so the summary line is emitted even if it dies partway through (`trap finish EXIT` in bash is a non-normative example; Python atexit, Makefile composition, and equivalent mechanisms are all valid). A missing summary = indeterminate = red ([FP-6](05-fail-posture.md)) — though this red does not actually fire until the wiring in item 5 is in place
5. **CI reconciliation wiring (completion condition for adoption)** — this clause is not "established" until the CI-side reconciliation gate ([templates/ci/](../../../templates/ci/README.md) test-lint; reusable input `require_suite_reconciliation: true`) is **enabled**. Merely emitting the summary line or quoting the clause is not adoption ("just placed" = [FP-5](05-fail-posture.md)). A repository outside scope leaves an explicit N/A to that effect in an Issue — silence is not N/A. Wire the skipped form (the three-value summary) only after the reconciliation gate's skipped support (#80 delta) lands on main; reversing the order makes an honest SKIP red

**SKIP-rate cap** — `skipped × 5 > declared` (= above 20%, with declared > 0) is red. A repository that changes the cap puts **the authoritative value in a CI caller input (the machine-readable location)** and records the reason for the change in one PR line or an Issue carrying an [LC-1](08-lifecycle.md) trigger (the same "numbers live in local configuration and changes are recorded" pattern as [LC-3](08-lifecycle.md)). An unrecorded change is invalid, so the default 20% applies. For a repository with declared ≤ 4, the formula means "SKIP 0 by default" — intentionally so (smaller repositories should be able to run everything; if a permanent SKIP is necessary, declare a different cap). SKIP is an honest report that an environment is absent, not a permanent escape hatch — red above the cap prompts "fix the environment or record the decision to remove the suite from scope"

Reason: "the tests ran" is easy to make a self-report. The three values declared / executed / skipped and their invariant reduce the routes for "pretend it ran" (silent suite loss, mixing SKIP into executed, denominator manipulation by unregistering, or misreporting a missing dependency) to one machine check. Fixing the format as a regular expression lets CI-side reconciliation (the W0-3 reusable test-lint) use one common implementation across every repository.

Making the boundary explicit:

- This clause is an **output contract**; it does not constrain test contents, granularity, or framework choice (see the appendix for recommended runners)
- Suite-level reporting is enough (test-case-level reporting is not required — granularity is the repository's choice. Make a SKIP inside a suite visible by splitting the suite)
- A new repository with zero tests (only the T-1 frame exists) may emit no summary line (there is no wiring yet, so it is not red), or may emit `declared=0 executed=0 skipped=0` (executed=0 is red, choosing the side that does not manufacture "green with zero targets") — either is valid, and the latter is recommended
- This handbook's own runner is the **first subject of this clause** (the lane publishing the clause makes its own `make test` conform before merge — the pilot principle)

## T-7 Honest Badges and Numbers — Green Only When a Machine Painted It〔public repository with a README = MUST / any other repository = the same discipline whenever it displays numbers or badges (a private scratch repository displaying neither is naturally N/A)〕

**Any display in a README or docs that looks "verified" is limited to one connected to a machine inspection result.** Three conditions must hold:

1. **CI state is explicit (do not hide "uninspected" by omitting a badge)** — a public repository with a README always displays CI state in **one of two** ways: ① a live badge for **the workflow that runs T-1's test gate** (a GitHub Actions badge.svg or equivalent live endpoint pointing to that workflow; **a badge for some other workflow that does not run tests does not satisfy this clause even when green**) ② if CI is not set up, a grey static badge reading `CI: not yet`. Omitting the display, or substituting the green of another workflow, both violate the clause
2. **Closed color set** — the only permitted colors for a static badge are **`lightgrey` / `blue` (including factual displays such as language and license)**, a closed enumeration. `green` / `brightgreen` / `success` / `passing` variants and equivalent green hex values cannot be used for static badges (inspect the substance, not the spelling — [R-6](09-rejection-rubric.md)). Only a machine-painted live badge may claim green
3. **Measured numbers and the Project status section** — when a README or docs states a number that reads as measured (test count, coverage, performance), it includes **the URL of that measurement run and the measurement date**. If those cannot be attached, do not state the number (do not place a number that cannot be verified — the [R layer](09-rejection-rubric.md)). A number that **differs from the measured value** in a newer run of that workflow is stale — update or remove it (the mere existence of a newer run does not make it stale when the value has not changed). A design value or target may be written when labeled "target," but it cannot masquerade as a measurement (such as "passed" with no run URL). When a README carries a status section, the standard form is below (**this form is canonical** — no external repository is the reference model):

   ```markdown
   ## Project status

   [live badge (badge.svg for the T-1 test workflow) or CI: not yet (grey)]

   - CI: <whether the test-lint gate exists and the connected workflow name>
   - Verified environment: <measured OS / runtime>
   - maturity: <stable / beta / reference, etc.>
   - Known limitations: <list them; explicitly write "none" when there are none>
   ```

Reason: outsiders make an immediate judgment about repository reliability from "is the badge green?" Handwritten green cannot be distinguished from machine green, and one handwritten green **damages the evidentiary value of green across every family repository**. Conversely, hiding "uninspected" by placing no badge is the other side of the same lie (measurement: nine handwritten green badges coexisted with repositories that had no CI and displayed nothing). Restricting displays to machine-connected states makes green = inspection ran / grey = no inspection mean the same thing everywhere.

Making the boundary explicit:

- The subject is a display that can impersonate an inspection result — factual badges (language, license, version; blue family) remain unrestricted
- **You are always free to state no numbers** (this clause says "if you write one, be honest," plus "public repositories must display CI state")
- A private scratch repository that is neither public nor has a README is naturally N/A. A repository that **is public but has no README** enters scope when it takes a lane to establish a README (B8, etc.) — lack of a README is not a permanent exemption
- Turning this clause into checks (detecting static green badges, stale numbers, and so on) follows [R-6](09-rejection-rubric.md) and is tracked in Issues

## Appendix (Non-Normative) — Recommended Runner Cheat Sheet

The clause requires only "set up a runner + CI." Tool selection is the implementer's discretion, and this table is a **non-normative reference**. Updating the table does not count as a clause revision.

| Language / Runtime | Recommended runner | Note |
|---|---|---|
| TypeScript / JavaScript (Node) | vitest | `node:test` is also fine if the standard library is enough |
| Python | pytest | — |
| Shell | bats-core | — |
| Go | `go test` | Language standard |
| Rust | `cargo test` | Language standard |
| Swift / iOS | XCTest | Run via `xcodebuild test` |
| CI execution environment | GitHub Actions | The default when the repository lives on GitHub |
