# TP : Spark Streaming

## Objectifs

Ce TP a pour objectif de :

- S'initier au traitement de données en temps réel avec Apache Spark DStream
- Créer un flux de données en temps réel
- Appliquer des transformations simples

## Environnement de Travail

- Google Colab, Python 3, PySpark

## Exercice 1 : Spark Streaming avec DStream

On souhaite analyser en temps réel des messages texte envoyés via un socket et calculer le nombre d'occurrences de chaque mot toutes les 5 secondes.

### Travail Demandé

1. Installer PySpark
2. Créer un serveur socket simulant un flux de données
3. Créer un StreamingContext
4. Lire les données sous forme de DStream
5. Appliquer un WordCount streaming
6. Afficher les résultats dans la console

### Installation PySpark

```python
!pip install pyspark
```

### Serveur Socket Simulant un Flux

```python
import socket, time, threading

def start_socket_server():
    host = "localhost"
    port = 9999
    s = socket.socket()
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()

    messages = [
        "spark streaming dstream",
        "spark spark streaming",
        "big data spark"
    ]

    while True:
        for msg in messages:
            conn.send((msg + "\n").encode())
            time.sleep(2)

threading.Thread(target=start_socket_server, daemon=True).start()
```

### Code Spark Streaming

```python
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext.getOrCreate()
ssc = StreamingContext(sc, 5)

lines = ssc.socketTextStream("localhost", 9999)
words = lines.flatMap(lambda line: line.split(" "))
pairs = words.map(lambda w: (w, 1))
counts = pairs.reduceByKey(lambda a, b: a + b)

counts.pprint()

ssc.start()
ssc.awaitTerminationOrTimeout(30)
ssc.stop(stopSparkContext=False)
```

## Questions

1. Créer des sections pour chaque partie du travail demandé
2. Chaque section doit être commentée
3. Modifier le code afin que la lecture aléatoire soit faite depuis un fichier
4. Qu'est-ce qu'un micro-batch dans DStream ?
5. Sur quelle structure repose un DStream ?
6. Quelle est la durée du batch utilisée ?

## Concepts Clés

### DStream (Discretized Stream)

Un DStream représente un flux continu de données, qui est divisé en petits batches de données appelés RDDs (Resilient Distributed Datasets).

### Micro-batch

Un micro-batch est un petit ensemble de données traités ensemble à chaque intervalle de temps spécifié (par défaut 500 ms, dans notre cas 5 secondes).

### Transformations Stateless

Les transformations qui ne dépendent pas de données précédentes :

- `flatMap`
- `map`
- `filter`

### Transformations Stateful

Les transformations qui maintiennent l'état à travers les micro-batches :

- `reduceByKey`
- `updateStateByKey`
- `window`

### Windowing

Permet de traiter les données sur une fenêtre temporelle glissante.

Exemple :

```python
windowedCounts = pairs.reduceByKeyAndWindow(lambda a, b: a+b, 10, 5)
# Fenêtre de 10 secondes, slide de 5 secondes
```

## Exercices Complémentaires

### 1. Filtrage des Mots Vides

```python
stopwords = {"the", "a", "an", "and", "or", "is", "are"}
filtered_words = words.filter(lambda w: w.lower() not in stopwords)
pairs = filtered_words.map(lambda w: (w, 1))
```

### 2. Calcul de Statistiques

```python
word_lengths = words.map(lambda w: len(w))
word_lengths.foreachRDD(lambda rdd: print("Statistiques des longueurs:", rdd.stats()))
```

### 3. Fenêtre Temporelle

```python
windowed_counts = counts.reduceByKeyAndWindow(lambda a, b: a+b, 30, 10)
# Fenêtre de 30 secondes, slide de 10 secondes
```

### 4. Stockage des Résultats

```python
def save_results(rdd):
    if not rdd.isEmpty():
        rdd.saveAsTextFile(f"/output/spark-streaming-{int(time.time())}")

counts.foreachRDD(save_results)
```

### 5. Intégration Kafka

Si vous disposez d'une source Kafka :

```python
from pyspark.streaming.kafka import KafkaUtils

kafkaStream = KafkaUtils.createStream(
    ssc, "localhost:2181", "spark-streaming-consumer", {"your-topic": 1}
)
```

## Notes

- Tous les calculs sont fait sur les RDDs (Resilient Distributed Datasets)
- Les transformations sont lazy (évaluées uniquement à l'affichage ou sauvegarde)
- Les actions forcent l'évaluation : `pprint()`, `saveAsTextFile()`, `foreachRDD()`
