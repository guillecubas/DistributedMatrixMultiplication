import csv
import psutil
import os
from time import time

def log_metrics(matrix_size, exec_time, nodes_used, csv_file, method, transfer_time=None):
    # Obtener memoria usada (en MB)
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info().rss / (1024 * 1024)  # Resident Set Size in MB

    # Obtener uso de CPU en porcentaje (tiempo medio en 1 segundo)
    cpu_usage = psutil.cpu_percent(interval=1)

    # Escribir en el CSV
    with open(csv_file, mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            method,
            matrix_size,
            round(exec_time * 1000, 2),  # ms
            round(memory_info, 2),
            round(cpu_usage, 2),
            nodes_used,
            round(transfer_time * 1000, 2) if transfer_time is not None else "-"
        ])
