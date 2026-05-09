"""GuardBench CLI entry point.

Usage:
    guardbench run [<eval>] [--tier smoke|dev|published] [--adapter <name>] [--seed <int>] [--report]
    guardbench corpus add <eval> --input <text> --label <tp|fp|tn|fn> [--cluster <tag>]
    guardbench list

The CLI is intentionally thin — the eval modules in eval/runner/ own the work.
"""

from __future__ import annotations

import click

from eval.runner.adapters import DEFAULT_ADAPTER, adapter_names
from eval.runner.all import EVALS_V0_1, run_all
from eval.runner.common import run_eval


@click.group()
def main() -> None:
    """GuardBench — public benchmark for AI-agent verification stacks."""


@main.command()
@click.argument("eval_name", required=False)
@click.option(
    "--tier",
    type=click.Choice(["smoke", "dev", "published"]),
    default="smoke",
    help="Run tier. smoke=N1 (CI), dev=N5 (local), published=full corpus (write report).",
)
@click.option("--adapter", default=None, help="Specific adapter to run. Default: all.")
@click.option("--seed", type=int, default=20260507, help="Deterministic seed.")
@click.option("--report", is_flag=True, help="Write a dated report under docs/benchmarks/.")
def run(eval_name: str | None, tier: str, adapter: str | None, seed: int, report: bool) -> None:
    """Run an eval or all evals."""
    if eval_name is not None and eval_name not in EVALS_V0_1:
        raise click.ClickException(f"unknown eval: {eval_name}")
    if eval_name is None and adapter is not None:
        raise click.ClickException("--adapter is only valid when running a single eval")

    results = (
        [result.as_dict() for result in run_eval(eval_name, tier, seed, adapter, report)]
        if eval_name
        else run_all(tier, seed, report)
    )
    for result in results:
        click.echo(
            "{eval} adapter={adapter} tier={tier} n={n} "
            "precision={precision:.3f} recall={recall:.3f} f1={f1:.3f} "
            "tp={tp} fp={fp} tn={tn} fn={fn}".format(**result)
        )
        if result["report_path"]:
            click.echo(f"report={result['report_path']}")


@main.command(name="list")
def list_evals() -> None:
    """List available evals and their corpora."""
    click.echo("Available evals (v0.1 runnable):")
    click.echo(
        "  assertion-auditor    — confident-wrong claim detection "
        f"(default adapter: {DEFAULT_ADAPTER['assertion-auditor']}; "
        f"adapters: {', '.join(adapter_names('assertion-auditor'))})"
    )
    click.echo(
        "  spec-drift           — spec-vs-reality drift detection "
        f"(default adapter: {DEFAULT_ADAPTER['spec-drift']}; "
        f"adapters: {', '.join(adapter_names('spec-drift'))})"
    )
    click.echo("")
    click.echo("v0.2+:")
    click.echo("  agent-domain-gate    — cross-agent boundary violations")
    click.echo("  recipient-language-gate — language-recipient mismatch")
    click.echo("  time-arithmetic-gate — date/DOW/elapsed correctness")
    click.echo("  mandate-gate         — domain-boundary classifier")
    click.echo("  wa-draft-gate        — pre-send draft hygiene")
    click.echo("  output-canary        — brief/aviso structural compliance")


@main.group()
def corpus() -> None:
    """Corpus management."""


@corpus.command(name="add")
@click.argument("eval_name")
@click.option("--input", "input_text", required=True, help="The fixture input text.")
@click.option("--label", required=True, type=click.Choice(["tp", "fp", "tn", "fn"]))
@click.option("--cluster", default=None, help="FP/TP cluster tag.")
def corpus_add(eval_name: str, input_text: str, label: str, cluster: str | None) -> None:
    """Add a labeled fixture to a corpus."""
    click.echo(f"[stub] corpus add {eval_name} label={label} cluster={cluster}")
    click.echo("Phase B work — corpus add not yet implemented.")


if __name__ == "__main__":
    main()
