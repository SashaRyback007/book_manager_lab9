from book_manager import analytics as an
from book_manager.profiling import measure_memory, profile_callable, top_allocations


def test_profile_finds_bottleneck() -> None:
    books = an.generate_books(500)
    result = profile_callable(an.catalog_report_python, books, iterations=10)
    assert result.bottleneck in {"calculate_scores_sequential", "book_score"}
    assert 0 < result.bottleneck_share <= 100
    assert "ncalls" in result.text


def test_memory_measurement() -> None:
    current, peak = measure_memory(an.generate_books, 1_000)
    assert peak > 0 and peak >= current
    assert top_allocations(an.generate_books, 1_000, limit=3)
