> **Machine translation.** The Japanese original ([10-test-ci-baseline.md](../../../docs/10-test-ci-baseline.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# T Test & CI Baseline — the Layer that Mechanically Accumulates Proof of Correctness

Where the L layers (L2 / L1 / L0) are the contract for **how work proceeds**, and the R layer is the contract for **what gets accepted**, the T layer defines the contract for **the minimum a repository must do to keep proving its own correctness through tests and CI — initial setup, accumulating regression tests, baking it into the delegation format, and never merging while red**. Each rule carries a stable rule ID (`T-1` through `T-4`), and the scope of application for each clause is noted in 〔 〕. The summary side ([docs/04](04-adoption.md)) references these IDs. The general principle of enforcing a gate as a check is [R-6](09-rejection-rubric.md); the stance to take when verification isn't possible is [docs/05](05-fail-posture.md).

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
