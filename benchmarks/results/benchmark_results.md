# Результати benchmark


## pages_statistics — 2 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00080 | 0.00080 | 0.00 | 1.00× | так |
| NumPy (list->array) | – | 0.00029 | 0.00029 | 0.03 | 2.79× | так |
| NumPy (готовий array) | – | 0.00007 | 0.00007 | 0.03 | 11.00× | так |
| ThreadPoolExecutor | 1 | 0.00288 | 0.00288 | 0.01 | 0.28× | так |
| ProcessPoolExecutor | 1 | 0.34025 | 0.34025 | 0.04 | 0.00× | так |
| ThreadPoolExecutor | 2 | 0.00192 | 0.00192 | 0.01 | 0.42× | так |
| ProcessPoolExecutor | 2 | 0.34126 | 0.34126 | 0.04 | 0.00× | так |

## scores — 2 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Sequential | 1 | 0.01350 | 0.01350 | 0.04 | 1.00× | так |
| ThreadPoolExecutor | 1 | 0.03516 | 0.03516 | 1.57 | 0.38× | так |
| ThreadPoolExecutor | 2 | 0.03427 | 0.03427 | 1.58 | 0.39× | так |
| ProcessPoolExecutor | 1 | 0.24940 | 0.24940 | 0.06 | 0.05× | так |
| ProcessPoolExecutor | 2 | 0.41893 | 0.41893 | 0.06 | 0.03× | так |
| NumPy vectorized | – | 0.00121 | 0.00121 | 0.06 | 11.13× | так |

## search_by_author — 2 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00012 | 0.00012 | 0.00 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00006 | 0.00006 | 0.00 | 1.91× | так |

## filter_by_year — 2 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00021 | 0.00021 | 0.00 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00006 | 0.00006 | 0.01 | 3.53× | так |

## group_by_author — 2 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00090 | 0.00090 | 0.07 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00140 | 0.00140 | 0.05 | 0.64× | так |

## longest_book — 2 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00012 | 0.00012 | 0.00 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00006 | 0.00006 | 0.00 | 1.94× | так |

## author_cache — 2 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Без кешу (cold) | – | 0.00006 | 0.00006 | – | 1.00× | так |
| lru_cache (warm) | – | 0.00000 | 0.00000 | – | 68.75× | так |

## pages_statistics — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00249 | 0.00249 | 0.00 | 1.00× | так |
| NumPy (list->array) | – | 0.00080 | 0.00080 | 0.15 | 3.11× | так |
| NumPy (готовий array) | – | 0.00026 | 0.00026 | 0.15 | 9.75× | так |
| ThreadPoolExecutor | 1 | 0.00463 | 0.00463 | 0.04 | 0.54× | так |
| ProcessPoolExecutor | 1 | 0.30925 | 0.30925 | 0.11 | 0.01× | так |
| ThreadPoolExecutor | 2 | 0.00320 | 0.00320 | 0.04 | 0.78× | так |
| ProcessPoolExecutor | 2 | 0.28114 | 0.28114 | 0.08 | 0.01× | так |

## scores — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Sequential | 1 | 0.05225 | 0.05225 | 0.19 | 1.00× | так |
| ThreadPoolExecutor | 1 | 0.16828 | 0.16828 | 7.89 | 0.31× | так |
| ThreadPoolExecutor | 2 | 0.20375 | 0.20375 | 7.91 | 0.26× | так |
| ProcessPoolExecutor | 1 | 0.30408 | 0.30408 | 0.41 | 0.17× | так |
| ProcessPoolExecutor | 2 | 0.30951 | 0.30951 | 0.33 | 0.17× | так |
| NumPy vectorized | – | 0.00432 | 0.00432 | 0.31 | 12.09× | так |

## search_by_author — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00045 | 0.00045 | 0.00 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00007 | 0.00007 | 0.01 | 6.24× | так |

## filter_by_year — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00049 | 0.00049 | 0.01 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00006 | 0.00006 | 0.03 | 7.72× | так |

## group_by_author — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00270 | 0.00270 | 0.07 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00047 | 0.00047 | 0.08 | 5.75× | так |

## longest_book — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Python loops | 1 | 0.00037 | 0.00037 | 0.00 | 1.00× | так |
| NumPy (готові arrays) | – | 0.00002 | 0.00002 | 0.00 | 21.11× | так |

## author_cache — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Без кешу (cold) | – | 0.00037 | 0.00040 | – | 1.00× | так |
| lru_cache (warm) | – | 0.00000 | 0.00000 | – | 480.42× | так |

## io_json_latency_0ms — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Sequential I/O | 1 | 0.02326 | 0.02326 | 1.44 | 1.00× | так |
| ThreadPoolExecutor | 1 | 0.02663 | 0.02663 | 1.45 | 0.87× | так |
| ThreadPoolExecutor | 2 | 0.02509 | 0.02509 | 1.65 | 0.93× | так |

## io_json_latency_50ms — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Sequential I/O | 1 | 0.44519 | 0.44519 | 1.44 | 1.00× | так |
| ThreadPoolExecutor | 1 | 0.43515 | 0.43515 | 1.45 | 1.02× | так |
| ThreadPoolExecutor | 2 | 0.22678 | 0.22678 | 1.45 | 1.96× | так |

## io_csv_latency_0ms — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Sequential I/O | 1 | 0.03738 | 0.03738 | 1.33 | 1.00× | так |
| ThreadPoolExecutor | 1 | 0.03453 | 0.03453 | 1.34 | 1.08× | так |
| ThreadPoolExecutor | 2 | 0.04045 | 0.04045 | 1.34 | 0.92× | так |

## io_csv_latency_50ms — 10 000 книг

| Метод | Workers | Mean, s | Median, s | Peak memory, MB | Speedup | Коректно |
|---|---|---|---|---|---|---|
| Sequential I/O | 1 | 0.45427 | 0.45427 | 1.33 | 1.00× | так |
| ThreadPoolExecutor | 1 | 0.45167 | 0.45167 | 1.34 | 1.01× | так |
| ThreadPoolExecutor | 2 | 0.23411 | 0.23411 | 1.34 | 1.94× | так |
