#!/bin/bash

# === CONFIGURATION ===
PYTHON_SCRIPT="/app/spark_matrix_mult.py"
CONTAINER_NAME="spark-master"
SPARK_MASTER_URL="spark://spark-master:7077"
RESULTS_FILE="results_python_spark.csv"
OUTPUT_DIR="output_logs_python"

# === PREPARE FOLDERS AND CSV ===
mkdir -p "$OUTPUT_DIR"
echo "MatrixSize,Worker1MemMB,Worker2MemMB,Worker1CPU,Worker2CPU" > "$RESULTS_FILE"

# === MATRIX SIZES TO TEST ===
for MATRIX_SIZE in 512 1024 2048 4096; do
  echo "🚀 Running PySpark job for matrix size $MATRIX_SIZE..."

  LOG_FILE="$OUTPUT_DIR/output_${MATRIX_SIZE}.txt"
  STATS_FILE="$OUTPUT_DIR/stats_${MATRIX_SIZE}.txt"

  # === RUN SPARK JOB AND SAVE LOG ===
  docker exec "$CONTAINER_NAME" bash -c \
  "spark-submit --master $SPARK_MASTER_URL $PYTHON_SCRIPT $MATRIX_SIZE" > "$LOG_FILE" 2>&1

  # === CAPTURE MEMORY AND CPU USAGE ===
  docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" > "$STATS_FILE"

  CPU1=$(grep "spark-worker-1" "$STATS_FILE" | awk '{print $2}' | sed 's/[^0-9.]//g')
  MEM1=$(grep "spark-worker-1" "$STATS_FILE" | awk '{print $3}' | sed 's/[^0-9.]//g')
  CPU2=$(grep "spark-worker-2" "$STATS_FILE" | awk '{print $2}' | sed 's/[^0-9.]//g')
  MEM2=$(grep "spark-worker-2" "$STATS_FILE" | awk '{print $3}' | sed 's/[^0-9.]//g')

  echo "📊 Resources for $MATRIX_SIZE: W1 ${MEM1}MB ${CPU1}%, W2 ${MEM2}MB ${CPU2}%"
  echo "$MATRIX_SIZE,$MEM1,$MEM2,$CPU1,$CPU2" >> "$RESULTS_FILE"
done

echo "✅ PySpark results saved:"
echo "📄 CSV: $RESULTS_FILE"
echo "📂 Logs: $OUTPUT_DIR/"
