"""Threading / multiprocessing / ThreadPoolExecutor / ProcessPoolExecutor.

Усі функції, що виконуються в процесах, оголошені на рівні модуля, щоб їх можна
було серіалізувати (pickle) — це обов'язково для Windows (spawn).
"""

from __future__ import annotations

import csv
import json
import math
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
from pathlib import Path

from book_manager.analytics import DEFAULT_SCORE_ITERATIONS, book_score
from book_manager.models import Book


# --------------------------------------------------------------------------
# CPU-bound: рейтинговий індекс книг
# --------------------------------------------------------------------------
def calculate_scores_threads(
    pages: list[int], workers: int = 4, iterations: int = DEFAULT_SCORE_ITERATIONS
) -> list[float]:
    """ThreadPoolExecutor: через GIL прискорення для CPU-bound не гарантоване."""
    function = partial(book_score, iterations=iterations)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(function, pages))


def calculate_scores_processes(
    pages: list[int],
    workers: int = 4,
    iterations: int = DEFAULT_SCORE_ITERATIONS,
    chunksize: int | None = None,
) -> list[float]:
    """ProcessPoolExecutor: кожен процес має власний інтерпретатор і GIL."""
    if chunksize is None:
        chunksize = max(1, len(pages) // (workers * 4))
    function = partial(book_score, iterations=iterations)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(function, pages, chunksize=chunksize))


# --------------------------------------------------------------------------
# Паралельна статистика сторінок (розбиття на частини + злиття)
# --------------------------------------------------------------------------
def _chunk_moments(values: list[int]) -> tuple[int, float, float, int, int]:
    """(кількість, середнє, M2, min, max) для однієї частини."""
    count = len(values)
    mean = sum(values) / count
    m2 = sum((value - mean) ** 2 for value in values)
    return count, mean, m2, min(values), max(values)


def split_chunks(values: list[int], parts: int) -> list[list[int]]:
    size = max(1, math.ceil(len(values) / parts))
    return [values[i : i + size] for i in range(0, len(values), size)]


def merge_moments(parts: list[tuple[int, float, float, int, int]]) -> dict[str, float]:
    """Злиття часткових результатів (алгоритм Chan et al.) — без втрати точності."""
    count, mean, m2 = 0, 0.0, 0.0
    minimum, maximum = parts[0][3], parts[0][4]
    for part_count, part_mean, part_m2, part_min, part_max in parts:
        delta = part_mean - mean
        total = count + part_count
        m2 += part_m2 + delta**2 * count * part_count / total
        mean += delta * part_count / total
        count = total
        minimum = min(minimum, part_min)
        maximum = max(maximum, part_max)
    return {
        "average": mean,
        "minimum": float(minimum),
        "maximum": float(maximum),
        "std": math.sqrt(m2 / count),
    }


def pages_statistics_threads(values: list[int], workers: int = 4) -> dict[str, float]:
    if not values:
        raise ValueError("Порожній набір даних")
    with ThreadPoolExecutor(max_workers=workers) as executor:
        parts = list(executor.map(_chunk_moments, split_chunks(values, workers)))
    return merge_moments(parts)


def pages_statistics_processes(values: list[int], workers: int = 4) -> dict[str, float]:
    if not values:
        raise ValueError("Порожній набір даних")
    with ProcessPoolExecutor(max_workers=workers) as executor:
        parts = list(executor.map(_chunk_moments, split_chunks(values, workers)))
    return merge_moments(parts)


# --------------------------------------------------------------------------
# I/O-bound: паралельне читання JSON/CSV-файлів каталогу
# --------------------------------------------------------------------------
def write_catalog_files(
    books: list[Book], directory: Path, files_count: int = 8, fmt: str = "json"
) -> list[Path]:
    """Розбиває каталог на files_count файлів (json або csv)."""
    if fmt not in {"json", "csv"}:
        raise ValueError("Підтримуються лише json та csv")
    directory.mkdir(parents=True, exist_ok=True)
    size = math.ceil(len(books) / files_count)
    paths = []
    for index in range(files_count):
        part = books[index * size : (index + 1) * size]
        path = directory / f"catalog_{index:02d}.{fmt}"
        if fmt == "json":
            rows = [
                {"title": b.title, "author": b.author, "year": b.year, "pages": b.pages}
                for b in part
            ]
            path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
        else:
            with path.open("w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["title", "author", "year", "pages"])
                writer.writerows((b.title, b.author, b.year, b.pages) for b in part)
        paths.append(path)
    return paths


def load_catalog_file(path: Path, latency: float = 0.0) -> list[Book]:
    """Читає один файл. ``latency`` моделює повільний диск/мережу (sleep)."""
    if latency:
        time.sleep(latency)
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return [Book(r["title"], r["author"], int(r["year"]), int(r["pages"])) for r in json.loads(text)]
    if path.suffix == ".csv":
        reader = csv.DictReader(text.splitlines())
        return [Book(r["title"], r["author"], int(r["year"]), int(r["pages"])) for r in reader]
    raise ValueError(f"Непідтримуваний формат: {path.suffix}")


def load_files_sequential(paths: list[Path], latency: float = 0.0) -> list[Book]:
    books: list[Book] = []
    for path in paths:
        books.extend(load_catalog_file(path, latency))
    return books


def load_files_threads(paths: list[Path], workers: int = 8, latency: float = 0.0) -> list[Book]:
    function = partial(load_catalog_file, latency=latency)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        parts = list(executor.map(function, paths))  # порядок файлів зберігається
    return [book for part in parts for book in part]
