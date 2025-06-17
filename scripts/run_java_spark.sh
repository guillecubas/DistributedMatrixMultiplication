#!/bin/bash

# === CONFIGURATION ===
MAIN_CLASS="org.ulpgc.SparkMatrixMultiplication"
JAVA_DIR="java"
JAR_NAME="SparkMatrixMultiplication-1.0-SNAPSHOT.jar"
JAR_PATH="$JAVA_DIR/target/$JAR_NAME"
REMOTE_PATH="/app/$JAR_NAME"
CONTAINER_NAME="spark-master"
SPARK_MASTER_URL="spark://spark-master:7077"
RESULTS_FILE="results_java_spark.csv"
OUTPUT_DIR="output_logs"

# === BUILD THE JAR ===
echo "🔧 Building Java project with Maven..."
cd "$JAVA_DIR" || exit 1
mvn clean package || exit 1
cd - > /dev/null || exit 1

# === COPY JAR TO CONTAINER ===
echo "📦 Copying JAR to $CONTAINER_NAME..."
docker cp "$JAR_PATH" "$CONTAINER_NAME":"$REMOTE_PATH" || {
  echo "❌ Error: JAR not found at '$JAR_PATH'."
  exit 1
}

# === PREPARE FOLDERS AND CSV ===
mkdir -p "$OUTPUT_DIR"
echo "MatrixSize,Worker1MemMB,Worker2MemMB,Worker1CPU,Worker2CPU" > "$RESULTS_FILE"

# === MATRIX SIZES TO TEST ===
for MATRIX_SIZE in 512 1024 2048 4096 8192; do
  echo "🚀 Running Spark job for matrix size $MATRIX_SIZE..."

  LOG_FILE="$OUTPUT_DIR/output_${MATRIX_SIZE}_java.txt"
  STATS_FILE="$OUTPUT_DIR/stats_${MATRIX_SIZE}_java.txt"

  # === RUN SPARK JOB AND SAVE LOG ===
  docker exec "$CONTAINER_NAME" bash -c \
  "spark-submit --class $MAIN_CLASS --master $SPARK_MASTER_URL $REMOTE_PATH $MATRIX_SIZE" > "$LOG_FILE" 2>&1

  # === CAPTURE MEMORY AND CPU USAGE ===
  docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" > "$STATS_FILE"

  CPU1=$(grep "spark-worker-1" "$STATS_FILE" | awk '{print $2}' | sed 's/[^0-9.]//g')
  MEM1=$(grep "spark-worker-1" "$STATS_FILE" | awk '{print $3}' | sed 's/[^0-9.]//g')
  CPU2=$(grep "spark-worker-2" "$STATS_FILE" | awk '{print $2}' | sed 's/[^0-9.]//g')
  MEM2=$(grep "spark-worker-2" "$STATS_FILE" | awk '{print $3}' | sed 's/[^0-9.]//g')

  echo "📊 Resources for $MATRIX_SIZE: W1 ${MEM1}MB ${CPU1}%, W2 ${MEM2}MB ${CPU2}%"
  echo "$MATRIX_SIZE,$MEM1,$MEM2,$CPU1,$CPU2" >> "$RESULTS_FILE"
done

echo "✅ Results saved:"
echo "📄 CSV: $RESULTS_FILE"
echo "📂 Logs: $OUTPUT_DIR/"
