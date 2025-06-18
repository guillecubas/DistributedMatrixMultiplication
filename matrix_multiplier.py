import multiprocessing

def multiply_row(args):
    row, matrix_b, size = args
    result_row = [
        sum(row[k] * matrix_b[k][j] for k in range(size))
        for j in range(size)
    ]
    return result_row

class MatrixMultiplier:

    @staticmethod
    def multiply(matrix_a, matrix_b, size, num_processes):
        with multiprocessing.Pool(processes=num_processes) as pool:
            result_matrix = pool.map(
                multiply_row,
                [(matrix_a[i], matrix_b, size) for i in range(size)]
            )
        return result_matrix
