"""Графіки execution time та speedup (потрібен matplotlib; необов'язково)."""

from __future__ import annotations

from pathlib import Path

from benchmark import Row


def save_plots(rows: list[Row], directory: Path) -> list[Path]:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib не встановлено — графіки пропущено (pip install matplotlib)")
        return []

    saved: list[Path] = []
    operations = sorted({(r.operation, r.size) for r in rows})

    # 1) Час виконання за методами (найбільший розмір кожної операції)
    largest: dict[str, int] = {}
    for name, size in operations:
        largest[name] = max(largest.get(name, 0), size)
    for name, size in largest.items():
        subset = [r for r in rows if r.operation == name and r.size == size]
        labels = [f"{r.method}" + (f" ({r.workers})" if r.workers else "") for r in subset]
        fig, axis = plt.subplots(figsize=(9, 4.5))
        axis.barh(labels, [r.mean for r in subset])
        axis.set_xscale("log")
        axis.set_xlabel("Середній час, s (лог. шкала)")
        axis.set_title(f"{name}: {size:,} книг".replace(",", " "))
        axis.invert_yaxis()
        fig.tight_layout()
        path = directory / f"time_{name}.png"
        fig.savefig(path, dpi=130)
        plt.close(fig)
        saved.append(path)

    # 2) Speedup залежно від кількості workers (threads vs processes)
    scoring = [r for r in rows if r.operation == "scores" and r.workers]
    if scoring:
        size = max(r.size for r in scoring)
        fig, axis = plt.subplots(figsize=(6.5, 4.5))
        for method in sorted({r.method for r in scoring}):
            series = sorted((r.workers, r.speedup) for r in scoring if r.method == method and r.size == size)
            axis.plot(*zip(*series), marker="o", label=method)
        axis.axhline(1.0, linestyle="--", linewidth=0.8, color="gray")
        axis.set_xlabel("Workers")
        axis.set_ylabel("Speedup відносно sequential")
        axis.set_title(f"Scaling: {size:,} книг".replace(",", " "))
        axis.legend()
        fig.tight_layout()
        path = directory / "speedup_workers.png"
        fig.savefig(path, dpi=130)
        plt.close(fig)
        saved.append(path)
    return saved
