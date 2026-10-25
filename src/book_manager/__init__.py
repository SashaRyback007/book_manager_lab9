"""Book manager: система обліку книг (варіант 2), ЛР №9."""

from book_manager.catalog import AuthorStats, BookCatalog
from book_manager.models import Book

__all__ = ["Book", "BookCatalog", "AuthorStats"]
__version__ = "0.9.0"
