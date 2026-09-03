# Security Policy

The statutes themselves are documentation, but this repository is **not** documentation-only. `templates/` bundles code that adopters copy into their own GitHub Actions and run there:

- `templates/publication-gate/check_publication_gate.py` — the publication-gate check
- `templates/seat-resolver/**` — the deterministic review-seat resolver (Python package, CLI, and conformance tests)
- `templates/ci/` — reusable workflow YAML, shell checks, and `templates/ci/scripts/assemble_review_comment.py`

`scripts/` holds this repository's own check scripts, which run only in this repository's CI. The distributed code uses the Python standard library only (no third-party runtime dependencies), but it still adds an attack surface that a docs-only repository would not have: a flaw in a template runs inside every adopter's CI, with that workflow's token and permissions. Security reports are welcome for:

- Bugs in the distributed templates or scripts that let untrusted input (PR title or body, labels, comments, file names, roster or config JSON) execute code, exfiltrate secrets, or bypass the gate the template implements
- Reusable workflows that request broader `permissions` than they need, or that trust an actor or event they should not
- Leaked credentials, tokens, or personal information anywhere in the repository or its git history
- Links in the documentation that point to malicious or compromised destinations
- Flaws in the protocol itself that could be exploited to bypass its safety mechanisms (e.g., a way to defeat the completion-evidence merge gate while appearing compliant)

## Reporting a Vulnerability

Please report security issues privately via **GitHub's private vulnerability reporting** on this repository (Security → Report a vulnerability). If that is unavailable, open a GitHub issue *without sensitive details* and ask a maintainer to establish a private channel.

We aim to acknowledge reports within 7 days. Please do not disclose the issue publicly until it has been addressed.

## Supported Versions

Only the latest tagged release and the `main` branch are maintained.
