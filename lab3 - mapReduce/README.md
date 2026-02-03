# Lab 3 - MapReduce Programming

## Objective

This laboratory explores the **MapReduce** paradigm for distributed data processing. You will learn to:

- Implement Mappers and Reducers in Java
- Process and analyze large data volumes in parallel
- Understand the Map-Reduce programming model
- Optimize distributed processing performance

## Description

Lab 3 provides two MapReduce implementations:

### 1. **Java Implementation**

MapReduce applications using Hadoop Framework:

- **WordCount.java**: Classic word counting application
  - **Mapper**: Tokenizes text, emits (word, 1)
  - **Reducer**: Sums occurrences per word

- **TokenizerMapper.java**: Advanced text tokenization

- **IntSumReducer.java**: Generic integer summation reducer

### 2. **Python Implementation**

Simple MapReduce scripts using Hadoop Streaming:

- **mapper.py**: Data transformation logic
- **reducer.py**: Data aggregation logic
- **alice.txt**: Test data

## Prerequisites

### For Java

- Java 8+ installed
- Maven 3.6+
- Hadoop 3.2+ configured
- Running Hadoop cluster (Lab 0)

### For Python

- Python 3.7+
- Hadoop Streaming enabled

## Architecture

```
Input Data
    ↓
┌─────────────────┐
│    Mapper       │  Parallel processes
└────────┬────────┘
         ↓ (Key-Value pairs)
┌─────────────────┐
│  Shuffle & Sort │  Group by key
└────────┬────────┘
         ↓
┌─────────────────┐
│   Reducer       │  Aggregation
└────────┬────────┘
         ↓
  Output Data
```

## Project Structure

```
lab3 - mapReduce/
├── README.md                       # This file
├── java/
│   ├── pom.xml                    # Maven config
│   ├── src/main/java/
│   │   └── edu/supmti/mapreduce/
│   │       ├── WordCount.java           # Main app
│   │       ├── TokenizerMapper.java     # Mapper
│   │       └── IntSumReducer.java       # Reducer
│   └── target/                    # Compiled files
└── python/
    ├── alice.txt                  # Test data
    ├── mapper.py                  # Python mapper
    └── reducer.py                 # Python reducer
```

## Compilation (Java)

```bash
cd lab3/java

# Compile
mvn clean package

# JAR created in: target/lab3-mapreduce-1.0.jar
```

## Execution

### Java - Local Mode

```bash
hadoop jar target/lab3-mapreduce-1.0.jar \
  edu.supmti.mapreduce.WordCount \
  input/file.txt \
  output/wordcount
```

### Java - Cluster Mode

```bash
# Copy data to HDFS
hdfs dfs -put input.txt /input/

# Run MapReduce job
hadoop jar target/lab3-mapreduce-1.0.jar \
  edu.supmti.mapreduce.WordCount \
  /input/input.txt \
  /output/wordcount

# Retrieve results
hdfs dfs -get /output/wordcount/part-r-00000 results.txt
```

### Python - Hadoop Streaming

```bash
# Copy files to HDFS
hdfs dfs -put alice.txt /input/
hdfs dfs -mkdir -p /output/wordcount

# Execute with Hadoop Streaming
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /input/alice.txt \
  -output /output/wordcount \
  -mapper "python python/mapper.py" \
  -reducer "python python/reducer.py"

# Retrieve results
hdfs dfs -get /output/wordcount/part-00000 results.txt
```

## Code Examples

### Java Mapper

```java
public class TokenizerMapper
    extends Mapper<Object, Text, Text, IntWritable> {

    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

    public void map(Object key, Text value, Context context)
            throws IOException, InterruptedException {
        StringTokenizer itr = new StringTokenizer(value.toString());
        while (itr.hasMoreTokens()) {
            word.set(itr.nextToken());
            context.write(word, one);
        }
    }
}
```

### Java Reducer

```java
public class IntSumReducer
    extends Reducer<Text, IntWritable, Text, IntWritable> {

    private IntWritable result = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values,
            Context context) throws IOException, InterruptedException {
        int sum = 0;
        for (IntWritable val : values) {
            sum += val.get();
        }
        result.set(sum);
        context.write(key, result);
    }
}
```

### Python Mapper

```python
import sys
for line in sys.stdin:
    words = line.strip().split()
    for word in words:
        print(f"{word}\t1")
```

### Python Reducer

```python
import sys
from collections import defaultdict

word_counts = defaultdict(int)
for line in sys.stdin:
    word, count = line.strip().split('\t')
    word_counts[word] += int(count)

for word, count in sorted(word_counts.items()):
    print(f"{word}\t{count}")
```

## Hadoop Data Types

| Type           | Serialization | Usage                |
| -------------- | ------------- | -------------------- |
| IntWritable    | 32-bit int    | Counters             |
| LongWritable   | 64-bit int    | Large numbers        |
| Text           | UTF-8 string  | Text data            |
| DoubleWritable | Double        | Decimals             |
| FloatWritable  | Float         | Lightweight decimals |

## Key Concepts

### MapReduce Phases

1. **Input**: Read from HDFS, split
2. **Map**: Transform, emit (key, value) pairs
3. **Shuffle**: Group values by key
4. **Sort**: Sort by key
5. **Reduce**: Aggregate values
6. **Output**: Write results

### Partitioning

Defines reducer count via key partition.

### Combiner

Local optimization phase (mini-reducer).

### Speculative Execution

Reruns slow tasks for optimization.

## Practical Exercises

1. **Count words** in a text file
2. **Calculate averages** per group
3. **Sort data** by descending value
4. **Filter data** with conditions
5. **Join two datasets**
6. **Calculate statistics** (min, max, avg)

## Troubleshooting

- **JAR not found**: Verify `mvn clean package` completed
- **Input file missing**: Check HDFS path
- **Class not found**: Verify JAR path and dependencies
- **No reducer**: Check mapper output grouping

## Performance

### Optimizations

- **Compression**: Compress intermediate data
- **Combiner**: Use Combiner for shuffle reduction
- **Partitioning**: Distribute keys evenly
- **Spill**: Reduce memory usage in sort

### Monitoring

```bash
# ResourceManager UI
http://localhost:8088

# Job History
http://localhost:19888
```

## MapReduce Limitations

- **Latency**: Not ideal for interactive queries
- **Iterations**: Multiple passes increase overhead
- **Complexity**: Hard for iterative algorithms
- **I/O Disk**: Each stage writes/reads disk

## Modern Alternatives

- **Spark**: Faster, better optimized
- **Flink**: Better for streaming
- **Presto**: SQL on distributed data

## Next Steps

- **Lab 4**: Kafka - Real-time streaming
- **Spark SQL**: MapReduce optimized
- **Spark Streaming**: Continuous processing
