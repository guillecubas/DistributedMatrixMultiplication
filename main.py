import hazelcast
from time import time
from matrix_utils import MatrixUtils
from matrix_multiplier import MatrixMultiplier
from metrics_logger import log_metrics
from distributed_tasks import remote_multiply_partition


def run_and_log(method_name, multiply_func, matrix_size, csv_file, **kwargs):
    matrix_a = MatrixUtils.generate_matrix(matrix_size)
    matrix_b = MatrixUtils.generate_matrix(matrix_size)

    start_time = time()
    result_matrix = multiply_func(matrix_a, matrix_b, matrix_size, **kwargs)
    end_time = time()

    if matrix_size <= 10:
        MatrixUtils.print_matrix(result_matrix)

    exec_time_ms = (end_time - start_time) * 1000

    print(f"[{method_name.upper()}] Matrix {matrix_size}x{matrix_size} completed in {exec_time_ms:.2f} ms")

    log_metrics(
        matrix_size=matrix_size,
        exec_time=exec_time_ms,
        nodes_used=kwargs.get("num_nodes", 1),
        csv_file=csv_file,
        method=method_name
    )


def run_hazelcast(matrix_size, csv_file, num_nodes):
    try:
        client = hazelcast.HazelcastClient(
            cluster_name="dev",
            cluster_members=["hazelcast1:5701", "hazelcast2:5701"]
        )
        print("✅ Cliente Hazelcast conectado correctamente.")
    except Exception as e:
        print("❌ Error al conectar con Hazelcast:", e)
        return

    matrix_a_map = client.get_map("matrixA").blocking()
    matrix_b_map = client.get_map("matrixB").blocking()
    result_matrix_map = client.get_map("resultMatrix").blocking()

    matrix_a = MatrixUtils.generate_matrix(matrix_size)
    matrix_b = MatrixUtils.generate_matrix(matrix_size)

    # Medir tiempo de transferencia
    transfer_start = time()
    matrix_a_map.put("A", matrix_a)
    matrix_b_map.put("B", matrix_b)
    transfer_end = time()
    transfer_time_ms = (transfer_end - transfer_start) * 1000

    # Multiplicación distribuida
    start_time = time()
    result_matrix = MatrixMultiplier.multiply(matrix_a, matrix_b, matrix_size, num_nodes, client=client)
    end_time = time()
    exec_time_ms = (end_time - start_time) * 1000

    result_matrix_map.put("C", result_matrix)

    if matrix_size <= 10:
        MatrixUtils.print_matrix(result_matrix)

    print(f"[HAZELCAST] Matrix {matrix_size}x{matrix_size} completed in {exec_time_ms:.2f} ms")

    log_metrics(
        matrix_size=matrix_size,
        exec_time=exec_time_ms,
        nodes_used=num_nodes,
        csv_file=csv_file,
        method="hazelcast",
        transfer_time=transfer_time_ms
    )

    client.shutdown()


def main():
    csv_file = "matrix_benchmark.csv"

    # Escribir cabecera del CSV
    with open(csv_file, mode="w", newline='') as f:
        f.write("Method,Matrix Size,Execution Time (ms),Memory Used (MB),CPU Usage (%),Nodes Used,Transfer Time (ms)\n")

    for matrix_size in [256, 512, 1024, 2048]:
        num_nodes = 2

        # Multiplicación básica
        run_and_log(
            method_name="basic",
            multiply_func=MatrixMultiplier.basic_multiply,
            matrix_size=matrix_size,
            csv_file=csv_file
        )

        # Multiplicación paralela
        run_and_log(
            method_name="parallel",
            multiply_func=MatrixMultiplier.parallel_multiply,
            matrix_size=matrix_size,
            csv_file=csv_file,
            num_threads=4
        )

        # Multiplicación distribuida
        run_hazelcast(
            matrix_size=matrix_size,
            csv_file=csv_file,
            num_nodes=num_nodes
        )


if __name__ == "__main__":
    main()
