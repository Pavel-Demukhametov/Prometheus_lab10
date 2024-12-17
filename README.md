# Prometheus Exporter

## Оглавление
1. [Описание](#описание)
2. [Стек технологий](#стек-технологий)
3. [Установка и запуск проекта](#установка-и-запуск-проекта)
4. [Конфигурация](#конфигурация)
5. [Настройка Prometheus](#настройка-prometheus)
6. [Maintainers](#maintainers)

## Описание

Проект представляет собой **экспортёр для Prometheus**, разработанный на Python, который собирает и экспортирует метрики использования процессора (CPU), оперативной памяти (RAM) и дискового пространства. Экспортёр предоставляет эти метрики в формате, совместимом с Prometheus, для последующего мониторинга и анализа.

**Особенности проекта**:
- **Сбор метрик CPU**: Процентное использование каждого ядра процессора.
- **Сбор метрик памяти**: Общий объём, использованная и свободная оперативная память.
- **Сбор метрик дискового пространства**: Общий объём, использованное и свободное дисковое пространство.
- **Настраиваемый интерфейс**: Возможность настройки хоста и порта через переменные окружения.
- **Простота использования**: Лёгкий запуск и интеграция с Prometheus.

## Стек технологий
- **Python 3**
- `prometheus_client` — для создания и экспорта метрик Prometheus.
- `psutil` — для сбора системных метрик.
- `python-dotenv` — для управления переменными окружения.

## Запуск проекта

1. Клонирование репозитория

    ```
    git clone <ссылка на репозиторий>
    ```

2. Переход в папку с репозиторием

    ```
    cd <название папки в которую клонировали репозиторий>
    ```

3. Создание виртуального окружения

    Для Windows:
    ```
    python -m venv venv
    ```

    Для Linux:
    ```
    python3 -m venv venv
    ```

4. Активация виртуального окружения

    Для Windows:
    ```
    .\venv\Scripts\activate
    ```

    Для Linux:
    ```
    source venv/bin/activate
    ```

5. Установка зависимостей

    ```
    pip install -r requirements.txt
    ```

6. Установка переменных окружения. Файл `.env`

    **Переменные окружения**:
        - `EXPORTER_HOST`: Хост, на котором будет запущен экспортёр 
        - `EXPORTER_PORT`: Порт для HTTP-сервера метрик

    Пример `.env` файла:
    ```
    EXPORTER_HOST=127.0.0.1
    EXPORTER_PORT=8000
    ```


### 6. Запуск экспортёра

Запустите экспортёр с помощью Python:

```bash
python main.py
```

**Пример вывода:**

```
Экспортер запускается на http://0.0.0.0:8080/metrics
```

Теперь экспортёр доступен по адресу [http://localhost:8080/metrics](http://localhost:8080/metrics)

## Метрики
```
    cpu_usage_percent — процентное использование процессора для каждого ядра
    memory_total_bytes — общий объём оперативной памяти (в байтах).
    memory_used_bytes — объём используемой оперативной памяти (в байтах).
    disk_total_bytes — общий объём доступного дискового пространства (в байтах).
    disk_used_bytes — объём используемого дискового пространства (в байтах).
```

## Настройка Prometheus

Чтобы Prometheus начал собирать метрики из вашего экспортёра, необходимо добавить соответствующую конфигурацию в файл `prometheus.yml`.

### 1. Открытие файла конфигурации Prometheus

Откройте файл `prometheus.yml` в текстовом редакторе.

### 2. Добавление нового задания (job) для вашего экспортёра

Добавьте следующий блок в секцию `scrape_configs`:

```yaml
  - job_name: "exporter"
    static_configs:
      - targets: ["localhost:8080"]
```
Перезапустите Prometheus, чтобы применить изменения.

### 3. Перезапуск Prometheus

После внесения изменений в конфигурационный файл перезапустите Prometheus

### 4. Проверка целевых заданий (targets)

Перейдите в веб-интерфейс Prometheus по адресу [http://localhost:9090/targets](http://localhost:9090/targets) и убедитесь, что задание `prometheus_exporter` отображается как `UP`.

## Примеры PromQL-запросов

Ниже приведены примеры PromQL-запросов для анализа собранных метрик.

### 1. Использование процессора

#### 1.1. Среднее использование CPU по каждому ядру

```promql
avg(cpu_usage_percent) by (core)
```

#### 1.2. Максимальное использование CPU на ядро

```promql
max(cpu_usage_percent) by (core)
```

### 2. Использование оперативной памяти

#### 2.1. Общая оперативная память (в Гигабайтах)

```promql
memory_total_bytes / 1024 / 1024 / 1024
```

#### 2.2. Используемая оперативная память (в Гигабайтах)

```promql
memory_used_bytes / 1024 / 1024 / 1024
```

#### 2.3. Процент использования оперативной памяти превышающее 80%

```promql
(memory_used_bytes / memory_total_bytes) * 100 > 80
```

### 3. Использование дискового пространства

#### 3.1. Общий объём диска (в Гигабайтах)

```promql
disk_total_bytes / 1024 / 1024 / 1024
```

#### 3.2. Используемый объём диска (в Гигабайтах)

```promql
disk_used_bytes / 1024 / 1024 / 1024
```

#### 3.3. Процент использования диска

```promql
(disk_used_bytes / disk_total_bytes) * 100
```

#### 3.3. Процент использования диска

```promql
(disk_used_bytes / disk_total_bytes) * 100
```

#### 3.4. Максимальное значение занятого пространства на диске в байтах за последние 15 минут
```promql
max_over_time(disk_used_bytes[15m])
```

## Maintainers

- Developed by [Pavel Demukhametov](https://github.com/Pavel-Demukhametov)
