#!/usr/bin/env bash
# Single-command full eval run. Wraps `guardbench run` with sensible defaults
# for a published-tier sweep.
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -d .venv ]; then
    echo "no .venv detected — run: python3.11 -m venv .venv && source .venv/bin/activate && pip install -e ."
    exit 1
fi

# shellcheck disable=SC1091
source .venv/bin/activate

guardbench run --tier "${TIER:-dev}" --seed "${SEED:-20260509}" "$@"
