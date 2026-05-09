#!/usr/bin/env bash
# Local pre-push check for GuardBench changes.
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -x .venv/bin/ruff ]; then
    RUFF=.venv/bin/ruff
    PYTEST=.venv/bin/pytest
    GUARDBENCH=.venv/bin/guardbench
else
    RUFF=ruff
    PYTEST=pytest
    GUARDBENCH=guardbench
fi

"$RUFF" check .
"$PYTEST" -q
"$GUARDBENCH" run --tier smoke
