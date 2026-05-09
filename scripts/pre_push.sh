#!/usr/bin/env bash
# Local pre-push check for GuardBench changes.
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -x .venv/bin/ruff ]; then
    RUFF=.venv/bin/ruff
    PYTEST=.venv/bin/pytest
else
    RUFF=ruff
    PYTEST=pytest
fi

run_guardbench() {
    if [ -x .venv/bin/guardbench ]; then
        .venv/bin/guardbench "$@"
    elif command -v guardbench >/dev/null 2>&1; then
        guardbench "$@"
    else
        python3 -m eval.cli "$@"
    fi
}

"$RUFF" check .
"$PYTEST" -q
run_guardbench run --tier smoke
python3 scripts/report_summary.py --check --min-precision 0.8 --min-recall 0.4 >/dev/null
