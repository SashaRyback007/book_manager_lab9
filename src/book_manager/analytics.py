"""Аналітика каталогу книг: baseline (Python loops) та NumPy-версії.

Операції варіанта 2: пошук за автором, фільтрація за роком, групування,
середня кількість сторінок, найбільша книга, статистика авторів.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

import numpy as np

from book_manager.models import Book

DEFAULT_SCORE_ITERATIONS = 30


# --------------------------------------------------------------------------
# Генерація тестових даних
# --------------------------------------------------------------------------
def generate_books(count: int, seed: int = 42, authors_count: int = 1000) -> list[Book]:
    """Детермінований каталог: однаковий seed -> однакові дані."""
    rng = random.Random(seed)
    return [
        Book(
            title=f"Book {index}",
            author=f"Author {rng.randrange(authors_count):04d}",
            year=rng.randint(1900, 2025),
            pages=rng.randint(50, 1200),
        )
        for index in range(count)
    ]


# --------------------------------------------------------------------------
# Baseline: Python loops
# --------------------------------------------------------------------------
def search_by_author_python(books: list[Book], author: str) -> list[Book]:
    result = []
    for book in books:
        if book.author == author:
            result.append(book)
    return result


def filter_by_year_python(books: list[Book], start: int, end: int) -> list[Book]:
    result = []
    for book in books:
        if start <= book.year <= end:
            result.append(book)
    return result


def group_by_author_python(books: list[Book]) -> dict[str, float]:
    """Середня кількість сторінок для кожного автора."""
    totals: dict[str, int] = {}
    counts: dict[str, int] = {}
    for book in books:
        totals[book.author] = totals.get(book.author, 0) + book.pages
        counts[book.author] = counts.get(book.author, 0) + 1
    return {author: totals[author] / counts[author] for author in totals}


def longest_book_python(books: list[Book]) -> Book:
    best = books[0]
    for book in books:
        if book.pages > best.pages:
            best = book
    return best


def pages_statistics_python(values: list[int]) -> dict[str, float]:
    """average / minimum / maximum / std (генеральна, ddof=0) без NumPy."""
    count = len(values)
    if count == 0:
        raise ValueError("Порожній набір даних")
    average = sum(values) / count
    variance = sum((value - average) ** 2 for value in values) / count
    return {
        "average": average,
        "minimum": float(min(values)),
        "maximum": float(max(values)),
        "std": math.sqrt(variance),
    }


# --------------------------------------------------------------------------
# Важка CPU-bound операція: «рейтинговий індекс» книги
# --------------------------------------------------------------------------
def book_score(pages: int, iterations: int = DEFAULT_SCORE_ITERATIONS) -> float:
    value = float(pages)
    for _ in range(iterations):
        value = math.sin(value) ** 2 + math.cos(value) ** 2 + math.sqrt(abs(value) + 1)
    return value


def calculate_scores_sequential(
    pages: list[int], iterations: int = DEFAULT_SCORE_ITERATIONS
) -> list[float]:
    return [book_score(value, iterations) for value in pages]


def calculate_scores_numpy(pages, iterations: int = DEFAULT_SCORE_ITERATIONS) -> np.ndarray:
    """Та сама формула, але цикл по книгах векторизований."""
    value = np.asarray(pages, dtype=np.float64)
    for _ in range(iterations):
        value = np.sin(value) ** 2 + np.cos(value) ** 2 + np.sqrt(np.abs(value) + 1)
    return value


# --------------------------------------------------------------------------
# NumPy: колонкове представлення каталогу + векторизовані операції
# --------------------------------------------------------------------------
@dataclass(slots=True)
class BookArrays:
    """Колонкове представлення каталогу (автори закодовані цілими числами)."""

    authors: list[str]  # словник: код -> ім'я автора
    author_codes: np.ndarray  # int32
    years: np.ndarray  # int16
    pages: np.ndarray  # int32

    @classmethod
    def from_books(cls, books: list[Book]) -> "BookArrays":
        authors = sorted({book.author for book in books})
        code_of = {author: code for code, author in enumerate(authors)}
        return cls(
            authors=authors,
            author_codes=np.fromiter((code_of[b.author] for b in books), np.int32, len(books)),
            years=np.fromiter((b.year for b in books), np.int16, len(books)),
            pages=np.fromiter((b.pages for b in books), np.int32, len(books)),
        )


def search_by_author_numpy(arrays: BookArrays, author: str) -> np.ndarray:
    """Повертає індекси знайдених книг."""
    try:
        code = arrays.authors.index(author)
    except ValueError:
        return np.empty(0, dtype=np.intp)
    return np.flatnonzero(arrays.author_codes == code)


def filter_by_year_numpy(arrays: BookArrays, start: int, end: int) -> np.ndarray:
    return np.flatnonzero((arrays.years >= start) & (arrays.years <= end))


def group_by_author_numpy(arrays: BookArrays) -> dict[str, float]:
    sizes = len(arrays.authors)
    totals = np.bincount(arrays.author_codes, weights=arrays.pages, minlength=sizes)
    counts = np.bincount(arrays.author_codes, minlength=sizes)
    averages = np.divide(totals, counts, out=np.zeros(sizes), where=counts > 0)
    return {
        author: float(averages[code])
        for code, author in enumerate(arrays.authors)
        if counts[code] > 0
    }


def longest_book_numpy(arrays: BookArrays) -> int:
    """Індекс першої книги з максимальною кількістю сторінок."""
    return int(np.argmax(arrays.pages))


def pages_statistics_numpy(values) -> dict[str, float]:
    array = np.asarray(values, dtype=np.float64)
    return {
        "average": float(array.mean()),
        "minimum": float(array.min()),
        "maximum": float(array.max()),
        "std": float(array.std()),
    }


# --------------------------------------------------------------------------
# Складений звіт (використовується для cProfile)
# --------------------------------------------------------------------------
def catalog_report_python(
    books: list[Book], iterations: int = DEFAULT_SCORE_ITERATIONS
) -> dict[str, object]:
    pages = [book.pages for book in books]
    scores = calculate_scores_sequential(pages, iterations)
    return {
        "statistics": pages_statistics_python(pages),
        "longest": longest_book_python(books),
        "by_author": group_by_author_python(books),
        "found_by_author": len(search_by_author_python(books, books[0].author)),
        "found_by_year": len(filter_by_year_python(books, 1990, 2010)),
        "mean_score": sum(scores) / len(scores),
    }
