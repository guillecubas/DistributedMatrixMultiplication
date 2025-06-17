package org.ulpgc;

import scala.Tuple2;
import java.util.*;

public class MatrixUtils {
    public static double[][] generateRandomMatrix(int n) {
        Random rand = new Random();
        double[][] m = new double[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                m[i][j] = rand.nextDouble();
        return m;
    }

    public static double[][] transpose(double[][] m) {
        int n = m.length;
        double[][] t = new double[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                t[j][i] = m[i][j];
        return t;
    }

    public static double dotProduct(double[] a, double[] b) {
        double sum = 0;
        for (int i = 0; i < a.length; i++) sum += a[i] * b[i];
        return sum;
    }

    public static List<Tuple2<Integer, double[]>> toIndexedRows(double[][] matrix) {
        List<Tuple2<Integer, double[]>> rows = new ArrayList<>();
        for (int i = 0; i < matrix.length; i++) {
            rows.add(new Tuple2<>(i, matrix[i]));
        }
        return rows;
    }
}
