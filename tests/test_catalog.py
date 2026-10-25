import pytest

from book_manager import Book, BookCatalog


@pytest.fixture
def catalog() -> BookCatalog:
    return BookCatalog(
        [
            Book("A", "Franko", 1900, 300),
            Book("B", "Franko", 1910, 500),
            Book("C", "Lesya", 1907, 200),
            Book("D", "Lesya", 2001, 700),
        ]
    )


def test_book_validation() -> None:
    with pytest.raises(ValueError):
        Book("", "Franko", 1900, 100)
    with pytest.raises(ValueError):
        Book("A", "Franko", 1900, 0)


def test_basic_features(catalog: BookCatalog) -> None:
    assert [b.title for b in catalog.search_by_author("Franko")] == ["A", "B"]
    assert [b.title for b in catalog.filter_by_year(1905, 1915)] == ["B", "C"]
    assert catalog.longest_book().title == "D"
    assert catalog.average_pages() == pytest.approx(425.0)


def test_empty_catalog_errors() -> None:
    empty = BookCatalog()
    with pytest.raises(ValueError):
        empty.longest_book()
    with pytest.raises(ValueError):
        empty.average_pages()


def test_author_statistics_is_cached(catalog: BookCatalog) -> None:
    first = catalog.author_statistics("Franko")
    second = catalog.author_statistics("Franko")
    info = catalog.cache_info()
    assert first == second
    assert (info.hits, info.misses) == (1, 1)
    assert first.books_count == 2
    assert first.average_pages == pytest.approx(400.0)


def test_cache_invalidation_after_add(catalog: BookCatalog) -> None:
    before = catalog.author_statistics("Franko")
    catalog.add_book(Book("E", "Franko", 1920, 1000))
    after = catalog.author_statistics("Franko")
    assert before.books_count == 2
    assert after.books_count == 3
    assert after.average_pages == pytest.approx(600.0)
    assert catalog.cache_info().misses == 2  # другий розрахунок, а не кеш


def test_cache_invalidation_after_update(catalog: BookCatalog) -> None:
    catalog.author_statistics("Lesya")
    catalog.update_pages(2, 1100)
    assert catalog.author_statistics("Lesya").max_pages == 1100


def test_unknown_author(catalog: BookCatalog) -> None:
    stats = catalog.author_statistics("Nobody")
    assert stats.books_count == 0 and stats.first_year is None
