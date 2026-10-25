"""Невеликий benchmark-фреймворк: повтори, середнє/медіана, speedup, пам'ять, CSV."""

from __future__ import annotations

import csv
import statistics
import tracemalloc
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from time import perf_counter


@dataclass
class Variant:
    method: str
    workers: int | None  # None -> не застосовується (NumPy, cache)
    run: Callable[[], object]


@dataclass
class Row:
    operation: str
    size: int
    method: str
    workers: int | None
    times: list[float]
    peak_memory_mb: float | None
    correct: bool
    speedup: float = 1.0
    mean: float = field(init=False)
    median: float = field(init=False)

    def __post_init__(self) -> None:
        self.mean = statistics.mean(self.times)
        self.median = statistics.median(self.times)


def time_runs(function: Callable[[], object], repeats: int) -> tuple[list[float], object]:
    times, result = [], None
    for _ in range(repeats):
        start = perf_counter()
        result = function()
        times.append(perf_counter() - start)
    return times, result


def peak_memory_mb(function: Callable[[], object]) -> float:
    """Пік Python-allocated пам'яті поточного процесу (tracemalloc)."""
    tracemalloc.start()
    try:
        function()
        return tracemalloc.get_traced_memory()[1] / 1024 / 1024
    finally:
        tracemalloc.stop()


def run_operation(
    operation: str,
    size: int,
    variants: list[Variant],
    equal: Callable[[object, object], bool],
    repeats: int,
    measure_memory: bool = True,
) -> list[Row]:
    """Перший варіант — baseline. Усі результати порівнюються з ним."""
    rows: list[Row] = []
    baseline_result, baseline_mean = None, None
    for index, variant in enumerate(variants):
        times, result = time_runs(variant.run, repeats)
        if index == 0:
            baseline_result, correct = result, True
            baseline_mean = statistics.mean(times)
        else:
            correct = bool(equal(baseline_result, result))
        memory = peak_memory_mb(variant.run) if measure_memory else None
        row = Row(operation, size, variant.method, variant.workers, times, memory, correct)
        row.speedup = baseline_mean / row.mean if row.mean else float("inf")
        rows.append(row)
        flag = "" if correct else "  !!! РЕЗУЛЬТАТ НЕ ЗБІГАЄТЬСЯ З BASELINE"
        workers = "-" if variant.workers is None else variant.workers
        print(f"  {variant.method:<28} w={workers!s:<2} mean={row.mean:9.5f}s  x{row.speedup:7.2f}{flag}")
    return rows


def save_csv(rows: list[Row], path: Path) -> None:
    repeats = max(len(row.times) for row in rows)
    header = ["operation", "data_size", "method", "workers"]
    header += [f"run_{i}" for i in range(1, repeats + 1)]
    header += ["mean_s", "median_s", "peak_memory_mb", "speedup", "correct"]
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for row in rows:
            runs = [f"{t:.6f}" for t in row.times] + [""] * (repeats - len(row.times))
            writer.writerow(
                [row.operation, row.size, row.method, "" if row.workers is None else row.workers]
                + runs
                + [
                    f"{row.mean:.6f}",
                    f"{row.median:.6f}",
                    "" if row.peak_memory_mb is None else f"{row.peak_memory_mb:.2f}",
                    f"{row.speedup:.2f}",
                    row.correct,
                ]
            )


def save_markdown(rows: list[Row], path: Path) -> None:
    lines = ["# Результати benchmark", ""]
    current = None
    for row in rows:
        key = (row.operation, row.size)
        if key != current:
            current = key
            lines += [
                "",
                f"## {row.operation} — {row.size:,} книг".replace(",", " "),
                "",
                "| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |",
                "|---|---|---|---|---|---|---|",
            ]
        memory = "–" if row.peak_memory_mb is None else f"{row.peak_memory_mb:.2f}"
        workers = "–" if row.workers is None else str(row.workers)
        lines.append(
            f"| {row.method} | {workers} | {row.mean:.5f} | {row.median:.5f} | {memory} "
            f"| {row.speedup:.2f}× | {'так' if row.correct else 'НІ'} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
