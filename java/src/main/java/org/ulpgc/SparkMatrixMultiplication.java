package org.ulpgc;

import org.apache.spark.api.java.*;
import org.apache.spark.SparkConf;
import scala.Tuple2;
import java.util.*;

public class SparkMatrixMultiplication {
    public static void main(String[] args) {
        SparkConf conf = new SparkConf().setAppName("DistributedMatrixMultiplication").setMaster("local[*]");
        JavaSparkContext sc = new JavaSparkContext(conf);

        int N = args.length > 0 ? Integer.parseInt(args[0]) : 1000;

        double[][] A = MatrixUtils.generateRandomMatrix(N);
        double[][] B = MatrixUtils.generateRandomMatrix(N);
        double[][] B_T = MatrixUtils.transpose(B);

        List<Tuple2<Integer, double[]>> rowsA = MatrixUtils.toIndexedRows(A);
        List<Tuple2<Integer, double[]>> colsB = MatrixUtils.toIndexedRows(B_T);

        JavaPairRDD<Integer, double[]> rddA = sc.parallelizePairs(rowsA);
        JavaPairRDD<Integer, double[]> rddB = sc.parallelizePairs(colsB);

        JavaPairRDD<Tuple2<Integer, Integer>, Double> product = rddA.cartesian(rddB)
                .mapToPair(pair -> {
                    int row = pair._1._1;
                    int col = pair._2._1;
                    double[] vecA = pair._1._2;
                    double[] vecB = pair._2._2;
                    double dot = MatrixUtils.dotProduct(vecA, vecB);
                    return new Tuple2<>(new Tuple2<>(row, col), dot);
                });

        List<Tuple2<Tuple2<Integer, Integer>, Double>> result = product.take(5);
        for (Tuple2<Tuple2<Integer, Integer>, Double> entry : result) {
            System.out.println("C[" + entry._1._1 + "][" + entry._1._2 + "] = " + entry._2);
        }

        sc.stop();
    }
}
