"""Профілювання: cProfile (час) та tracemalloc (пам'ять).

Запуск:  python -m book_manager.profiling --size 50000
"""

from __future__ import annotations

import argparse
import cProfile
import io
import pstats
import tracemalloc
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from book_manager.analytics import catalog_report_python, generate_books


@dataclass(slots=True)
class ProfileResult:
    text: str  # таблиця pstats (sort by cumulative)
    total_time: float  # сумарний час профілювання, s
    bottleneck: str  # функція analytics.py з найбільшим cumtime
    bottleneck_cumtime: float
    bottleneck_share: float  # частка від total_time, %


def profile_callable(
    function: Callable, *args, top: int = 15, prof_file: Path | None = None, **kwargs
) -> ProfileResult:
    profiler = cProfile.Profile()
    profiler.enable()
    function(*args, **kwargs)
    profiler.disable()
    if prof_file is not None:
        profiler.dump_stats(str(prof_file))

    buffer = io.StringIO()
    stats = pstats.Stats(profiler, stream=buffer).sort_stats("cumulative")
    stats.print_stats(top)

    # Bottleneck: найдорожча (за cumtime) функція проєкту, крім функції-обгортки.
    own = [
        (key[2], values[3])
        for key, values in stats.stats.items()  # type: ignore[attr-defined]
        if key[0].endswith("analytics.py") and key[2] != function.__name__
    ]
    name, cumtime = max(own, key=lambda item: item[1], default=("-", 0.0))
    total = stats.total_tt  # type: ignore[attr-defined]
    return ProfileResult(buffer.getvalue(), total, name, cumtime, cumtime / total * 100 if total else 0.0)


def measure_memory(function: Callable, *args, **kwargs) -> tuple[float, float]:
    """(current, peak) у MB для Python-allocated пам'яті."""
    tracemalloc.start()
    try:
        function(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return current / 1024 / 1024, peak / 1024 / 1024


def top_allocations(function: Callable, *args, limit: int = 10, **kwargs) -> list[str]:
    """Рядки коду, що виділили найбільше пам'яті."""
    tracemalloc.start()
    try:
        function(*args, **kwargs)
        snapshot = tracemalloc.take_snapshot()
    finally:
        tracemalloc.stop()
    return [str(stat) for stat in snapshot.statistics("lineno")[:limit]]


def main() -> None:
    parser = argparse.ArgumentParser(description="Профілювання каталогу книг")
    parser.add_argument("--size", type=int, default=50_000, help="кількість книг")
    parser.add_argument("--out", type=Path, default=Path("benchmarks/results"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    books = generate_books(args.size)
    result = profile_callable(catalog_report_python, books, prof_file=args.out / "profile.prof")
    current, peak = measure_memory(catalog_report_python, books)
    allocations = top_allocations(catalog_report_python, books)

    report = [
        f"Каталог: {args.size} книг",
        f"Bottleneck: {result.bottleneck}",
        f"  cumtime = {result.bottleneck_cumtime:.3f} s ({result.bottleneck_share:.1f}% від {result.total_time:.3f} s)",
        f"tracemalloc: current = {current:.2f} MB, peak = {peak:.2f} MB",
        "",
        "=== cProfile (sort by cumulative) ===",
        result.text,
        "=== tracemalloc: top рядків за пам'яттю ===",
        *allocations,
    ]
    text = "\n".join(report)
    (args.out / "profile_report.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
