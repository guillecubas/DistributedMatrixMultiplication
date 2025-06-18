import time
import psutil
import os
import csv
from pyspark import SparkContext

# Setup
sc = SparkContext("local[*]", "DistributedMatrixMultiplication")

def run_benchmark(matrix_size):
    # Simulate generating matrices A and B
    A = [(i, k, 1) for i in range(matrix_size) for k in range(matrix_size)]
    B = [(k, j, 1) for k in range(matrix_size) for j in range(matrix_size)]

    rddA = sc.parallelize(A)
    rddB = sc.parallelize(B)

    start_transfer = time.time()
    # MapReduce step
    mappedA = rddA.map(lambda x: (x[1], (x[0], x[2])))
    mappedB = rddB.map(lambda x: (x[0], (x[1], x[2])))
    joined = mappedA.join(mappedB)
    transfer_time = (time.time() - start_transfer) * 1000

    start = time.time()
    product = joined.map(lambda x: ((x[1][0][0], x[1][1][0]), x[1][0][1] * x[1][1][1]))
    result = product.reduceByKey(lambda x, y: x + y)
    result.count()  # Trigger the computation
    end = time.time()

    # Metrics
    execution_time = (end - start) * 1000  # in ms
    memory_used = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # in MB
    cpu_usage = psutil.cpu_percent(interval=1)  # during sleep window
    nodes_used = 1  # you can change this dynamically in a real cluster

    return {
        "Matrix Size": matrix_size,
        "Execution Time (ms)": round(execution_time),
        "Memory Used (MB)": round(memory_used),
        "CPU Usage (%)": cpu_usage,
        "Nodes Used": nodes_used,
        "Transfer Time (ms)": round(transfer_time)
    }

# Sizes to test
sizes = [256, 512, 1024]
results = []

for size in sizes:
    result = run_benchmark(size)
    results.append(result)

# Write CSV
with open("matrix_benchmark.csv", mode="w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Benchmark results written to matrix_benchmark.csv")
