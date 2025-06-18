import random

class MatrixUtils:

    @staticmethod
    def generate_matrix(size):
        return [[random.randint(0, 9) for _ in range(size)] for _ in range(size)]

    @staticmethod
    def print_matrix(matrix):
        for row in matrix:
            print(" ".join(map(str, row)))
