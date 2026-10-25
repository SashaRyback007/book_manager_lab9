import numpy as np
import pytest

from book_manager import analytics as an


@pytest.fixture(scope="module")
def books():
    return an.generate_books(5_000, seed=7, authors_count=50)


@pytest.fixture(scope="module")
def arrays(books):
    return an.BookArrays.from_books(books)


def index_of(book) -> int:
    return int(book.title.removeprefix("Book "))


def test_generate_is_deterministic() -> None:
    assert an.generate_books(100, seed=1) == an.generate_books(100, seed=1)
    assert an.generate_books(100, seed=1) != an.generate_books(100, seed=2)


def test_statistics_python_vs_numpy(books) -> None:
    pages = [b.pages for b in books]
    python = an.pages_statistics_python(pages)
    numpy_ = an.pages_statistics_numpy(pages)
    for key in python:
        assert numpy_[key] == pytest.approx(python[key])


def test_statistics_small_known_values() -> None:
    result = an.pages_statistics_python([100, 200, 300, 400])
    assert result == {"average": 250.0, "minimum": 100.0, "maximum": 400.0, "std": pytest.approx(111.80339887)}


def test_search_by_author(books, arrays) -> None:
    author = books[0].author
    expected = [index_of(b) for b in an.search_by_author_python(books, author)]
    assert an.search_by_author_numpy(arrays, author).tolist() == expected
    assert an.search_by_author_numpy(arrays, "Unknown").size == 0


def test_filter_by_year(books, arrays) -> None:
    expected = [index_of(b) for b in an.filter_by_year_python(books, 1990, 2010)]
    assert an.filter_by_year_numpy(arrays, 1990, 2010).tolist() == expected


def test_group_by_author(books, arrays) -> None:
    python = an.group_by_author_python(books)
    numpy_ = an.group_by_author_numpy(arrays)
    assert python.keys() == numpy_.keys()
    for author in python:
        assert numpy_[author] == pytest.approx(python[author])


def test_longest_book(books, arrays) -> None:
    assert index_of(an.longest_book_python(books)) == an.longest_book_numpy(arrays)


def test_scores_numpy_matches_sequential() -> None:
    pages = [50, 300, 777, 1200]
    sequential = an.calculate_scores_sequential(pages, iterations=10)
    vectorized = an.calculate_scores_numpy(pages, iterations=10)
    assert np.allclose(sequential, vectorized, rtol=1e-9)


def test_report_runs(books) -> None:
    report = an.catalog_report_python(books[:200], iterations=3)
    assert set(report) == {"statistics", "longest", "by_author", "found_by_author", "found_by_year", "mean_score"}
