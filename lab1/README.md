# Lab 1 - Hadoop HDFS Operations

## Objective

This laboratory aims to master the basic operations of the Hadoop Distributed File System (HDFS). You will learn to:

- Read and write files from/to HDFS
- Interact with the distributed file system
- Understand Java APIs for Hadoop

## Description

Lab 1 contains three main Java applications for working with HDFS:

### 1. **ReadHDFS.java** - Reading HDFS Files

Demonstration of reading files stored in HDFS with path and stream handling.

### 2. **WriteHDFS.java** - Writing HDFS Files

Creating and writing data to HDFS, illustrating persistent distributed data storage.

### 3. **HadoopFileStatus.java** - Inspecting the File System

Consulting HDFS metadata: permissions, size, replication, owner, etc.

## Prerequisites

- Java 8+ installed
- Maven 3.6+
- Running Hadoop cluster (Lab 0)
- HDFS access rights

## Dependencies

```xml
- hadoop-hdfs 3.2.0
- hadoop-common 3.2.0
- hadoop-mapreduce-client-core 3.2.0
```

## Compilation

```bash
cd lab1
mvn clean compile
```

## Execution

### 1. Compile the project

```bash
mvn clean package
```

### 2. Run Java classes

```bash
# Read HDFS
java -cp target/lab1-1.0-SNAPSHOT.jar edu.supmti.hadoop.ReadHDFS

# Write HDFS
java -cp target/lab1-1.0-SNAPSHOT.jar edu.supmti.hadoop.WriteHDFS

# Inspect file system
java -cp target/lab1-1.0-SNAPSHOT.jar edu.supmti.hadoop.HadoopFileStatus
```

## Project Structure

```
lab1/
├── pom.xml                    # Maven configuration
├── src/
│   ├── main/java/
│   │   └── edu/supmti/hadoop/
│   │       ├── ReadHDFS.java          # Read from HDFS
│   │       ├── WriteHDFS.java         # Write to HDFS
│   │       └── HadoopFileStatus.java  # File metadata
│   └── test/
└── target/                    # Compiled files
```

## Key Concepts

- **Replication Factor**: Default 3 (configurable)
- **Block Size**: Size of distributed data blocks
- **NameNode**: Manages namespace and file system
- **DataNodes**: Store actual data
- **HDFS API**: FileSystem, FSDataInputStream, FSDataOutputStream

## HDFS Configuration

Important connection points:

- **NameNode**: hdfs://localhost:9000
- **Web UI**: http://localhost:9870
- **Configuration Files**: core-site.xml, hdfs-site.xml

## Useful HDFS Commands

```bash
# List contents
hdfs dfs -ls /

# Create directory
hdfs dfs -mkdir /my_directory

# Copy local to HDFS
hdfs dfs -put local_file.txt /

# Copy from HDFS to local
hdfs dfs -get /my_file.txt

# Delete file
hdfs dfs -rm /my_file.txt

# Check space used
hdfs dfs -du -sh /
```

## Practical Exercises

1. **Create and write** a text file to HDFS
2. **Read the file** from HDFS and display content
3. **Inspect metadata** (size, replication, owner)
4. **Write multiple times** to verify replication factor
5. **Create directory hierarchy** and store files

## Troubleshooting

- **Connection refused**: Check Hadoop is running
- **FileNotFoundException**: Verify file path in HDFS
- **Permission denied**: Check HDFS permissions

## Next Steps

After mastering HDFS, proceed to:

- **Lab 3**: MapReduce - Distributed data processing
- **Lab 4**: Kafka - Real-time data streaming
