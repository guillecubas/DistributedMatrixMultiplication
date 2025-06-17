from pyspark.sql import SparkSession
import numpy as np
import sys

def main():
    # Spark session
    spark = SparkSession.builder \
        .appName("DistributedMatrixMultiplication") \
        .getOrCreate()

    sc = spark.sparkContext

    # Matrix size as command line argument
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000

    # Generate random matrices
    A = np.random.rand(N, N)
    B = np.random.rand(N, N)

    # Transpose B to make it easy to access columns
    B_T = B.T

    # Create RDDs of rows of A and columns of B
    rdd_A = sc.parallelize([(i, A[i]) for i in range(N)])
    rdd_B = sc.parallelize([(j, B_T[j]) for j in range(N)])

    # Cartesian product and compute dot products
    result = rdd_A.cartesian(rdd_B) \
        .map(lambda pair: ((pair[0][0], pair[1][0]),
                           float(np.dot(pair[0][1], pair[1][1])))) \
        .collect()

    # Print a sample of the result
    for ((i, j), value) in result[:5]:
        print(f"C[{i}][{j}] = {value:.4f}")

    spark.stop()

if __name__ == "__main__":
    main()
