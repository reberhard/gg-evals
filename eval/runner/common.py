"""Shared eval runner machinery."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from eval.runner.adapters import adapter_names, get_adapter
from eval.shared.corpus import deterministic_sample_aligned, load_corpus
from eval.shared.report import write_report
from eval.shared.scoring import ScoreResult, score_predictions

TIER_SAMPLE_SIZE = {
    "smoke": 1,
    "dev": 5,
    "published": None,
}


@dataclass(frozen=True)
class RunResult:
    eval_name: str
    adapter: str
    tier: str
    seed: int
    score: ScoreResult
    corpus_version: str
    report_path: Path | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "eval": self.eval_name,
            "adapter": self.adapter,
            "tier": self.tier,
            "seed": self.seed,
            "n": self.score.n,
            "precision": self.score.precision,
            "recall": self.score.recall,
            "f1": self.score.f1,
            "tp": self.score.tp,
            "fp": self.score.fp,
            "tn": self.score.tn,
            "fn": self.score.fn,
            "report_path": str(self.report_path) if self.report_path else None,
        }


def run_eval(
    eval_name: str,
    tier: str,
    seed: int,
    adapter: str | None = None,
    report: bool = False,
) -> list[RunResult]:
    """Run one eval against one adapter or all registered adapters."""
    inputs, labels = load_corpus(eval_name, ["fixtures"])
    if not inputs:
        raise ValueError(f"no corpus fixtures found for {eval_name}")

    sampled_inputs, sampled_labels = deterministic_sample_aligned(
        inputs,
        labels,
        TIER_SAMPLE_SIZE[tier],
        seed,
    )
    selected_adapter_names = [adapter] if adapter else adapter_names(eval_name)
    results: list[RunResult] = []
    for adapter_name in selected_adapter_names:
        selected_adapter = get_adapter(eval_name, adapter_name)
        predictions = [selected_adapter.predict(row) for row in sampled_inputs]
        score = score_predictions(predictions, sampled_labels)
        report_path = None
        should_write_report = report or tier == "published"
        if should_write_report:
            report_path = write_report(
                eval_name=eval_name,
                adapter=selected_adapter.name,
                score_result=score,
                corpus_version=f"{eval_name}/fixtures",
                seed=seed,
                notes=f"Tier: {tier}. Adapter: {selected_adapter.name}.",
            )
        results.append(
            RunResult(
                eval_name=eval_name,
                adapter=selected_adapter.name,
                tier=tier,
                seed=seed,
                score=score,
                corpus_version=f"{eval_name}/fixtures",
                report_path=report_path,
            )
        )
    return results
