#!/usr/bin/env bash
# Local pre-push check for GuardBench changes.
set -euo pipefail

cd "$(dirname "$0")/.."

run_ruff() {
    if [ -x .venv/bin/ruff ]; then
        .venv/bin/ruff "$@"
    elif command -v ruff >/dev/null 2>&1; then
        ruff "$@"
    else
        python3 -m ruff "$@"
    fi
}

run_pytest() {
    if [ -x .venv/bin/pytest ]; then
        .venv/bin/pytest "$@"
    elif command -v pytest >/dev/null 2>&1; then
        pytest "$@"
    else
        python3 -m pytest "$@"
    fi
}

run_guardbench() {
    if [ -x .venv/bin/guardbench ]; then
        .venv/bin/guardbench "$@"
    elif command -v guardbench >/dev/null 2>&1; then
        guardbench "$@"
    else
        python3 -m eval.cli "$@"
    fi
}

run_ruff check .
run_pytest -q
run_guardbench run --tier smoke
python3 scripts/report_summary.py --check --min-precision 0.8 --min-recall 0.4 >/dev/null
