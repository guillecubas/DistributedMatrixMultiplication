import hazelcast
from time import time

from matrix_utils import MatrixUtils
from matrix_multiplier import MatrixMultiplier
from metrics_logger import log_metrics

def main():
    csv_file = "hazelcast_benchmark.csv"
    
    # Write header
    with open(csv_file, mode="w", newline='') as f:
        f.write("Matrix Size,Execution Time (ms),Memory Used (MB),CPU Usage (%),Nodes Used,Transfer Time (ms)\n")

    for matrix_size in [256, 512, 1024]:
        num_nodes = 4

        # Hazelcast setup
        client = hazelcast.HazelcastClient()
        matrix_a_map = client.get_map("matrixA").blocking()
        matrix_b_map = client.get_map("matrixB").blocking()
        result_matrix_map = client.get_map("resultMatrix").blocking()

        # Generate matrices
        matrix_a = MatrixUtils.generate_matrix(matrix_size)
        matrix_b = MatrixUtils.generate_matrix(matrix_size)
        matrix_a_map.put("A", matrix_a)
        matrix_b_map.put("B", matrix_b)

        # Multiply
        start_time = time()
        result_matrix = MatrixMultiplier.multiply(matrix_a, matrix_b, matrix_size, num_nodes)
        end_time = time()

        result_matrix_map.put("C", result_matrix)

        if matrix_size <= 10:
            MatrixUtils.print_matrix(result_matrix)

        print(f"Matrix {matrix_size}x{matrix_size} completed in {end_time - start_time:.2f} s")

        log_metrics(matrix_size, end_time - start_time, num_nodes, csv_file)

        client.shutdown()

if __name__ == "__main__":
    main()
