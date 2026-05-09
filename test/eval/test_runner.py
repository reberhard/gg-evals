from __future__ import annotations

from click.testing import CliRunner

from eval.cli import main
from eval.runner.adapters import adapter_names, get_adapter
from eval.runner.common import run_eval


def test_adapter_registration() -> None:
    assert adapter_names("assertion-auditor") == ["regex-only"]
    assert get_adapter("spec-drift").name == "keyword"


def test_run_eval_smoke_executes_reference_adapter() -> None:
    results = run_eval("assertion-auditor", "smoke", 20260509)

    assert len(results) == 1
    assert results[0].score.n == 1
    assert results[0].adapter == "regex-only"


def test_cli_runs_single_eval() -> None:
    runner = CliRunner()

    result = runner.invoke(main, ["run", "spec-drift", "--tier", "smoke", "--seed", "1"])

    assert result.exit_code == 0
    assert "spec-drift adapter=keyword tier=smoke" in result.output
    assert "precision=" in result.output
