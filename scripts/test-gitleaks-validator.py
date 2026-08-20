#!/usr/bin/env python3
"""Exercise the validator embedded in reusable-gitleaks.yml."""

from pathlib import Path
import subprocess
import sys


WORKFLOW = Path(".github/workflows/reusable-gitleaks.yml")
CONFIG = Path("/tmp/gitleaks-base-config.toml")
STEP_NAME = "Scan PR commit range"


def indentation(line):
    return len(line) - len(line.lstrip(" "))


def extract_run_block(lines):
    step_markers = []
    for index, line in enumerate(lines):
        if line.strip() == "- name: " + STEP_NAME:
            step_markers.append((index, indentation(line)))
    if len(step_markers) != 1:
        raise ValueError(
            "expected exactly one named workflow step, found "
            + str(len(step_markers))
        )

    step_start, step_indent = step_markers[0]
    run_markers = []
    for index in range(step_start + 1, len(lines)):
        line = lines[index]
        if line.strip() and indentation(line) <= step_indent:
            break
        if line.strip() == "run: |":
            run_markers.append((index, indentation(line)))
    if len(run_markers) != 1:
        raise ValueError(
            "expected exactly one literal run block in named step, found "
            + str(len(run_markers))
        )

    run_start, run_indent = run_markers[0]
    raw_block = []
    for line in lines[run_start + 1 :]:
        if line.strip() and indentation(line) <= run_indent:
            break
        raw_block.append(line)
    nonempty = [indentation(line) for line in raw_block if line.strip()]
    if not nonempty:
        raise ValueError("named workflow step has an empty run block")
    content_indent = min(nonempty)
    if content_indent <= run_indent:
        raise ValueError("literal run block is not indented beneath run: |")
    return [line[content_indent:] if line.strip() else "" for line in raw_block]


def extract_validator(workflow):
    run_lines = extract_run_block(workflow.read_text(encoding="utf-8").splitlines())
    opening = [
        index for index, line in enumerate(run_lines) if line.strip() == "python3 -c '"
    ]
    closing = [
        index for index, line in enumerate(run_lines) if line.strip() == "' || exit 1"
    ]
    if len(opening) != 1 or len(closing) != 1 or closing[0] <= opening[0]:
        raise ValueError(
            "expected one complete single-quoted python3 -c validator payload"
        )
    validator = "\n".join(run_lines[opening[0] + 1 : closing[0]]) + "\n"
    if not validator.strip():
        raise ValueError("extracted validator payload is empty")
    if "'" in validator:
        raise ValueError("validator payload contains a single quote that breaks shell quoting")
    return validator


CASES = (
    ("canonical-use-default", "[extend]\nuseDefault = true\n", True),
    ("uppercase-path", '[EXTEND]\npath = "evil.toml"\n', False),
    ("mixed-case-path", '[Extend]\npath = "evil.toml"\n', False),
    ("mixed-case-use-default", "[Extend]\nuseDefault = true\n", False),
    (
        "canonical-then-sibling",
        '[extend]\nuseDefault = true\n[Extend]\npath = "evil.toml"\n',
        False,
    ),
    (
        "sibling-then-canonical",
        '[Extend]\npath = "evil.toml"\n[extend]\nuseDefault = true\n',
        False,
    ),
    ("use-default-extra-key", '[extend]\nuseDefault = true\npath = "evil.toml"\n', False),
    ("use-default-false", "[extend]\nuseDefault = false\n", False),
    ("use-default-integer", "[extend]\nuseDefault = 1\n", False),
    ("use-default-string", '[extend]\nuseDefault = "true"\n', False),
    ("array-of-tables", "[[extend]]\nuseDefault = true\n", False),
    ("dotted-use-default", "extend.useDefault = true\n", True),
    (
        "duplicate-key-parse-error",
        "[extend]\nuseDefault = true\nuseDefault = false\n",
        False,
    ),
    ("non-extend-config", '[rules]\nid = "example"\n', True),
)


def main():
    try:
        validator = extract_validator(WORKFLOW)
    except (OSError, UnicodeError, ValueError) as error:
        print("FAIL validator-extraction: " + str(error))
        return 1

    if CONFIG.exists():
        print("FAIL fixture-path-occupied: " + str(CONFIG))
        return 1

    failures = 0
    try:
        for name, fixture, should_allow in CASES:
            CONFIG.write_text(fixture, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-B", "-c", validator],
                capture_output=True,
                text=True,
                check=False,
            )
            allowed = result.returncode == 0
            error_line = result.stdout.strip()
            valid_denial = allowed or (
                result.returncode == 1 and error_line.startswith("::error::")
            )
            if allowed == should_allow and valid_denial:
                print("PASS " + name + " (" + ("allow" if allowed else "deny") + ")")
            else:
                failures += 1
                expected = "allow" if should_allow else "deny"
                actual = "allow" if allowed else "deny"
                print(
                    "FAIL "
                    + name
                    + " (expected="
                    + expected
                    + " actual="
                    + actual
                    + " exit="
                    + str(result.returncode)
                    + ")"
                )
                if result.stdout:
                    print(result.stdout.rstrip())
                if result.stderr:
                    print(result.stderr.rstrip())
    finally:
        if CONFIG.exists():
            CONFIG.unlink()

    print("summary fixtures=" + str(len(CASES)) + " failures=" + str(failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
