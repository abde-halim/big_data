# Lab 4 - Apache Kafka

## Objective

This laboratory explores **Apache Kafka** for distributed messaging and data streaming. You will learn to:

- Produce and consume Kafka messages
- Architecture real-time systems
- Process continuous data streams
- Manage partitions and replication

## Description

Lab 4 implements a complete Kafka application with two main components:

### 1. **EventProducer.java**

Kafka producer that generates and sends events to a topic.

- Creates custom events
- Sends data to Kafka broker
- Handles asynchronous callbacks

### 2. **WordCountApp.java**

Real-time word counting application based on Kafka.

- Receives text messages
- Counts word occurrences in real-time
- Displays updated results

## Prerequisites

- Java 8+ installed
- Maven 3.6+
- Running Kafka cluster (integrated or Docker)
- Kafka broker accessible (localhost:9092 by default)

## Installation and Configuration

### Kafka Installation (optional if using Docker)

```bash
# Download Kafka
wget https://archive.apache.org/dist/kafka/3.5.2/kafka_2.13-3.5.2.tgz

# Extract
tar -xzf kafka_2.13-3.5.2.tgz
cd kafka_2.13-3.5.2

# Start ZooKeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka Broker (another terminal)
bin/kafka-server-start.sh config/server.properties
```

### Docker Setup

```bash
docker run -d --name zookeeper \
  -e ZOOKEEPER_CLIENT_PORT=2181 \
  confluentinc/cp-zookeeper:7.4.0

docker run -d --name kafka \
  -e KAFKA_BROKER_ID=1 \
  -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092 \
  -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT \
  -e KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  confluentinc/cp-kafka:7.4.0
```

## Project Structure

```
lab4/kafka/
├── README.md                   # This file
├── pom.xml                    # Maven configuration
├── src/main/java/
│   └── com/kafka/
│       ├── EventProducer.java     # Producer app
│       └── WordCountApp.java      # Consumer app
└── target/                    # Compiled files
```

## Dependencies

```xml
- kafka-clients 3.5.2 (Java 8 compatible)
- slf4j-api 1.7.36 (logging)
- slf4j-simple 1.7.36
```

## Compilation

```bash
cd lab4/kafka

# Compile
mvn clean package

# Creates: target/lab4-kafka-1.0-SNAPSHOT.jar
```

## Execution

### 1. Create a Topic

```bash
bin/kafka-topics.sh --create \
  --topic test-events \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1
```

### 2. Run the Producer

```bash
java -cp target/lab4-kafka-1.0-SNAPSHOT.jar com.kafka.EventProducer
```

### 3. Run the Consumer (different terminal)

```bash
java -cp target/lab4-kafka-1.0-SNAPSHOT.jar com.kafka.WordCountApp
```

### 4. Test with CLI

```bash
# List topics
bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# Consume messages
bin/kafka-console-consumer.sh \
  --topic test-events \
  --bootstrap-server localhost:9092 \
  --from-beginning

# Produce messages
bin/kafka-console-producer.sh \
  --topic test-events \
  --bootstrap-server localhost:9092
```

## Kafka Architecture

```
┌──────────────────────────────────────────────────────┐
│           Kafka Cluster (Brokers)                    │
│                                                      │
│  ┌─────────────────────────────────────────────┐   │
│  │  Topic: test-events                        │   │
│  │                                             │   │
│  │  Partition 0  ┌──┬──┬──┐                   │   │
│  │  ├─ Replica 0 │M0│M1│M2│                   │   │
│  │  └─ Replica 1 │M0│M1│M2│                   │   │
│  │                                             │   │
│  │  Partition 1  ┌──┬──┐                      │   │
│  │  └─ Replica 0 │M3│M4│                      │   │
│  │                                             │   │
│  │  Partition 2  ┌──┬──┬──┬──┐                │   │
│  │  └─ Replica 0 │M5│M6│M7│M8│                │   │
│  └─────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────┘
        ▲                               ▼
    Producer                        Consumer Group
   (EventProducer)           (WordCountApp)
```

## Code Examples

### EventProducer.java

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer",
    "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer",
    "org.apache.kafka.common.serialization.StringSerializer");

try (KafkaProducer<String, String> producer =
        new KafkaProducer<>(props)) {
    for (int i = 0; i < 100; i++) {
        String message = "Event " + i;
        ProducerRecord<String, String> record =
            new ProducerRecord<>("test-events",
                String.valueOf(i), message);

        producer.send(record, (metadata, exception) -> {
            if (exception == null) {
                System.out.println("Sent: " + message);
            } else {
                exception.printStackTrace();
            }
        });
    }
}
```

### WordCountApp.java

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "word-count-group");
props.put("key.deserializer",
    "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer",
    "org.apache.kafka.common.serialization.StringDeserializer");
props.put("auto.offset.reset", "earliest");

try (KafkaConsumer<String, String> consumer =
        new KafkaConsumer<>(props)) {
    consumer.subscribe(Arrays.asList("test-events"));
    Map<String, Integer> wordCounts = new HashMap<>();

    while (true) {
        ConsumerRecords<String, String> records =
            consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            String[] words = record.value().split("\\s+");
            for (String word : words) {
                wordCounts.put(word,
                    wordCounts.getOrDefault(word, 0) + 1);
            }
            System.out.println("Word counts: " + wordCounts);
        }
    }
}
```

## Key Concepts

### Topics and Partitions

- **Topic**: Category/stream of messages
- **Partition**: Distributed subset of topic, replicated

### Producers

- Send messages to topics
- Support sync and async sends
- Can specify key and value

### Consumers

- Receive topic messages
- Part of **Consumer Groups**
- One consumer per partition per group

### Offsets

- Position in partition
- Automatic or manual management

## Important Configuration

```properties
# Broker
bootstrap.servers=localhost:9092
broker.id=1

# Topic
num.partitions=3
replication.factor=1
min.insync.replicas=1

# Producer
acks=1
retries=3
batch.size=16384

# Consumer
group.id=my-group
auto.offset.reset=earliest
max.poll.records=500
```

## Practical Exercises

1. **Produce 1000 messages** and measure throughput
2. **Consume with multiple consumers** in same group
3. **Implement real-time word counter**
4. **Filter messages** by criteria
5. **Measure producer-consumer latency**
6. **Handle errors** and resilience

## Monitoring and Debugging

```bash
# Topic details
bin/kafka-topics.sh --describe \
  --topic test-events \
  --bootstrap-server localhost:9092

# List consumer groups
bin/kafka-consumer-groups.sh --list \
  --bootstrap-server localhost:9092

# Group details
bin/kafka-consumer-groups.sh --describe \
  --group word-count-group \
  --bootstrap-server localhost:9092

# Reset offsets
bin/kafka-consumer-groups.sh --reset-offsets \
  --group word-count-group \
  --topic test-events \
  --to-earliest \
  --execute \
  --bootstrap-server localhost:9092
```

## Troubleshooting

- **Connection refused**: Verify Kafka/ZooKeeper running
- **Topic not found**: Create topic first
- **Consumer lag**: Adjust `fetch.min.bytes` or `fetch.max.wait.ms`
- **Slow performance**: Increase `batch.size` and `linger.ms`

## Performance Parameters

| Parameter          | Impact             | Value             |
| ------------------ | ------------------ | ----------------- |
| batch.size         | Latency/Throughput | 16384-32768       |
| linger.ms          | Wait before send   | 0-100             |
| compression.type   | Network size       | snappy, lz4, gzip |
| num.partitions     | Parallelism        | Consumer count    |
| replication.factor | Durability         | 1-3               |

## Real-world Use Cases

- **Event Streaming**: App logs, user events
- **Messaging**: Asynchronous service communication
- **Data Pipeline**: ETL, data ingestion
- **Analytics**: Real-time data processing
- **Activity Tracking**: User action tracking

## Next Steps

- **TP Spark Streaming**: Kafka + Spark for more power
- **Lab 3**: MapReduce for batch comparison
- **MongoDB**: Store streaming results
