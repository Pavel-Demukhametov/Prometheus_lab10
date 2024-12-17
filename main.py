import os
import time
from prometheus_client import start_http_server, Gauge
import psutil
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('EXPORTER_HOST', '0.0.0.0')
PORT = int(os.getenv('EXPORTER_PORT', 8080))

print(f"Экспортер запускается на http://{HOST}:{PORT}/metrics")

cpu_usage = Gauge('cpu_usage_percent', 'Процент использования CPU', ['core'])
memory_total = Gauge('memory_total_bytes', 'Общий объём оперативной памяти')
memory_used = Gauge('memory_used_bytes', 'Используемая оперативная память')

disk_total = Gauge('disk_total_bytes', 'Общий объём дискового пространства')
disk_used = Gauge('disk_used_bytes', 'Используемое дисковое пространство')


def collect_metrics():
    cpu_percentages = psutil.cpu_percent(interval=1, percpu=True)
    for i, percentage in enumerate(cpu_percentages):
        core_label = f'core_{i}'
        cpu_usage.labels(core=core_label).set(percentage)

    memory = psutil.virtual_memory()
    memory_total.set(memory.total)
    memory_used.set(memory.used)

    disk = psutil.disk_usage('/')
    disk_total.set(disk.total)
    disk_used.set(disk.used)


start_http_server(PORT, addr=HOST)
while True:
    collect_metrics()
