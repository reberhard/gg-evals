# Install for Agents

Idempotent setup guide for an AI agent (Claude Code, Cursor, etc.) to install and verify GuardBench from a clean checkout.

## Step 1 — Clone and enter

```bash
git clone https://github.com/<owner>/gg-evals.git
cd gg-evals
```

Verify: `pwd` ends with `gg-evals`. `git log --oneline | head -1` shows a commit.

## Step 2 — Python environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -V
```

Verify: `python -V` reports `3.11.x`. `which python` ends with `gg-evals/.venv/bin/python`.

## Step 3 — Install

```bash
pip install -e .[dev]
```

Verify: `which guardbench` ends with `gg-evals/.venv/bin/guardbench`. `guardbench --help` shows the CLI.

## Step 4 — List evals

```bash
guardbench list
```

Verify: output lists `assertion-auditor` and `spec-drift` under v0.1 scaffolded.

## Step 5 — Smoke run (placeholder until Phase B)

```bash
guardbench run --tier smoke
```

v0.1 status: this is a stub that exits 0 and prints "Phase B work". Real smoke runs land when the assertion-auditor adapter and corpus ship.

## Step 6 — Tests

```bash
pytest -q
```

Verify: tests pass (or "no tests collected" until Phase B). Lint is clean: `ruff check .`.

## Troubleshooting

- **`guardbench: command not found`** — `.venv` not activated. Run `source .venv/bin/activate`.
- **`ModuleNotFoundError: eval`** — installed without `-e`. Re-run `pip install -e .[dev]`.
- **Python version mismatch** — `python -V` reports < 3.11. Install Python 3.11 (e.g. `brew install python@3.11` on macOS).

## Upgrading

```bash
git pull
pip install -e .[dev] --upgrade
```

If the corpus version bumps, reports for the prior version stay in `docs/benchmarks/` — never mutated. New version reports land alongside.
