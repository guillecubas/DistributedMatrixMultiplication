import psutil
import csv

def log_metrics(matrix_size, exec_time, nodes_used, csv_file):
    memory_used = psutil.Process().memory_info().rss / (1024 * 1024)  # in MB
    cpu_usage = psutil.cpu_percent(interval=1)
    transfer_time = "N/A"  # optional to extend later

    with open(csv_file, mode="a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            matrix_size,
            round(exec_time * 1000),
            round(memory_used),
            cpu_usage,
            nodes_used,
            transfer_time
        ])
