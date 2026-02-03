from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Création ou récupération du SparkContext
sc = SparkContext.getOrCreate()

# Création du StreamingContext avec un batch de 5 secondes
ssc = StreamingContext(sc, 5)



# Lecture des données sous forme de DStream
lines = ssc.socketTextStream("127.0.0.1", 9999)


# Découpage des lignes en mots
words = lines.flatMap(lambda line: line.split(" "))

# Création de paires (mot, 1)
pairs = words.map(lambda word: (word, 1))

# Agrégation des occurrences par mot
counts = pairs.reduceByKey(lambda a, b: a + b)


# Affichage des résultats dans la console
counts.pprint()

# Démarrage du streaming
ssc.start()

# Laisser tourner pendant 30 secondes
ssc.awaitTerminationOrTimeout(30)

# Arrêt propre du streaming (sans arrêter SparkContext)
ssc.stop(stopSparkContext=False)

# ssc.stop(stopSparkContext=True, stopGraceFully=True)
