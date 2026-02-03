# TP Spark Streaming

## Objective

This laboratory explores **Apache Spark Streaming** for real-time data processing. You will learn to:

- Process data streams continuously
- Implement stateless and stateful transformations
- Use data sources (sockets, Kafka)
- Manage micro-batches and temporal windows
- Write results to sinks (console, files)

## Description

This project provides real-time data processing with:

### 1. **server.py** - Data Source

Socket server generating continuous message streams to simulate a data source.

### 2. **client.py** - Spark Streaming Consumer

Spark Streaming application connecting to the source and processing data in real-time.

### 3. **Questions.txt** - Directives

Questions and exercises for implementation.

## Architecture

```
Socket Server (server.py)
    ↓ (sends messages)
Spark Streaming DStream
    ↓ (micro-batches)
┌──────────────────────┐
│  Transformations     │
│  - Tokenization      │
│  - Filtering         │
│  - Aggregation       │
│  - Windowing         │
└──────────────────────┘
    ↓ (outputs)
┌──────────────────────┐
│  Sinks               │
│  - Console (print)   │
│  - HDFS              │
│  - Database          │
└──────────────────────┘
```

## Prerequisites

- Python 3.7+
- Apache Spark 3.0+
- PySpark installed
- Java 8+ installed
- Running Hadoop cluster (optional)

## Installation

### PySpark Installation

```bash
# Via pip
pip install pyspark

# Or download from Apache
wget https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
tar -xzf spark-3.5.0-bin-hadoop3.tgz
export SPARK_HOME=/path/to/spark-3.5.0-bin-hadoop3
export PATH=$PATH:$SPARK_HOME/bin
```

## Project Structure

```
tp_spark_streaming/
├── README.md              # This file
├── CONTENT.md             # Original PDF content (French)
├── Questions.txt          # Exercises
├── server.py             # Data source (socket server)
└── client.py             # Spark Streaming consumer
```

## Usage

### Step 1: Start the Data Source

```bash
python server.py
```

Expected output:

```
test
test2
🟢 Server waiting for connection...
🟢 Client connected from: ('127.0.0.1', 12345)
```

### Step 2: Run Spark Streaming (another terminal)

```bash
python client.py
```

## Server Code (server.py)

```python
import socket, time, threading

def start_socket_server():
    host = "127.0.0.1"
    port = 9999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    print("🟢 Server waiting for connection...")

    conn, addr = s.accept()
    print("🟢 Client connected from:", addr)

    messages = [
        "spark streaming dstream",
        "spark spark streaming",
        "big data spark"
    ]

    while True:
        for msg in messages:
            conn.send((msg + "\n").encode())
            time.sleep(2)

threading.Thread(target=start_socket_server).start()
```

## Spark Streaming Code (client.py) - Example

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, col, window, count

spark = SparkSession.builder \
    .appName("SocketStreamingApp") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Read from socket
lines = spark.readStream \
    .format("socket") \
    .option("host", "127.0.0.1") \
    .option("port", 9999) \
    .load()

# Tokenize
words = lines.select(
    explode(split(col("value"), " ")).alias("word")
)

# Count words
word_counts = words.groupBy("word").count()

# Display results
query = word_counts \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .option("numRows", 25) \
    .option("truncate", False) \
    .start()

query.awaitTermination()
```

## Key Concepts

### DStream (Discretized Stream)

Abstracts a continuous stream into a sequence of RDDs processed by micro-batches.

### Micro-batch

Time interval (default 500ms) between processing cycles.

### Output Modes

| Mode       | Description                 |
| ---------- | --------------------------- |
| `append`   | Add new rows only (default) |
| `update`   | Update modified rows        |
| `complete` | Show full state             |

### Stateless Transformations

```python
# Tokenization
words = lines.select(explode(split(col("value"), " ")).alias("word"))

# Filtering
filtered = words.filter(col("word") != "")

# Mapping
mapped = words.select(upper(col("word")).alias("word"))
```

### Stateful Transformations (Aggregations)

```python
# GroupBy
word_counts = words.groupBy("word").count()

# Temporal windowing
windowed = words \
    .groupBy(
        window(col("timestamp"), "10 seconds"),
        col("word")
    ) \
    .count()
```

### Windowing

```python
from pyspark.sql.functions import window

# 10-second window, 5-second slide
windowed = data.groupBy(
    window(col("timestamp"), "10 seconds", "5 seconds"),
    col("category")
).count()
```

## Data Sources

### Socket

```python
lines = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()
```

### Kafka

```python
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "my-topic") \
    .load()
```

### Files (HDFS/Local)

```python
df = spark.readStream \
    .schema("timestamp TIMESTAMP, value STRING") \
    .option("path", "/path/to/files") \
    .csv()
```

## Output Sinks

### Console

```python
query = df.writeStream \
    .format("console") \
    .start()
```

### HDFS/Parquet

```python
query = df.writeStream \
    .format("parquet") \
    .option("path", "/path/to/output") \
    .option("checkpointLocation", "/path/to/checkpoint") \
    .start()
```

### Custom Processing

```python
def process_batch(batch_df, batch_id):
    batch_df.show()

query = df.writeStream \
    .foreachBatch(process_batch) \
    .start()
```

## Practical Exercises (Questions.txt)

### 1. Simple Word Counting

Count word occurrences from the stream.

### 2. Filtering

Filter words with less than 3 characters.

### 3. Real-time Statistics

Calculate: total, average, max, min per second.

### 4. Temporal Windows

Count words in 10-second windows.

### 5. Persistent State

Maintain cumulative word counts.

### 6. Multiple Sinks

Display on console AND write to HDFS.

### 7. Kafka Integration

Use Kafka as source instead of socket.

## State Management

### mapGroupsWithState

```python
def update_function(key, new_events, state):
    old_count = state.get or 0
    new_count = old_count + len(new_events)
    state.update(new_count)
    return (key, new_count)

word_counts = words \
    .groupByKey("word") \
    .mapGroupsWithState(
        outputMode="update",
        timeoutConf="1 hour"
    )(update_function)
```

### flatMapGroupsWithState

Maintain complex state with timeout.

## Checkpoint and Recovery

```python
query = df.writeStream \
    .format("console") \
    .option("checkpointLocation", "/path/to/checkpoint") \
    .start()
```

Enables recovery after crashes.

## Performance and Optimization

### Micro-batch Interval

```python
spark.conf.set("spark.streaming.kafka.maxRatePerPartition", "10000")
```

### Partitioning

```python
df.repartition(10).writeStream...
```

### Caching

```python
df.cache()  # Limited in streaming
```

## Troubleshooting

- **Port already in use**: Change port (9999 → 9998)
- **No data flowing**: Check server-client connection
- **OOM errors**: Reduce batch size or micro-batch interval
- **Slow processing**: Increase partitions
- **Lost connection**: Implement reconnection logic

## Recommended Architecture

```
┌─────────────────────────────────────┐
│  Data Sources                       │
│  (Kafka, Socket, Files)             │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Spark Streaming DStream            │
│  - Parsing                          │
│  - Filtering                        │
│  - Transformations                  │
└──────────────┬──────────────────────┘
               │
      ┌────────┴────────┐
      │                 │
┌─────▼──────┐  ┌──────▼─────┐
│  Console   │  │  MongoDB   │
│  (Debug)   │  │  (Storage) │
└────────────┘  └────────────┘
      │                 │
      └────────┬────────┘
               │
        ┌──────▼──────┐
        │  Dashboard  │
        │  (Analytics)│
        └─────────────┘
```

## Integration with Other Components

### Spark Streaming + Kafka

```python
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "events") \
    .load()
```

### Spark Streaming + MongoDB

```python
def write_to_mongo(batch_df, batch_id):
    batch_df.write \
        .format("mongodb") \
        .mode("append") \
        .option("uri", "mongodb://localhost:27017") \
        .option("database", "streaming") \
        .option("collection", "results") \
        .save()

query = df.writeStream \
    .foreachBatch(write_to_mongo) \
    .start()
```

## Next Steps

1. **Complete exercises** in Questions.txt
2. **Integrate Kafka** as data source
3. **Persist results** to MongoDB
4. **Create real-time dashboard**
5. **Deploy on Spark cluster**

## Resources

- [Spark Streaming Docs](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-api-compatibility.html)
- [Kafka Integration](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html)
- [Performance Tuning](https://spark.apache.org/docs/latest/streaming-programming-guide.html#performance-tuning)

## Important Points

- **Exactly-once**: Spark Streaming guarantees single processing
- **End-to-end fault tolerance**: Via checkpointing
- **Low latency**: With proper configuration
- **Scalability**: Increase executors for more throughput
