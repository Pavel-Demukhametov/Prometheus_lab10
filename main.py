import os
import logging
from dotenv import load_dotenv
from prometheus_client import start_http_server, Gauge
import psutil

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем значения переменных окружения
exporter_host = os.getenv("EXPORTER_HOST", "0.0.0.0")
exporter_port = int(os.getenv("EXPORTER_PORT", 8000))

# Логируем загрузку переменных окружения
logger.info(f"Экспортер запускается на {exporter_host}:{exporter_port}")

# Создаем метрики для Prometheus
cpu_usage = Gauge('cpu_usage_percent', 'Процент использования процессора')
memory_total = Gauge('memory_total_bytes', 'Общий объем оперативной памяти')
memory_used = Gauge('memory_used_bytes', 'Используемая оперативная память')
disk_total = Gauge('disk_total_bytes', 'Общий объем дисков')
disk_used = Gauge('disk_used_bytes', 'Используемый объем дисков')

# Функция для сбора метрик
def collect_metrics():
    try:
        # Процессор
        cpu_usage.set(psutil.cpu_percent())
        
        # Память
        memory_info = psutil.virtual_memory()
        memory_total.set(memory_info.total)
        memory_used.set(memory_info.used)
        
        # Диски
        disk_info = psutil.disk_usage('/')
        disk_total.set(disk_info.total)
        disk_used.set(disk_info.used)

        logger.info("Метрики успешно обновлены")
    except Exception as e:
        logger.error(f"Ошибка при сборе метрик: {e}")

# Главная функция
def main():
    try:
        # Запускаем HTTP-сервер для Prometheus
        logger.info(f"Запуск сервера на {exporter_host}:{exporter_port}")
        start_http_server(exporter_port, addr=exporter_host)
        
        # Периодическое обновление метрик
        logger.info("Сбор метрик начат")
        while True:
            collect_metrics()
    except Exception as e:
        logger.error(f"Ошибка при запуске экспортера: {e}")

if __name__ == "__main__":
    main()
