#!/bin/bash

echo "======================================"
echo " TP Spark Cluster – Full Verification "
echo "======================================"

MASTER=cluster-master
SLAVES=("cluster-slave1" "cluster-slave2")
SPARK_JAR="spark-examples_2.12-3.2.4.jar"
INPUT_DIR="/user/root/input"
OUTPUT_DIR="/user/root/output/respark1"
INPUT_FILE="alice.txt"

echo "[1] Checking Docker containers..."

ALL_CONTAINERS=("$MASTER" "${SLAVES[@]}")

for C in "${ALL_CONTAINERS[@]}"; do
  STATUS=$(docker inspect -f '{{.State.Running}}' $C 2>/dev/null)

  if [ "$STATUS" != "true" ]; then
    echo " → Starting container: $C"
    docker start $C
  else
    echo " ✓ Container running: $C"
  fi
done




########################################
echo "[2] Entering hadoop-master container..."

docker exec $MASTER bash -c "

echo '--- Hadoop & Spark status ---'

# Start Hadoop & Spark (safe to re-run)
./start-hadoop.sh
./start-spark.sh

sleep 5

echo '[3] Checking HDFS...'
hdfs dfs -ls / || exit 1

########################################
# 3. Prepare HDFS input
########################################
echo '[4] Preparing HDFS input data...'

hdfs dfs -mkdir -p $INPUT_DIR
echo 'Alice was beginning to get very tired of sitting by her sister on the bank' > /tmp/$INPUT_FILE
hdfs dfs -put -f /tmp/$INPUT_FILE $INPUT_DIR/

hdfs dfs -ls $INPUT_DIR

########################################
# 4. Run SparkPi
########################################
echo '[5] Running SparkPi...'

spark-submit \
 --class org.apache.spark.examples.SparkPi \
 --master local[*] \
 \$SPARK_HOME/examples/jars/$SPARK_JAR \
 100

########################################
# 5. WordCount with spark-shell (non-interactive)
########################################
echo '[6] Running WordCount (Scala)...'

hdfs dfs -rm -r -f $OUTPUT_DIR

spark-shell --master local[*] --driver-memory 1g <<EOF
val data = sc.textFile(\"hdfs://hadoop-master:9000$INPUT_DIR/$INPUT_FILE\")
val count = data
  .flatMap(line => line.split(\" \"))
  .map(word => (word, 1))
  .reduceByKey(_ + _)
count.saveAsTextFile(\"hdfs://hadoop-master:9000$OUTPUT_DIR\")
:quit
EOF

########################################
# 6. Verify results
########################################
echo '[7] Verifying output...'
hdfs dfs -ls $OUTPUT_DIR

echo '=== N9I ==='
"
