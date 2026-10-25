# Book Manager — система обліку книг (варіант 2)

Лабораторна робота №9 — **паралельність, багатопроцесність та оптимізація**.
Проєкт продовжує варіант 2 (облік книг): книга має назву, автора, рік видання та кількість сторінок.

## Що реалізовано

| Вимога лабораторної | Де |
|---|---|
| Базові можливості (додавання, пошук за автором, фільтр за роком, найбільша книга, середня к-сть сторінок) | `src/book_manager/catalog.py` |
| Генерація каталогу 10 000 – 300 000 книг | `analytics.generate_books` |
| Baseline (Python loops) | `analytics.py` (`*_python`) |
| NumPy-векторизація | `analytics.py` (`*_numpy`, `BookArrays`) |
| threading / `ThreadPoolExecutor` | `parallel.py`, `synchronization.py` |
| multiprocessing / `ProcessPoolExecutor` | `parallel.py` |
| Synchronization (`Lock`), race condition | `synchronization.py` |
| I/O-bound: паралельне читання JSON/CSV | `parallel.load_files_*` |
| `cProfile` + `tracemalloc` + визначення bottleneck | `profiling.py` |
| Caching + invalidation | `BookCatalog.author_statistics` (`lru_cache` + `version`) |
| Benchmark, повтори, speedup, CSV/MD/графіки | `benchmarks/` |
| Перевірка правильності та тести | `tests/` |

## Структура

```
book_manager/
├── pyproject.toml
├── requirements.txt
├── README.md
├── src/book_manager/
│   ├── models.py            # Book
│   ├── catalog.py           # BookCatalog + кешована статистика автора
│   ├── analytics.py         # baseline (Python) та NumPy
│   ├── parallel.py          # ThreadPool / ProcessPool / I/O
│   ├── synchronization.py   # race condition + Lock
│   └── profiling.py         # cProfile, tracemalloc
├── tests/
└── benchmarks/
    ├── benchmark.py         # фреймворк (повтори, speedup, CSV)
    ├── plots.py             # графіки
    ├── run_benchmarks.py    # запуск усіх експериментів
    └── results/             # CSV / MD / PNG / profile_report.txt
```

## Встановлення

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate      Linux/macOS:  source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Запуск

```bash
# тести
pytest

# профілювання (cProfile + tracemalloc) -> benchmarks/results/profile_report.txt
python -m book_manager.profiling --size 50000

# швидка перевірка бенчмарків (кілька секунд)
python benchmarks/run_benchmarks.py --quick

# повний бенчмарк: 10 000 / 100 000 / 300 000 книг, workers 1-2-4-8, 5 повторів
python benchmarks/run_benchmarks.py
```

Корисні параметри: `--sizes 10000 100000 300000`, `--workers 1 2 4 8`, `--repeats 5`,
`--iterations 30` (вага CPU-bound операції), `--latency 0.05` (імітація повільного I/O).

Результати: `benchmarks/results/benchmark_results.csv`, `benchmark_results.md`, графіки `*.png`.

> ⚠️ Числа залежать від CPU, ОС, версії Python та кількості workers. У звіт слід вносити
> **власні виміряні** результати після запуску на своєму комп'ютері.

## Експерименти

1. **pages_statistics** — average/min/max/std: Python loops, NumPy, ThreadPool, ProcessPool.
2. **scores** — важка CPU-bound операція («рейтинговий індекс» книги): Sequential, ThreadPool, ProcessPool, NumPy.
3. **search_by_author**, **filter_by_year**, **group_by_author**, **longest_book**: Python loops vs NumPy.
4. **author_cache** — холодний виклик vs `lru_cache`.
5. **io_*** — читання 8 JSON/CSV-файлів: Sequential vs ThreadPoolExecutor, з імітацією затримки та без.

Кожна реалізація автоматично порівнюється з baseline; при розбіжності запуск завершується помилкою.

## Нотатки до аналізу

* **NumPy (list→array) vs NumPy (готовий array)** — перетворення списку в масив коштує часу;
  виграш повністю проявляється, коли дані зберігаються колонково (`BookArrays`).
* **ProcessPoolExecutor** створює пул при кожному виклику, тож у вимірювання входять запуск процесів
  та серіалізація — для малих наборів він може бути повільнішим за baseline.
* **ThreadPoolExecutor** для CPU-bound коду не прискорює через GIL; для I/O-bound — прискорює,
  коли є реальне очікування (див. `latency`).
* **Cache invalidation**: кожна зміна каталогу збільшує `version`, що входить до ключа `lru_cache`.
* Пам'ять вимірюється `tracemalloc` лише для основного процесу (дочірні процеси не враховуються).

## Таблиця результатів (заповнити після запуску)

| Experiment | Data size | Workers | Mean time, s | Peak memory, MB | Speedup |
|---|---|---|---|---|---|
| Baseline | 100000 | 1 | … | … | 1.00 |
| Threads | 100000 | 4 | … | … | … |
| Processes | 100000 | 4 | … | … | … |
| NumPy | 100000 | – | … | … | … |
| Cached repeated call | – | – | … | … | … |

## Git-коміти

```bash
git add src/book_manager/analytics.py benchmarks/benchmark.py
git commit -m "Add project performance benchmarks"
git add src/book_manager/profiling.py
git commit -m "Profile application bottlenecks"
git add src/book_manager/parallel.py src/book_manager/synchronization.py
git commit -m "Add threaded processing experiment"
git commit --allow-empty -m "Add multiprocessing optimization"
git commit --allow-empty -m "Add NumPy vectorized implementation"
git add tests README.md
git commit -m "Add caching and performance tests"
```
