# Cluster Spark avec Docker - Lab Exercises

## Objective

Master Apache Spark using a Docker-based Hadoop cluster, plus integrate with MongoDB Atlas. This lab provides 4 essential practical exercises for data processing with Spark and NoSQL.

## Quick Start

```bash
# Generate all exercises
./collab.sh all

# Copy Spark scripts to Docker
docker cp exercises/wordcount_analysis.py exercises/dataframe_agg.py exercises/dataframe_join.py cluster-master:/tmp/

# Run Exercise 1
docker exec cluster-master spark-submit /tmp/wordcount_analysis.py

# Run Exercise 4 (MongoDB) locally
pip install pymongo
python3 exercises/mongodb_integration.py
```

## What You Get

- **Executable Script**: `collab.sh` - Generates and manages exercises
- **4 Applications**: WordCount, Aggregation, Joins, MongoDB Integration
- **Real Data Processing**: Work with HDFS and MongoDB Atlas
- **Learning by Doing**: Hands-on practical exercises

## Prerequisites

- Docker Engine & Docker Compose installed
- Cluster running: `docker-compose up -d`
- Python 3.7+ (for MongoDB exercise)
- At least 4 GB available RAM
- MongoDB Atlas account (for Exercise 4)

## Architecture

```
┌─────────────────────────────────────┐
│     hadoop-master (Master)          │
│ ├─ Hadoop NameNode (HDFS)           │
│ ├─ Spark Master                     │
│ └─ YARN ResourceManager             │
└─────────────────────────────────────┘
          ↓
┌─────────────────────────────────────┐
│     hadoop-slave1 (Worker)          │
│ ├─ Hadoop DataNode                  │
│ ├─ Spark Worker                     │
│ └─ YARN NodeManager                 │
└─────────────────────────────────────┘
          ↓
┌─────────────────────────────────────┐
│  MongoDB Atlas (Cloud)              │
│  cluster0.htrgtlb.mongodb.net       │
└─────────────────────────────────────┘
```

## Available Services

| Service         | URL                   | Port  |
| --------------- | --------------------- | ----- |
| Hadoop NameNode | http://localhost:9870 | 9870  |
| YARN UI         | http://localhost:8088 | 8088  |
| Spark Master    | http://localhost:7077 | 7077  |
| HDFS            | localhost:9000        | 9000  |
| MongoDB Atlas   | cluster0.htrgtlb...   | 27017 |

## 4 Essential Exercises

### Exercise 1: WordCount Analysis with Spark SQL

- **File**: `wordcount_analysis.py`
- **Input**: alice.txt (text file)
- **Output**: Top 20 words by frequency
- **Concepts**: DataFrame, SQL, splitting, counting

### Exercise 2: DataFrame Aggregation

- **File**: `dataframe_agg.py`
- **Input**: sales.csv
- **Output**: Sales totals & averages by region/product
- **Concepts**: groupBy, agg, sum, avg, count

### Exercise 3: DataFrame Joins

- **File**: `dataframe_join.py`
- **Input**: employees.csv, departments.csv
- **Output**: Joined employee-department data
- **Concepts**: INNER JOIN, DataFrames

### Exercise 4: MongoDB Integration

- **File**: `mongodb_integration.py`
- **Input**: MongoDB Atlas cluster
- **Output**: Collections with CRUD operations
- **Concepts**: PyMongo, aggregation pipeline, indexes, CRUD
- **Connection**: `mongodb+srv://abdelilahhalim05_db_user:C2X4AXnO7MJWm52Z@cluster0.htrgtlb.mongodb.net/`
- **Concepts**: INNER JOIN operations

## Commands

```bash
# Show menu
./collab.sh

# Generate Exercise 1
./collab.sh 1

# Generate Exercise 2
./collab.sh 2

# Generate Exercise 3
./collab.sh 3

# Generate all exercises
./collab.sh all
```

## Full Workflow

### 1. Generate Exercises

```bash
cd "/home/ubuntu/Desktop/big_data_labs/Cluster spark avec docker"
./collab.sh all
```

### 2. Copy to Docker

```bash
docker cp exercises/* cluster-master:/tmp/
```

### 3. Upload Sample Data

```bash
# For Exercise 2 (Aggregation)
docker cp /tmp/sales.csv cluster-master:/tmp/
docker exec cluster-master bash -c 'hdfs dfs -put -f /tmp/sales.csv /user/root/input/'

# For Exercise 3 (Joins)
docker cp /tmp/employees.csv /tmp/departments.csv cluster-master:/tmp/
docker exec cluster-master bash -c 'hdfs dfs -put -f /tmp/employees.csv /tmp/departments.csv /user/root/input/'
```

### 4. Run Exercises

```bash
# Exercise 1: WordCount
docker exec cluster-master spark-submit /tmp/wordcount_analysis.py

# Exercise 2: Aggregation
docker exec cluster-master spark-submit /tmp/dataframe_agg.py

# Exercise 3: Joins
docker exec cluster-master spark-submit /tmp/dataframe_join.py
```

### 5. Check Results in HDFS

```bash
docker exec cluster-master bash -c "hdfs dfs -ls /user/root/output/"
```

## Files Generated

- `exercises/wordcount_analysis.py` - Exercise 1
- `exercises/dataframe_agg.py` - Exercise 2
- `exercises/dataframe_join.py` - Exercise 3

## Validation

Check Python syntax:

```bash
python3 -m py_compile exercises/wordcount_analysis.py
python3 -m py_compile exercises/dataframe_agg.py
python3 -m py_compile exercises/dataframe_join.py
```

## Documentation

- **EXERCISES.md** - Exercise details and instructions
- **collab.sh** - The executable script

## Useful Links

- [Spark Documentation](https://spark.apache.org/docs/latest/)
- [Hadoop HDFS](https://hadoop.apache.org/)
- [Docker Documentation](https://docs.docker.com/)
  ./start-spark.sh

````

Verify startup with:

```bash
jps
````

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
