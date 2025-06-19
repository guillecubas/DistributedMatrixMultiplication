import multiprocessing
import threading
from distributed_tasks import remote_multiply_partition


def multiply_row(args):
    row, matrix_b, size = args
    result_row = [
        sum(row[k] * matrix_b[k][j] for k in range(size))
        for j in range(size)
    ]
    return result_row


class MatrixMultiplier:

    @staticmethod
    def multiply(matrix_a, matrix_b, size, num_nodes, client=None):
        """
        Distribuye la multiplicación en los nodos Hazelcast mediante executor_service.
        Usa 'submit' (no 'submit_to_member') para que Hazelcast asigne los nodos automáticamente.
        """
        if client is None:
            raise ValueError("Hazelcast client must be provided for distributed execution.")

        executor = client.get_executor("matrix-executor")
        step = size // num_nodes
        futures = []

        for i in range(num_nodes):
            start_row = i * step
            end_row = size if i == num_nodes - 1 else (i + 1) * step

            task_context = {
                "matrix_a": matrix_a,
                "matrix_b": matrix_b,
                "start_row": start_row,
                "end_row": end_row
            }

            # ✅ Método correcto y soportado en Hazelcast Python Client
            future = executor.submit(remote_multiply_partition, task_context)
            futures.append((start_row, future))

        result_matrix = [None] * size
        for start_row, future in futures:
            partial_result = future.result()
            for i, row in enumerate(partial_result):
                result_matrix[start_row + i] = row

        return result_matrix

    @staticmethod
    def basic_multiply(matrix_a, matrix_b, size):
        result = [[0 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    result[i][j] += matrix_a[i][k] * matrix_b[k][j]
        return result

    @staticmethod
    def parallel_multiply(matrix_a, matrix_b, size, num_threads):
        result = [[0 for _ in range(size)] for _ in range(size)]

        def worker(start_row, end_row):
            for i in range(start_row, end_row):
                for j in range(size):
                    for k in range(size):
                        result[i][j] += matrix_a[i][k] * matrix_b[k][j]

        threads = []
        rows_per_thread = size // num_threads

        for t in range(num_threads):
            start = t * rows_per_thread
            end = size if t == num_threads - 1 else (t + 1) * rows_per_thread
            thread = threading.Thread(target=worker, args=(start, end))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        return result
