"""Race condition та її виправлення через Lock.

Приклад: кілька потоків одночасно збільшують кількість примірників книги на складі.
Щоб гонка відтворювалась стабільно, між читанням і записом викликається
``time.sleep(0)`` — це віддає керування іншому потоку (як і в реальному коді,
де між read та write може відбутися перемикання).
"""

from __future__ import annotations

import time
from threading import Lock, Thread


class CopiesCounter:
    """Кількість примірників книги у спільній пам'яті."""

    def __init__(self) -> None:
        self.value = 0
        self._lock = Lock()

    def add_unsafe(self) -> None:
        current = self.value  # read
        time.sleep(0)  # перемикання потоків між read та write
        self.value = current + 1  # write

    def add_safe(self) -> None:
        with self._lock:  # критична секція — максимально коротка
            current = self.value
            time.sleep(0)
            self.value = current + 1


def run_copies_demo(threads_count: int = 8, per_thread: int = 500, use_lock: bool = False) -> int:
    """Повертає фінальне значення; очікується threads_count * per_thread."""
    counter = CopiesCounter()
    method = counter.add_safe if use_lock else counter.add_unsafe

    def worker() -> None:
        for _ in range(per_thread):
            method()

    threads = [Thread(target=worker) for _ in range(threads_count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return counter.value
