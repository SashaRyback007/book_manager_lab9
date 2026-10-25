# Результати benchmark


## pages_statistics — 2 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00080 | 0.00080 | 0.00 | 1.00× | так |
| NumPy (list->array) | – | 0.00034 | 0.00034 | 0.03 | 2.33× | так |
| NumPy (готовий array) | – | 0.00012 | 0.00012 | 0.03 | 6.78× | так |
| ThreadPoolExecutor | 1 | 0.00258 | 0.00258 | 0.01 | 0.31× | так |
| ProcessPoolExecutor | 1 | 0.42603 | 0.42603 | 0.04 | 0.00× | так |
| ThreadPoolExecutor | 2 | 0.00177 | 0.00177 | 0.01 | 0.45× | так |
| ProcessPoolExecutor | 2 | 0.39991 | 0.39991 | 0.05 | 0.00× | так |

## scores — 2 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Sequential | 1 | 0.01040 | 0.01040 | 0.04 | 1.00× | так |
| ThreadPoolExecutor | 1 | 0.04323 | 0.04323 | 1.62 | 0.24× | так |
| ThreadPoolExecutor | 2 | 0.03280 | 0.03280 | 1.60 | 0.32× | так |
| ProcessPoolExecutor | 1 | 0.24237 | 0.24237 | 0.06 | 0.04× | так |
| ProcessPoolExecutor | 2 | 0.29121 | 0.29121 | 0.06 | 0.04× | так |
| NumPy vectorized | – | 0.00100 | 0.00100 | 0.06 | 10.45× | так |

## search_by_author — 2 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00006 | 0.00006 | 0.00 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00005 | 0.00005 | 0.00 | 1.19× | так |

## filter_by_year — 2 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00010 | 0.00010 | 0.00 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00003 | 0.00003 | 0.01 | 3.24× | так |

## group_by_author — 2 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00102 | 0.00102 | 0.07 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00065 | 0.00065 | 0.05 | 1.55× | так |

## longest_book — 2 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00009 | 0.00009 | 0.00 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00002 | 0.00002 | 0.00 | 3.85× | так |

## author_cache — 2 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Без кешу (cold) | – | 0.00006 | 0.00005 | – | 1.00× | так |
| lru_cache (warm) | – | 0.00000 | 0.00000 | – | 60.09× | так |

## pages_statistics — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00224 | 0.00224 | 0.00 | 1.00× | так |
| NumPy (list->array) | – | 0.00081 | 0.00081 | 0.15 | 2.76× | так |
| NumPy (готовий array) | – | 0.00008 | 0.00008 | 0.15 | 28.42× | так |
| ThreadPoolExecutor | 1 | 0.00346 | 0.00346 | 0.04 | 0.65× | так |
| ProcessPoolExecutor | 1 | 0.25490 | 0.25490 | 0.11 | 0.01× | так |
| ThreadPoolExecutor | 2 | 0.00298 | 0.00298 | 0.04 | 0.75× | так |
| ProcessPoolExecutor | 2 | 0.26990 | 0.26990 | 0.10 | 0.01× | так |

## scores — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Sequential | 1 | 0.05256 | 0.05256 | 0.19 | 1.00× | так |
| ThreadPoolExecutor | 1 | 0.16223 | 0.16223 | 7.89 | 0.32× | так |
| ThreadPoolExecutor | 2 | 0.16294 | 0.16294 | 7.87 | 0.32× | так |
| ProcessPoolExecutor | 1 | 0.33835 | 0.33835 | 0.41 | 0.16× | так |
| ProcessPoolExecutor | 2 | 0.35490 | 0.35490 | 0.32 | 0.15× | так |
| NumPy vectorized | – | 0.00437 | 0.00437 | 0.31 | 12.01× | так |

## search_by_author — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00077 | 0.00077 | 0.00 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00028 | 0.00028 | 0.01 | 2.77× | так |

## filter_by_year — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00090 | 0.00090 | 0.01 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00006 | 0.00006 | 0.03 | 15.00× | так |

## group_by_author — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00222 | 0.00222 | 0.07 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00042 | 0.00042 | 0.08 | 5.28× | так |

## longest_book — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00032 | 0.00032 | 0.00 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00001 | 0.00001 | 0.00 | 22.14× | так |

## author_cache — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Без кешу (cold) | – | 0.00025 | 0.00025 | – | 1.00× | так |
| lru_cache (warm) | – | 0.00000 | 0.00000 | – | 294.30× | так |

## io_json_latency_0ms — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Sequential I/O | 1 | 0.02473 | 0.02473 | 1.44 | 1.00× | так |
| ThreadPoolExecutor | 1 | 0.02552 | 0.02552 | 1.45 | 0.97× | так |
| ThreadPoolExecutor | 2 | 0.02695 | 0.02695 | 1.45 | 0.92× | так |

## io_json_latency_50ms — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Sequential I/O | 1 | 0.44263 | 0.44263 | 1.44 | 1.00× | так |
| ThreadPoolExecutor | 1 | 0.44194 | 0.44194 | 1.45 | 1.00× | так |
| ThreadPoolExecutor | 2 | 0.22219 | 0.22219 | 1.45 | 1.99× | так |

## io_csv_latency_0ms — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Sequential I/O | 1 | 0.07304 | 0.07304 | 1.33 | 1.00× | так |
| ThreadPoolExecutor | 1 | 0.03417 | 0.03417 | 1.34 | 2.14× | так |
| ThreadPoolExecutor | 2 | 0.04002 | 0.04002 | 1.34 | 1.83× | так |

## io_csv_latency_50ms — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Sequential I/O | 1 | 0.45751 | 0.45751 | 1.33 | 1.00× | так |
| ThreadPoolExecutor | 1 | 0.44919 | 0.44919 | 1.34 | 1.02× | так |
| ThreadPoolExecutor | 2 | 0.23023 | 0.23023 | 1.34 | 1.99× | так |
