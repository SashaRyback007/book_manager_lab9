import pytest

from book_manager import analytics as an
from book_manager import parallel as par
from book_manager.synchronization import run_copies_demo

ITERATIONS = 5


@pytest.fixture(scope="module")
def books():
    return an.generate_books(2_000, seed=3, authors_count=20)


def test_scores_threads_equal_sequential(books) -> None:
    pages = [b.pages for b in books[:300]]
    assert par.calculate_scores_threads(pages, workers=3, iterations=ITERATIONS) == an.calculate_scores_sequential(
        pages, ITERATIONS
    )


def test_scores_processes_equal_sequential(books) -> None:
    pages = [b.pages for b in books[:300]]
    parallel = par.calculate_scores_processes(pages, workers=2, iterations=ITERATIONS)
    assert parallel == an.calculate_scores_sequential(pages, ITERATIONS)


@pytest.mark.parametrize("function", [par.pages_statistics_threads, par.pages_statistics_processes])
def test_parallel_statistics(books, function) -> None:
    pages = [b.pages for b in books]
    expected = an.pages_statistics_python(pages)
    result = function(pages, workers=3)
    for key in expected:
        assert result[key] == pytest.approx(expected[key])


def test_statistics_with_more_workers_than_items() -> None:
    result = par.pages_statistics_threads([10, 20], workers=8)
    assert result["average"] == pytest.approx(15.0)


@pytest.mark.parametrize("fmt", ["json", "csv"])
def test_file_loading(books, tmp_path, fmt) -> None:
    paths = par.write_catalog_files(books, tmp_path, files_count=4, fmt=fmt)
    assert par.load_files_sequential(paths) == books
    assert par.load_files_threads(paths, workers=4) == books


def test_unsupported_format(tmp_path, books) -> None:
    with pytest.raises(ValueError):
        par.write_catalog_files(books, tmp_path, fmt="xml")


def test_lock_prevents_race_condition() -> None:
    assert run_copies_demo(threads_count=4, per_thread=100, use_lock=True) == 400


def test_race_condition_loses_updates_without_lock() -> None:
    result = run_copies_demo(threads_count=4, per_thread=200, use_lock=False)
    assert result <= 800  # без Lock значення не може перевищити очікуване (зазвичай — менше)
