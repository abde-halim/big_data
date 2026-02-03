# Big Data Labs - Documentation Structure

## Overview

This workspace contains comprehensive Big Data laboratory exercises covering Hadoop, Spark, MapReduce, Kafka, and MongoDB.

For each project, there are **two markdown files**:

1. **README.md** - Comprehensive guide in English
2. **CONTENT.md** - PDF content converted to markdown in French

## Projects Structure

### Lab 0 - Docker Cluster Setup

- **README.md**: Complete guide for setting up Hadoop/Spark cluster with Docker
- **CONTENT.md**: Not available (no PDF)
- **Files**: docker-compose.yml configuration

### Lab 1 - Hadoop HDFS Operations

- **README.md**: Operations on HDFS (reading, writing, inspecting file system)
- **Note**: No CONTENT.md created (no PDF in this folder)
- **Files**: Java code for ReadHDFS, WriteHDFS, HadoopFileStatus

### Lab Spark SQL - FIFA World Cup Analysis

- **README.md**: Spark SQL queries on FIFA dataset
- **CONTENT.md**: Original PDF content in French - 22 questions from simple to advanced analytics
- **Files**: main.py with Spark SQL queries and fifaworldcup.csv dataset

### Lab 3 - MapReduce

- **README.md**: MapReduce programming with Java and Python
- **CONTENT.md**: Original PDF content in French - Complete guide with code examples
- **Files**: Java Mapper/Reducer classes, Python mapper.py and reducer.py scripts

### Lab 4 - Apache Kafka

- **README.md**: Kafka topics, producers, consumers, and streaming applications
- **CONTENT.md**: Original PDF content in French - Complete tutorial with configurations
- **Files**: Java EventProducer, EventConsumer, WordCountApp classes

### Cluster Spark avec Docker

- **README.md**: Spark cluster setup and applications
- **CONTENT.md**: Original PDF content in French - Installation, examples, Colab setup, MongoDB integration
- **Files**: st.sh startup script, integration examples

### TP MongoDB

- **README.md**: MongoDB Atlas, CRUD operations, aggregation, MapReduce
- **CONTENT.md**: Original PDF content in French - Complete tutorial with queries and dashboard creation
- **Files**: Database setup and manipulation examples

### TP Spark Streaming

- **README.md**: Real-time data processing with Spark Streaming and DStream
- **CONTENT.md**: Original PDF content in French - Socket streaming, word count application
- **Files**: server.py (data source), client.py (Spark consumer), Questions.txt

## How to Use This Documentation

### For English Learners / Complete Guides

👉 **Read the README.md files** in each project directory

Each README contains:

- Objectives and description
- Prerequisites and installation
- Step-by-step execution guide
- Code examples and best practices
- Troubleshooting section
- Next steps recommendations

### For French Content / PDF Equivalent

👉 **Read the CONTENT.md files** in each project directory

These files contain:

- Original PDF content converted to markdown format
- Practical exercises and assignments
- Code snippets from the original documents
- Exact questions and requirements

## File Naming Convention

| File Type  | Language       | Purpose                           |
| ---------- | -------------- | --------------------------------- |
| README.md  | English        | Comprehensive educational guide   |
| CONTENT.md | French         | PDF content converted to markdown |
| \*.py      | English/Python | Python scripts                    |
| \*.java    | English/Java   | Java classes                      |
| \*.sh      | English        | Shell scripts                     |

## Access the Documentation

### Quick Navigation

```
big_data_labs/
├── README.md (Overview)
├── lab0/
│   └── README.md (Docker Cluster)
├── lab1/
│   └── README.md (HDFS)
├── lab_spark_sql_fifa/
│   ├── README.md (Spark SQL Guide)
│   └── CONTENT.md (FIFA Queries)
├── lab3 - mapReduce/
│   ├── README.md (MapReduce Guide)
│   └── CONTENT.md (MapReduce Tutorial)
├── lab4/kafka/
│   ├── README.md (Kafka Guide)
│   └── CONTENT.md (Kafka Tutorial)
├── Cluster spark avec docker/
│   ├── README.md (Spark Cluster Guide)
│   └── CONTENT.md (Cluster Tutorial)
├── tp_mongoDB/
│   ├── README.md (MongoDB Guide)
│   └── CONTENT.md (MongoDB Tutorial)
└── tp_spark_streaming/
    ├── README.md (Spark Streaming Guide)
    └── CONTENT.md (Streaming Tutorial)
```

## Content Summary by Language

### English Documentation (README.md)

Perfect for:

- Learning objectives and concepts
- Setup and installation procedures
- Best practices and patterns
- Performance optimization
- Troubleshooting guides

### French Documentation (CONTENT.md)

Perfect for:

- Exact lab requirements from course materials
- Specific exercise questions
- Original instructor requirements
- Step-by-step tutorials with detailed explanations
- Code examples from lectures

## Recommended Learning Path

1. **Start with Lab 0** (Docker) - Get the cluster running
2. **Move to Lab 1** (HDFS) - Understand distributed file system
3. **Try Lab 3** (MapReduce) - Learn batch processing
4. **Explore Lab 4** (Kafka) - Understand streaming concepts
5. **Work with Lab Spark SQL** - SQL on Spark
6. **Deploy on Cluster** (Cluster Spark Docker) - Production setup
7. **Advanced Streaming** (Spark Streaming) - Real-time processing
8. **Data Storage** (MongoDB) - NoSQL database integration

## Finding Specific Information

### For Implementation Details

👉 Use **README.md** files with their detailed code sections

### For Exact Requirements

👉 Use **CONTENT.md** files with original exercise questions

### For Execution Commands

👉 Look in **Usage/Running** sections of README.md

### For Configuration

👉 Check both README.md (best practices) and CONTENT.md (exact configs)

## Tips

- README files are optimized for learning and understanding concepts
- CONTENT files preserve the original PDF structure for reference
- Both files are complementary - use them together for complete understanding
- All code examples are copy-paste ready
- Follow the "Next Steps" section in each README for progression

---

**Last Updated**: February 2026  
**Format**: Markdown  
**Languages**: English (README), French (CONTENT)
