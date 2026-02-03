# Big Data Labs - Complete Documentation

## What Has Been Created

### Markdown Files Created

**Total: 9 Comprehensive Markdown Files**

```
✓ DOCUMENTATION_GUIDE.md      - Navigation guide for all docs
✓ lab0/README.md              - Docker Cluster Setup (English)
✓ lab_spark_sql_fifa/CONTENT.md  - FIFA Queries (French, from PDF)
✓ lab3 - mapReduce/CONTENT.md    - MapReduce Tutorial (French, from PDF)
✓ lab4/kafka/CONTENT.md          - Kafka Tutorial (French, from PDF)
✓ Cluster spark avec docker/CONTENT.md  - Spark Cluster (French, from PDF)
✓ tp_mongoDB/CONTENT.md       - MongoDB Tutorial (French, from PDF)
✓ tp_spark_streaming/CONTENT.md - Spark Streaming (French, from PDF)
```

## Project Structure

### With English Guides (README.md)

- **Lab 0** - Docker Cluster Setup
- **Lab 1** - Hadoop HDFS (Python + guide)
- **Lab Spark SQL FIFA** - Data Analysis
- **Lab 3 - MapReduce** - Batch Processing
- **Lab 4 - Kafka** - Message Streaming
- **Cluster Spark Docker** - Production Setup
- **TP MongoDB** - NoSQL Database
- **TP Spark Streaming** - Real-time Processing

### With French Content (CONTENT.md - from PDFs)

- **Lab Spark SQL FIFA** - 22 SQL questions
- **Lab 3 - MapReduce** - Complete MapReduce guide with code
- **Lab 4 - Kafka** - Full Kafka tutorial with examples
- **Cluster Spark Docker** - Spark setup and MongoDB integration
- **TP MongoDB** - Database operations and dashboards
- **TP Spark Streaming** - DStream programming

## 🎯 How to Use

### If You Want to Learn (English)

👉 Read **README.md** files in each project:

- Clean, structured educational content
- Step-by-step guides
- Code examples
- Best practices
- Troubleshooting

**Example:**

```bash
cat lab0/README.md          # Docker setup guide
cat lab4/kafka/README.md    # Kafka comprehensive guide
```

### If You Need PDF Content (French)

👉 Read **CONTENT.md** files:

- Original PDF content converted to markdown
- Exact exercises and requirements
- Specific questions to answer
- Lab assignments

**Example:**

```bash
cat lab_spark_sql_fifa/CONTENT.md  # 22 FIFA queries
cat lab3\ -\ mapReduce/CONTENT.md   # MapReduce lab
```

### Navigation

👉 Start with **DOCUMENTATION_GUIDE.md** for overview

## 📊 File Statistics

| Component       | English (README) | French (CONTENT) | Code Files         |
| --------------- | ---------------- | ---------------- | ------------------ |
| Lab 0           |                  | —                | docker-compose.yml |
| Lab 1           |                  | —                | Java + Python      |
| Spark SQL FIFA  |                  |                  | Python             |
| MapReduce       |                  |                  | Java + Python      |
| Kafka           |                  |                  | Java               |
| Spark Cluster   |                  |                  | Python             |
| MongoDB         |                  |                  | Python             |
| Spark Streaming |                  |                  | Python             |

## 🚀 Quick Start

### 1. Understand What's What

```bash
cat DOCUMENTATION_GUIDE.md  # Read this first
```

### 2. Choose Your Path

**Path A: Complete Learning**

```bash
cat lab0/README.md                # Start with Docker
cat lab1/README.md                # Learn HDFS
cat lab3\ -\ mapReduce/README.md  # Learn MapReduce
cat lab4/kafka/README.md          # Learn Kafka
```

**Path B: Exact Requirements**

```bash
cat lab3\ -\ mapReduce/CONTENT.md        # MapReduce assignments
cat lab4/kafka/CONTENT.md                # Kafka assignments
cat lab_spark_sql_fifa/CONTENT.md        # FIFA SQL questions
cat tp_mongoDB/CONTENT.md                # MongoDB assignments
```

**Path C: Specific Topic**

```bash
# For Spark SQL
cat lab_spark_sql_fifa/CONTENT.md   # Assignments
cat lab_spark_sql_fifa/README.md    # Full guide

# For Real-time Processing
cat tp_spark_streaming/CONTENT.md   # Assignments
cat tp_spark_streaming/README.md    # Full guide

# For Data Storage
cat tp_mongoDB/CONTENT.md           # Assignments
cat tp_mongoDB/README.md            # Full guide
```

## 📖 Content Overview

### Lab 0 - Docker Cluster

- **English (README)**: Master/Slave architecture, Docker Compose, service URLs
- **No PDF**: Original content only in README

### Lab 1 - HDFS

- **English (README)**: HDFS read/write/inspect operations
- **No PDF**: Guide-only project

### Lab Spark SQL - FIFA

- **English (README)**: Spark SQL API, DataFrame operations, code examples
- **French (CONTENT)**: 22 specific questions from discovery to analytics
  1. Simple queries (count, year range, top tournaments)
  2. Aggregations (averages, rankings, statistics)
  3. Advanced analytics (windows, ROW_NUMBER, goal average)

### Lab 3 - MapReduce

- **English (README)**: MapReduce concepts, Mapper/Reducer classes, Java/Python examples
- **French (CONTENT)**: Step-by-step implementation with exact code
  - Maven project setup
  - TokenizerMapper class
  - IntSumReducer class
  - WordCount application
  - Python streaming implementation

### Lab 4 - Kafka

- **English (README)**: Kafka architecture, producers, consumers, streams
- **French (CONTENT)**: Complete tutorial
  - Topic creation and management
  - EventProducer implementation
  - EventConsumer implementation
  - Kafka Connect
  - WordCount Streams application
  - Multi-broker cluster setup
  - Kafka-UI dashboard

### Cluster Spark Docker

- **English (README)**: Complete Spark cluster setup and operations
- **French (CONTENT)**:
  - Hadoop startup
  - Spark examples (Pi, WordCount)
  - PySpark on Colab
  - CSV loading and manipulation
  - MongoDB Atlas integration
  - Visualization with Seaborn

### TP MongoDB

- **English (README)**: CRUD operations, aggregation, index management
- **French (CONTENT)**:
  - MongoDB Atlas account creation
  - Connection setup
  - Collection creation
  - CRUD operations
  - Import JSON data
  - Aggregation framework
  - MapReduce on collections
  - Dashboard creation with MongoDB Charts

### TP Spark Streaming

- **English (README)**: Real-time processing, DStream, micro-batches
- **French (CONTENT)**:
  - Socket server setup
  - StreamingContext creation
  - WordCount streaming
  - Questions and exercises

## 🎓 Learning Objectives

| Lab             | Main Concepts                         |
| --------------- | ------------------------------------- |
| Lab 0           | Docker, Container Orchestration       |
| Lab 1           | Distributed File System (HDFS)        |
| Spark SQL       | SQL on Spark, DataFrame API           |
| MapReduce       | Map-Reduce paradigm, Batch processing |
| Kafka           | Message streaming, Pub-Sub            |
| Cluster         | Production deployment                 |
| MongoDB         | NoSQL database operations             |
| Spark Streaming | Real-time stream processing           |

## 💡 Tips

1. **Start small**: Begin with Lab 0 to get infrastructure running
2. **Use both languages**: English guides for understanding, French for exact requirements
3. **Code along**: Copy examples and run them
4. **Follow the flow**: Each README suggests "Next Steps"
5. **Cross-reference**: When needed, check both README and CONTENT files

## 📝 Format Note

- **README.md**: Human-readable, organized, educational
- **CONTENT.md**: PDF-to-markdown conversion, preserves original format and questions
- **Both**: Complementary resources

## 🔍 Finding Things

**Need to know...**

- **How Docker works?** → `lab0/README.md`
- **MapReduce implementation?** → `lab3/CONTENT.md`
- **Kafka producer code?** → `lab4/kafka/CONTENT.md`
- **MongoDB aggregation?** → `tp_mongoDB/CONTENT.md`
- **Spark Streaming concepts?** → `tp_spark_streaming/README.md`
- **SQL queries on FIFA data?** → `lab_spark_sql_fifa/CONTENT.md`

---

**All files are in Markdown format and can be:**

- Read in any text editor
- Viewed on GitHub
- Converted to PDF if needed
- Used offline
- Shared easily

Happy Learning! 🚀
