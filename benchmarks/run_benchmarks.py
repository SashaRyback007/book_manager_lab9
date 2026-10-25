"""Запуск усіх експериментів ЛР №9 (варіант 2).

    python benchmarks/run_benchmarks.py            # повний запуск
    python benchmarks/run_benchmarks.py --quick    # швидка перевірка

Результати: benchmarks/results/benchmark_results.csv, .md та графіки.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from functools import partial
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
from benchmark import Row, Variant, run_operation, save_csv, save_markdown  # noqa: E402
from plots import save_plots  # noqa: E402

from book_manager import analytics as an  # noqa: E402
from book_manager import parallel as par  # noqa: E402
from book_manager.catalog import BookCatalog  # noqa: E402

AUTHOR_YEARS = (1990, 2010)


# ---- функції порівняння результатів з baseline --------------------------------
def stats_equal(a, b) -> bool:
    return all(np.isclose(a[k], b[k], rtol=1e-9, atol=1e-9) for k in a)


def scores_equal(a, b) -> bool:
    return np.allclose(np.asarray(a), np.asarray(b), rtol=1e-9)


def group_equal(a, b) -> bool:
    return a.keys() == b.keys() and all(np.isclose(a[k], b[k]) for k in a)


def title_index(book) -> int:
    """generate_books дає назви виду 'Book {index}' — звідси відновлюється індекс."""
    return int(book.title.removeprefix("Book "))


def books_vs_indices(a, b) -> bool:
    """a — list[Book] (baseline), b — індекси NumPy."""
    return [title_index(book) for book in a] == b.tolist()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", type=int, nargs="+", default=[10_000, 100_000, 300_000])
    parser.add_argument("--workers", type=int, nargs="+", default=[1, 2, 4, 8])
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--iterations", type=int, default=an.DEFAULT_SCORE_ITERATIONS)
    parser.add_argument("--latency", type=float, default=0.05, help="імітація I/O затримки на файл, s")
    parser.add_argument("--quick", action="store_true", help="малі розміри, 2 повтори")
    parser.add_argument("--out", type=Path, default=ROOT / "benchmarks" / "results")
    args = parser.parse_args()
    if args.quick:
        args.sizes, args.repeats, args.workers, args.iterations = [2_000, 10_000], 2, [1, 2], 10

    args.out.mkdir(parents=True, exist_ok=True)
    print(f"CPU count: {os.cpu_count()} | sizes={args.sizes} | workers={args.workers} | repeats={args.repeats}")
    rows: list[Row] = []

    for size in args.sizes:
        books = an.generate_books(size)
        pages = [b.pages for b in books]
        arrays = an.BookArrays.from_books(books)
        author = books[0].author
        iters = args.iterations
        catalog = BookCatalog(books)

        # 1) статистика сторінок: average / min / max / std ------------------------
        print(f"\n[pages_statistics] {size}")
        variants = [
            Variant("Python loops", 1, lambda: an.pages_statistics_python(pages)),
            Variant("NumPy (list->array)", None, lambda: an.pages_statistics_numpy(pages)),
            Variant("NumPy (готовий array)", None, partial(an.pages_statistics_numpy, arrays.pages)),
        ]
        for w in args.workers:
            variants.append(Variant("ThreadPoolExecutor", w, partial(par.pages_statistics_threads, pages, w)))
            variants.append(Variant("ProcessPoolExecutor", w, partial(par.pages_statistics_processes, pages, w)))
        rows += run_operation("pages_statistics", size, variants, stats_equal, args.repeats)

        # 2) важка CPU-bound операція: рейтинговий індекс -----------------------------
        print(f"\n[scores] {size} (iterations={iters})")
        variants = [Variant("Sequential", 1, partial(an.calculate_scores_sequential, pages, iters))]
        for w in args.workers:
            variants.append(Variant("ThreadPoolExecutor", w, partial(par.calculate_scores_threads, pages, w, iters)))
        for w in args.workers:
            variants.append(Variant("ProcessPoolExecutor", w, partial(par.calculate_scores_processes, pages, w, iters)))
        variants.append(Variant("NumPy vectorized", None, partial(an.calculate_scores_numpy, pages, iters)))
        rows += run_operation("scores", size, variants, scores_equal, args.repeats)

        # 3) пошук за автором -------------------------------------------------------
        print(f"\n[search_by_author] {size}")
        variants = [
            Variant("Python loops", 1, lambda: an.search_by_author_python(books, author)),
            Variant("NumPy (готові arrays)", None, lambda: an.search_by_author_numpy(arrays, author)),
        ]
        rows += run_operation("search_by_author", size, variants, books_vs_indices, args.repeats)

        # 4) фільтрація за роком ----------------------------------------------------
        print(f"\n[filter_by_year] {size}")
        variants = [
            Variant("Python loops", 1, lambda: an.filter_by_year_python(books, *AUTHOR_YEARS)),
            Variant("NumPy (готові arrays)", None, lambda: an.filter_by_year_numpy(arrays, *AUTHOR_YEARS)),
        ]
        rows += run_operation("filter_by_year", size, variants, books_vs_indices, args.repeats)

        # 5) групування за автором --------------------------------------------------
        print(f"\n[group_by_author] {size}")
        variants = [
            Variant("Python loops", 1, lambda: an.group_by_author_python(books)),
            Variant("NumPy (готові arrays)", None, lambda: an.group_by_author_numpy(arrays)),
        ]
        rows += run_operation("group_by_author", size, variants, group_equal, args.repeats)

        # 6) найбільша книга ----------------------------------------------------------
        print(f"\n[longest_book] {size}")
        variants = [
            Variant("Python loops", 1, lambda: an.longest_book_python(books)),
            Variant("NumPy (готові arrays)", None, lambda: an.longest_book_numpy(arrays)),
        ]
        rows += run_operation("longest_book", size, variants, lambda a, b: title_index(a) == b, args.repeats)

        # 7) caching: cold vs warm статистика автора --------------------------------
        print(f"\n[author_statistics_cache] {size}")

        def cold() -> object:
            catalog.clear_cache()
            return catalog.author_statistics(author)

        catalog.author_statistics(author)  # прогрів
        variants = [
            Variant("Без кешу (cold)", None, cold),
            Variant("lru_cache (warm)", None, lambda: catalog.author_statistics(author)),
        ]
        rows += run_operation("author_cache", size, variants, lambda a, b: a == b, max(args.repeats, 5), measure_memory=False)

    # 8) I/O-bound: читання кількох JSON/CSV файлів ------------------------------------
    io_size = args.sizes[-1] if args.quick else args.sizes[min(1, len(args.sizes) - 1)]
    books = an.generate_books(io_size)
    data_dir = args.out / "data"
    try:
        for fmt in ("json", "csv"):
            paths = par.write_catalog_files(books, data_dir / fmt, files_count=8, fmt=fmt)
            for latency in (0.0, args.latency):
                name = f"io_{fmt}_latency_{int(latency * 1000)}ms"
                print(f"\n[{name}] {io_size}")
                variants = [Variant("Sequential I/O", 1, partial(par.load_files_sequential, paths, latency))]
                for w in args.workers:
                    variants.append(Variant("ThreadPoolExecutor", w, partial(par.load_files_threads, paths, w, latency)))
                rows += run_operation(name, io_size, variants, lambda a, b: a == b, args.repeats)
    finally:
        shutil.rmtree(data_dir, ignore_errors=True)

    save_csv(rows, args.out / "benchmark_results.csv")
    save_markdown(rows, args.out / "benchmark_results.md")
    for path in save_plots(rows, args.out):
        print("Графік:", path)
    bad = [r for r in rows if not r.correct]
    print(f"\nЗбережено: {args.out / 'benchmark_results.csv'}")
    if bad:
        raise SystemExit(f"Некоректні результати: {[(r.operation, r.method) for r in bad]}")
    print("Усі реалізації дають результат, що збігається з baseline.")


if __name__ == "__main__":
    main()
