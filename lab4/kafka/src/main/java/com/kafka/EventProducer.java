package com.kafka;

import java.util.Properties;
import java.util.Scanner;
import org.apache.kafka.clients.producer.*;

public class EventProducer {

    public static void main(String[] args) {

        String topicName;

        if (args.length > 0) {
            topicName = args[0];
        } else {
            Scanner scanner = new Scanner(System.in);
            System.out.print("Entrer le nom du topic : ");
            topicName = scanner.nextLine();
        }

        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("acks", "all");
        props.put("retries", 0);
        props.put("batch.size", 16384);
        props.put("buffer.memory", 33554432);
        props.put("key.serializer",
                "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer",
                "org.apache.kafka.common.serialization.StringSerializer");

        Producer<String, String> producer = new KafkaProducer<>(props);

        for (int i = 0; i < 10; i++) {
            producer.send(new ProducerRecord<>(
                    topicName,
                    Integer.toString(i),
                    "Message " + i));
        }

        producer.close();
        System.out.println("Messages envoyés avec succès");
    }
}
