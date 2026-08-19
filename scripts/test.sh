#!/bin/sh

# The handbook's T-6-conformant test runner. Suite totals are derived from the
# registrations below; do not replace the bookkeeping with a literal summary.

python_bin=${PYTHON_BIN:-python3}
declared=0
executed=0
skipped=0
failures=0
active_suite=

register_suite() {
    declared=$((declared + 1))
}

finish() {
    status=$?
    trap - EXIT HUP INT TERM
    printf 'suites: declared=%s executed=%s skipped=%s\n' "$declared" "$executed" "$skipped"
    if [ "$status" -ne 0 ]; then
        exit "$status"
    fi
    if [ "$failures" -ne 0 ]; then
        exit 1
    fi
}

interrupt() {
    interrupt_signal=$1
    if [ -n "$active_suite" ]; then
        executed=$((executed + 1))
    fi
    failures=$((failures + 1))
    printf 'FAIL runner-interrupted (suite=%s signal=%s)\n' "${active_suite:-none}" "$interrupt_signal"
    exit 1
}

trap finish EXIT
trap 'interrupt HUP' HUP
trap 'interrupt INT' INT
trap 'interrupt TERM' TERM

register_suite # README files are present and non-empty.
register_suite # The four localized READMEs have matching structure.
register_suite # Seat-resolver unit tests.
register_suite # Seat-resolver conformance vectors.

if [ "$#" -ne 0 ]; then
    printf 'FAIL usage (expected=no-arguments)\n' >&2
    exit 2
fi

if ! command -v "$python_bin" >/dev/null 2>&1; then
    printf 'missing-dep: %s\n' "$python_bin" >&2
    exit 127
fi

check_readmes() {
    for file in README.ja.md README.md README.zh.md README.th.md i18n/README.md; do
        if [ ! -s "$file" ]; then
            printf 'empty README: %s\n' "$file" >&2
            return 1
        fi
    done
}

run_suite() {
    suite_name=$1
    shift
    active_suite=$suite_name
    if "$@"; then
        active_suite=
        executed=$((executed + 1))
        printf 'PASS %s\n' "$suite_name"
    else
        suite_status=$?
        active_suite=
        executed=$((executed + 1))
        failures=$((failures + 1))
        printf 'FAIL %s (exit=%s)\n' "$suite_name" "$suite_status"
    fi
}

run_conformance() {
    conformance_output=$("$python_bin" -B templates/seat-resolver/bin/run-conformance 2>&1)
    conformance_status=$?
    if [ "$conformance_status" -eq 0 ]; then
        conformance_result=PASS
    else
        conformance_result=FAIL
    fi
    while IFS= read -r output_line; do
        case "$output_line" in
            "summary "*)
                printf '%s conformance-vectors %s\n' "$conformance_result" "${output_line#summary }"
                ;;
            *)
                printf '%s\n' "$output_line"
                ;;
        esac
    done <<EOF
$conformance_output
EOF
    return "$conformance_status"
}

run_suite readme-nonempty check_readmes
run_suite readme-structure "$python_bin" -B scripts/readme-check/inspect_readme.py langs README.ja.md README.md README.zh.md README.th.md
run_suite seat-resolver-unit "$python_bin" -B -m unittest discover -s templates/seat-resolver/tests -v
run_suite seat-resolver-conformance run_conformance

if [ "$failures" -ne 0 ]; then
    exit 1
fi
