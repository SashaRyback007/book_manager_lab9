"""Модель предметної області: книга (назва, автор, рік, кількість сторінок)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Book:
    """Незмінна книга. Зміна даних виконується через dataclasses.replace."""

    title: str
    author: str
    year: int
    pages: int

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Назва книги не може бути порожньою")
        if not self.author.strip():
            raise ValueError("Автор не може бути порожнім")
        if self.year <= 0:
            raise ValueError("Рік видання має бути додатним")
        if self.pages <= 0:
            raise ValueError("Кількість сторінок має бути додатною")
