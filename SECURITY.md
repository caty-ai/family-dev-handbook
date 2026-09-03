# Security Policy

The statutes themselves are documentation, but this repository is **not** documentation-only. It distributes code that runs inside adopters' GitHub Actions, in two forms:

- **Reusable workflows** — `.github/workflows/reusable-*.yml` (gitleaks, history-check, pr-size, review-labels, release-sync, test-lint). Adopters call them with `uses: caty-ai/family-dev-handbook/.github/workflows/reusable-<name>.yml@ci-v1`, so a change merged here runs in every calling repository once the `ci-v1` moving tag advances, without the adopter copying anything.
- **Copied templates** — `templates/ci/` (caller stencils for those workflows, plus `check-release-drift.sh`, `check-required-checks.sh`, and `scripts/assemble_review_comment.py`), `templates/publication-gate/check_publication_gate.py` (the publication-gate check), and `templates/seat-resolver/**` (an optional, dependency-free review-seat resolver: Python package, CLI, and conformance tests, adopted once per family rather than copied into each repository).

`scripts/` holds this repository's own check scripts (run by this repository's CI and by `make test`); nothing there is distributed. All distributed Python uses the standard library only (no third-party runtime dependencies), but it still adds an attack surface that a docs-only repository would not have: a flaw in a reusable workflow or template runs inside adopters' CI, with that workflow's token and permissions. Security reports are welcome for:

- Bugs in the reusable workflows or in the copied templates (including their scripts) that let untrusted input (PR title or body, labels, comments, file names, roster or config JSON) execute code, exfiltrate secrets, or bypass the gate they implement
- Reusable workflows that request broader `permissions` than they need, or that trust an actor or event they should not
- Leaked credentials, tokens, or personal information anywhere in the repository or its git history
- Links in the documentation that point to malicious or compromised destinations
- Flaws in the protocol itself that could be exploited to bypass its safety mechanisms (e.g., a way to defeat the completion-evidence merge gate while appearing compliant)

## Reporting a Vulnerability

Please report security issues privately via **GitHub's private vulnerability reporting** on this repository (Security → Report a vulnerability). If that is unavailable, open a GitHub issue *without sensitive details* and ask a maintainer to establish a private channel.

We aim to acknowledge reports within 7 days. Please do not disclose the issue publicly until it has been addressed.

## Supported Versions

Only the latest tagged release and the `main` branch are maintained.
