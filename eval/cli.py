"""GuardBench CLI entry point.

Usage:
    guardbench run [<eval>] [--tier smoke|dev|published] [--adapter <name>] [--seed <int>] [--report]
    guardbench corpus add <eval> --input <text> --label <tp|fp|tn|fn> [--cluster <tag>]
    guardbench list

The CLI is intentionally thin — the eval modules in eval/runner/ own the work.
"""

from __future__ import annotations

import sys

import click


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
    click.echo(f"[stub] guardbench run eval={eval_name or 'all'} tier={tier} adapter={adapter} seed={seed} report={report}")
    click.echo("Phase B work — eval runners not yet implemented.")
    sys.exit(0)


@main.command(name="list")
def list_evals() -> None:
    """List available evals and their corpora."""
    click.echo("Available evals (v0.1 scaffolded):")
    click.echo("  assertion-auditor    — confident-wrong claim detection")
    click.echo("  spec-drift           — spec-vs-reality drift detection")
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
    sys.exit(0)


if __name__ == "__main__":
    main()
