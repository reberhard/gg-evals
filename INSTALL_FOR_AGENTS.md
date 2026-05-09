# Install for Agents

Idempotent setup guide for an AI agent (Claude Code, Cursor, etc.) to install and verify GuardBench from a clean checkout.

GuardBench is the Codex-friendly verification lane for the GG harness. It is not
the production agent runtime: live GG agents, Telegram RC sessions, Claude Code
hooks, and boot-context injection remain on Claude Code unless a future
benchmark-backed roadmap phase explicitly changes that boundary.

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

## Step 5 — Smoke run

```bash
guardbench run assertion-auditor --tier smoke
guardbench run spec-drift --tier smoke
```

Verify: both commands print `precision`, `recall`, `f1`, `tp`, `fp`, `tn`, and `fn`.

## Step 6 — Tests

```bash
pytest -q
ruff check .
guardbench run --tier smoke
```

Verify: tests pass, lint is clean, and both v0.1 smoke evals print metric lines.

Optional local pre-push equivalent:

```bash
scripts/pre_push.sh
```

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
