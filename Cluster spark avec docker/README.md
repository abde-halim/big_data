# Cluster Spark avec Docker

## Objective

This TP aims to set up a complete development environment for Big Data projects using Docker Compose. It enables you to deploy a multi-node Hadoop and Spark cluster in isolated containers.

## Description

This project configures a distributed infrastructure with:

- **Master Node**: Runs Hadoop NameNode, YARN ResourceManager, Spark Master, and Jupyter Notebook
- **Slave Node(s)**: Run Hadoop DataNode, YARN NodeManager, and Spark Workers

## Prerequisites

- Docker Engine installed
- Docker Compose installed
- At least 4 GB available RAM
- Sufficient disk space for Docker images

## Architecture

```
┌─────────────────────────────────────┐
│     hadoop-master (Master Node)     │
│ ├─ Hadoop NameNode (port 9870)      │
│ ├─ YARN ResourceManager (port 8088) │
│ ├─ Spark Master (port 7077)         │
│ ├─ Jupyter (port 8888)              │
│ └─ MapReduce JobHistory (port 19888)│
└─────────────────────────────────────┘
          ↓
┌─────────────────────────────────────┐
│     hadoop-slave1 (Worker Node)     │
│ ├─ Hadoop DataNode                  │
│ ├─ YARN NodeManager (port 8042)     │
│ └─ Spark Worker                     │
└─────────────────────────────────────┘
```

## Configuration

### Available Services

| Service              | URL                    | Port  | Description             |
| -------------------- | ---------------------- | ----- | ----------------------- |
| Hadoop NameNode      | http://localhost:9870  | 9870  | HDFS Admin UI           |
| YARN ResourceManager | http://localhost:8088  | 8088  | Resource Management     |
| Spark Master         | http://localhost:7077  | 7077  | Spark Cluster Manager   |
| MapReduce JobHistory | http://localhost:19888 | 19888 | Job History             |
| Jupyter Notebook     | http://localhost:8888  | 8888  | Interactive Environment |
| HDFS NameNode        | localhost:9000         | 9000  | Native HDFS Port        |
| Spark Standalone     | http://localhost:8080  | 8080  | Spark Standalone UI     |

## Usage

### Start the Cluster

```bash
docker-compose up -d
```

### Check Status

```bash
docker-compose ps
```

### Access Interfaces

- **Hadoop NameNode**: http://localhost:9870
- **YARN UI**: http://localhost:8088
- **Spark Master**: http://localhost:7077
- **Jupyter**: http://localhost:8888

### Execute Commands in Containers

```bash
# Access master node
docker exec -it hadoop-master bash

# Access worker node
docker exec -it hadoop-slave1 bash
```

### Stop the Cluster

```bash
docker-compose down
```

## Hadoop and Spark Setup

### Start Hadoop and Spark

Inside the master container:

```bash
docker exec -it hadoop-master bash
./start-hadoop.sh
./start-spark.sh
```

Verify startup with:

```bash
jps
```

## Spark Examples

### 1. Calculate Pi with Spark

```bash
spark-submit \
  --class org.apache.spark.examples.SparkPi \
  --master local[*] \
  $SPARK_HOME/examples/jars/spark-examples_{version}.jar \
  100
```

### 2. WordCount with Spark Shell

```bash
spark-shell

# In Scala shell:
val data = sc.textFile("hdfs://hadoop-master:9000/user/root/input/alice.txt")
val count = data.flatMap(line => line.split(" ")).map(word => (word, 1)).reduceByKey(_+_)
count.saveAsTextFile("hdfs://hadoop-master:9000/user/root/output/spark1")
```

### 3. Python Application

Create `wordcount.py`:

```python
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("yarn").appName('wordcount').getOrCreate()
data = spark.sparkContext.textFile("hdfs://hadoop-master:9000/user/root/input/alice.txt")
words = data.flatMap(lambda line: line.split(" "))
wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a+b)
wordCounts.saveAsTextFile("hdfs://hadoop-master:9000/user/root/output/spark2")
```

Submit with:

```bash
spark-submit wordcount.py
```

## PySpark on Google Colab

### Installation

In Colab cell:

```bash
!sudo apt update
!apt-get install openjdk-8-jdk-headless -qq > /dev/null
!wget -q https://dlcdn.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz
!tar xf spark-3.2.1-bin-hadoop3.2.tgz
!pip install -q findspark
!pip install pyspark
!pip install py4j
!pip install -q pymongo matplotlib seaborn
```

### Configuration

```python
import os
import sys
import findspark

findspark.init()
findspark.find()
```

### Start Spark Session

```python
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
  .appName("ColabSpark") \
  .config("spark.driver.memory", "2g") \
  .getOrCreate()

print("Spark configured successfully!")
```

### Create and Use DataFrames

```python
# Create DataFrame
data = [(1, "Alice", 23), (2, "Bob", 30), (3, "Charlie", 29)]
columns = ["id", "name", "age"]
df = spark.createDataFrame(data, columns)

# Display
df.show()

# Operations
df.printSchema()
df.select("name", "age").show()
df.filter(df.age > 25).show()
```

## Load and Manipulate Data

### Load CSV

```python
df = spark.read.csv("/content/transactions.csv",
                    header=True, inferSchema=True)
df.show(5)
```

### Filter and Group

```python
# Filter
df.filter(df["Amount"] > 1000).show()

# Group and aggregate
df.groupBy("Type").sum("Amount").show()

# Sort
df.orderBy(df["Amount"].desc()).show(5)
```

## MongoDB Integration

### Configuration

```python
mongo_uri = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/bankdb.transactions?retryWrites=true&w=majority"

spark = SparkSession.builder \
  .appName("MongoDBIntegration") \
  .config("spark.mongodb.input.uri", mongo_uri) \
  .config("spark.mongodb.output.uri", mongo_uri) \
  .getOrCreate()
```

### Load from MongoDB

```python
df_mongo = spark.read.format("mongo") \
  .option("uri", mongo_uri) \
  .load()

df_mongo.show(5)
```

### Analyze Data

```python
# Average by type
df_mongo.groupBy("Transaction Type") \
  .avg("Transaction Amount") \
  .show()

# Count by account
df_mongo.groupBy("Sender Account ID") \
  .count() \
  .filter("count > 5") \
  .show()
```

## Visualization

### Using Seaborn

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Prepare data
df_grouped = df.groupBy("Type").sum("Amount").toPandas()
df_grouped.columns = ["Type", "Total Amount"]

# Plot
plt.figure(figsize=(10, 5))
sns.barplot(data=df_grouped, x="Type", y="Total Amount",
            palette="coolwarm")
plt.title("Total Amount by Type")
plt.show()
```

### Histogram

```python
df_pandas = df.select("Amount").toPandas()

plt.figure(figsize=(10, 5))
sns.histplot(df_pandas["Amount"], bins=30, kde=True,
            color="blue")
plt.title("Amount Distribution")
plt.show()
```

### Comparison Plot

```python
df_status = df.groupBy("Status").count().toPandas()
df_status.columns = ["Status", "Count"]

plt.figure(figsize=(7, 5))
sns.barplot(data=df_status, x="Status", y="Count",
           palette="pastel")
plt.title("Success vs Failed")
plt.show()
```

## Important Points

- Shared files mounted via `~/Documents/hadoop_project/`
- Docker network `hadoop` connects all nodes
- Ports exposed for web interface access
- STDIN and TTY enabled for interactive use

## Troubleshooting

- **Containers not starting**: Check available resources
- **No NameNode connection**: Wait 30 seconds after startup
- **Volume issues**: Check shared directory permissions

## Next Steps

Once configured, proceed to:

- **Lab 1**: HDFS and Hadoop
- **Lab 3**: MapReduce
- **Lab 4**: Kafka
- **Spark SQL / Spark Streaming**: Data analysis and streaming
