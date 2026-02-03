# TP: Cluster Spark avec Docker

## Introduction

Pour rappel, Spark est un moteur de calcul distribué destiné au traitement de données à grande échelle. C'est un framework complet et unifié pour le traitement et l'analyse Big Data de diverse natures (texte, streaming, graphe, etc.).

Spark peut s'exécuter en mode standalone ou bien en mode cluster manager dédié tels qu'Apache Hadoop YARN ou Apache Mesos.

## Objectif

L'objectif de ce TP est de :

- Installer un cluster Spark avec Docker
- Premier exemple
- Installer PySpark sur Colab
- Charger et manipuler des données avec Spark
- Étude de cas

## I. Installation Cluster Spark

### 1. Accéder au Master

Après le démarrage du cluster Hadoop, entrer dans le conteneur master :

```bash
docker exec -it hadoop-master bash
```

### 2. Démarrer Hadoop et Yarn

Lancer Hadoop et YARN en utilisant un script fourni appelé `start-hadoop.sh` :

```bash
./start-hadoop.sh
./start-spark.sh
```

À la fin du démarrage, vérifier si Spark et YARN ont démarré correctement. Pour ce faire :

- Vérifier à travers la commande `jps`
- Dans un navigateur, entrer l'adresse :
  - Yarn Web UI: https://localhost:8088
  - Spark web UI: https://localhost:8080

## II. Premiers Exemples sur Apache Spark

### 1. Premier Exemple Spark avec Spark-Submit

Spark-submit est un script Spark qui permet de lancer des applications sur un cluster. Il peut utiliser tous les cluster managers pris en charge par Spark via une interface uniforme.

Tester l'exemple SparkPi qui permet de calculer la valeur PI :

```bash
spark-submit \
  --class org.apache.spark.examples.SparkPi \
  --master local[*] \
  $SPARK_HOME/examples/jars/spark-examples_{version}.jar \
  100
```

**Tâche** : Rapporter le nombre PI calculé pour différentes valeurs

### 2. Application Word Count avec Spark-Shell

Les shells de Spark fournissent un moyen simple et puissant pour analyser les données de manière interactive.

On veut réaliser l'exemple WordCount en Scala :

```scala
val data=sc.textFile("hdfs://hadoop-master:9000/user/root/input/alice.txt")
val count= data.flatMap(line => line.split(" ")).map(word => (word, 1)).reduceByKey(_+_)
count.saveAsTextFile("hdfs://hadoop-master:9000/user/root/output/respark1")
```

### 3. Soumettre une Application Python

Écrire le script Python :

```python
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("yarn").appName('wordcount').getOrCreate()
data = spark.sparkContext.textFile("hdfs://hadoop-master:9000/user/root/input/alice.txt")
words = data.flatMap(lambda line: line.split(" "))
wordCounts = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a +b)
wordCounts.saveAsTextFile("hdfs://hadoop-master:9000/user/root/output/rr2")
```

Soumettre le script Python via `spark-submit` :

```bash
spark-submit script.py
```

Consulter les résultats enregistrés dans HDFS.

Sortir de bash du hadoop-master et arrêter les conteneurs :

```bash
exit
docker stop hadoop-master hadoop-slave1 hadoop-slave2
```

## Installation PySpark sur Google Colab

PySpark est une API Python pour Spark. Elle permet de manipuler les RDD et DataFrames.

Google Colab ne fournit pas Spark par défaut, nous devons donc l'installer.

### Installer Apache Spark et PySpark

Commencer d'abord par ouvrir un nouveau notebook Colab.

Exécutez les commandes suivantes dans une cellule Colab :

```bash
!sudo apt update
!apt-get install openjdk-8-jdk-headless -qq > /dev/null
# Check this site for the latest download link
# https://www.apache.org/dyn/closer.lua/spark/spark-3.2.1/spark-3.2.1bin-hadoop3.2.tgz
!wget -q https://dlcdn.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz
!tar xf spark-3.2.1-bin-hadoop3.2.tgz
!pip install -q findspark
!pip install pyspark
!pip install py4j
!pip install -q pymongo matplotlib seaborn
```

### Configurer l'Environnement

Après l'installation, nous devons configurer les variables d'environnement pour utiliser Spark :

```python
import os
import sys
import findspark
# os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
# os.environ["SPARK_HOME"] = "/content/spark-3.2.1-bin-hadoop3.2"
findspark.init()
findspark.find()
```

### Démarrer une Session Spark

```python
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
  .appName("ColabSpark") \
  .config("spark.driver.memory", "2g") \
  .getOrCreate()

print("Spark est configuré avec succès !")
```

### Premier Exemple

Vérifier la session Spark :

```python
print(spark.version)
```

Créer un DataFrame simple avec les infos suivantes :

```python
data = [(1, "Alice", 23), (2, "Bob", 30), (3, "Charlie", 29)]
columns = ["id", "nom", "age"]
df = spark.createDataFrame(data, columns)
```

Afficher le contenu du DataFrame :

```python
df.show()
```

Voici quelques opérations de base :

```python
df.printSchema() # Structure du DataFrame
df.select("nom", "age").show() # Sélection de colonnes
df.filter(df.age > 25).show() # Filtrage des données
```

## Chargement et Manipulation des Données avec Spark

Nous allons utiliser un jeu de données sur les transactions financières.

### Charger un Fichier CSV

```python
df = spark.read.csv("/content/transactions.csv", header=True, inferSchema=True)
df.show(5)
```

### Afficher le Schéma des Données

```python
df.printSchema()
```

### Filtrer les Transactions Supérieures à 1000

```python
df.filter(df["Transaction Amount"] > 1000).show()
```

### Calculer le Montant Total des Transactions par Type

```python
df.groupBy("Transaction Type").sum("Transaction Amount").show()
```

### Trier les Transactions par Montant Décroissant

```python
df.orderBy(df["Transaction Amount"].desc()).show(5)
```

## Étude de Cas : Intégration de Spark avec MongoDB Atlas

Nous allons maintenant connecter Spark à MongoDB Atlas pour analyser les transactions directement depuis la base de données.

### Installer le Connecteur MongoDB Spark

```bash
!pip install pymongo
```

### Configurer la Connexion à MongoDB Atlas

Ajoutez vos identifiants MongoDB Atlas :

```python
mongo_uri = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/bankdb.transactions?retryWrites=true&w=majority"
spark = SparkSession.builder \
  .appName("MongoDBIntegration") \
  .config("spark.mongodb.input.uri", mongo_uri) \
  .config("spark.mongodb.output.uri", mongo_uri) \
  .getOrCreate()
```

### Charger les Transactions depuis MongoDB

```python
df_mongo = spark.read.format("mongo").option("uri", mongo_uri).load()
df_mongo.show(5)
```

### Effectuer des Analyses sur MongoDB avec Spark

Calculer le montant moyen des transactions :

```python
df_mongo.groupBy("Transaction Type").avg("Transaction Amount").show()
```

Trouver les comptes ayant effectué plus de 5 transactions :

```python
df_mongo.groupBy("Sender Account ID").count().filter("count > 5").show()
```

### Utiliser Spark SQL

Spark permet aussi d'écrire des requêtes SQL sur les DataFrames.

Enregistrer un DataFrame comme table temporaire :

```python
df.createOrReplaceTempView("transactions")
```

Exécuter une requête SQL avec Spark :

```python
df.createOrReplaceTempView("transactions")
result = spark.sql("SELECT `Transaction Type`, SUM(`Transaction Amount`) as Total FROM transactions GROUP BY `Transaction Type`")
result.show()
```

### Visualiser les Transactions par Type

Nous allons afficher le total des transactions par type sous forme de graphique barplot avec Seaborn.

Préparer les données :

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Agréger les transactions par type
df_grouped = df.groupBy("Transaction Type").sum("Transaction Amount").toPandas()
# Renommer les colonnes
df_grouped.columns = ["Transaction Type", "Total Amount"]
df_grouped.sort_values(by="Total Amount", ascending=False, inplace=True)
```

Visualiser avec Seaborn :

```python
plt.figure(figsize=(10, 5))
sns.barplot(data=df_grouped, x="Transaction Type", y="Total Amount", palette="coolwarm")
plt.title("Montant Total des Transactions par Type")
plt.xlabel("Type de Transaction")
plt.ylabel("Montant Total (€)")
plt.xticks(rotation=45)
plt.show()
```

### Distribution des Montants des Transactions

Nous allons afficher la distribution des montants avec un histogramme.

Convertir en Pandas :

```python
df_pandas = df.select("Transaction Amount").toPandas()
```

Tracer un Histogramme :

```python
plt.figure(figsize=(10, 5))
sns.histplot(df_pandas["Transaction Amount"], bins=30, kde=True, color="blue")
plt.title("Distribution des Montants des Transactions")
plt.xlabel("Montant (€)")
plt.ylabel("Nombre de Transactions")
plt.show()
```

### Comparaison des Transactions Réussies vs Échouées

Nous allons comparer les transactions réussies et échouées avec un countplot.

Préparer les données :

```python
df_status = df.groupBy("Transaction Status").count().toPandas()
df_status.columns = ["Transaction Status", "Count"]
```

Tracer le graphique :

```python
plt.figure(figsize=(7, 5))
sns.barplot(data=df_status, x="Transaction Status", y="Count", palette="pastel")
plt.title("Nombre de Transactions Réussies vs Échouées")
plt.xlabel("Statut de la Transaction")
plt.ylabel("Nombre de Transactions")
plt.show()
```
