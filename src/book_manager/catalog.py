"""Каталог книг: базові можливості + кешована статистика автора.

Cache invalidation: кожна зміна каталогу збільшує ``version``. Версія входить
до ключа ``lru_cache``, тому застарілий результат повторно не використовується.
Додатково ``clear_cache()`` звільняє пам'ять від старих записів.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, replace
from functools import lru_cache

from book_manager.models import Book


@dataclass(frozen=True, slots=True)
class AuthorStats:
    author: str
    books_count: int
    average_pages: float
    max_pages: int
    first_year: int | None
    last_year: int | None


class BookCatalog:
    def __init__(self, books: Iterable[Book] | None = None) -> None:
        self._books: list[Book] = list(books) if books is not None else []
        self._version = 0
        # lru_cache на рівні екземпляра: ``self`` не потрапляє до ключа кешу.
        self._cached_author_stats = lru_cache(maxsize=256)(self._compute_author_stats)

    # ---- службові властивості -------------------------------------------
    def __len__(self) -> int:
        return len(self._books)

    @property
    def books(self) -> Sequence[Book]:
        """Лише для читання (повертається сам список без копіювання)."""
        return self._books

    @property
    def version(self) -> int:
        return self._version

    # ---- базові можливості (Lab_01) ---------------------------------------
    def add_book(self, book: Book) -> None:
        self._books.append(book)
        self._invalidate()

    def add_books(self, books: Iterable[Book]) -> None:
        self._books.extend(books)
        self._invalidate()

    def update_pages(self, index: int, pages: int) -> None:
        self._books[index] = replace(self._books[index], pages=pages)
        self._invalidate()

    def search_by_author(self, author: str) -> list[Book]:
        return [book for book in self._books if book.author == author]

    def filter_by_year(self, start: int, end: int) -> list[Book]:
        return [book for book in self._books if start <= book.year <= end]

    def longest_book(self) -> Book:
        if not self._books:
            raise ValueError("Каталог порожній")
        return max(self._books, key=lambda book: book.pages)

    def average_pages(self) -> float:
        if not self._books:
            raise ValueError("Каталог порожній")
        return sum(book.pages for book in self._books) / len(self._books)

    # ---- caching ----------------------------------------------------------
    def author_statistics(self, author: str) -> AuthorStats:
        """Повторна статистика автора: перший виклик рахує, наступні беруться з кешу."""
        return self._cached_author_stats(author, self._version)

    def cache_info(self):
        return self._cached_author_stats.cache_info()

    def clear_cache(self) -> None:
        self._cached_author_stats.cache_clear()

    def _invalidate(self) -> None:
        self._version += 1

    def _compute_author_stats(self, author: str, version: int) -> AuthorStats:
        del version  # лише частина ключа кешу
        found = [book for book in self._books if book.author == author]
        if not found:
            return AuthorStats(author, 0, 0.0, 0, None, None)
        return AuthorStats(
            author=author,
            books_count=len(found),
            average_pages=sum(book.pages for book in found) / len(found),
            max_pages=max(book.pages for book in found),
            first_year=min(book.year for book in found),
            last_year=max(book.year for book in found),
        )
