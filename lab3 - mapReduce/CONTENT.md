# Lab3: Programmation avec l'API MapReduce

## Objectif

L'objectif de ce TP est de :

- S'initier à la programmation avec l'API MapReduce
- Implémenter l'exemple WordCount en Java
- Exécuter MapReduce en Python avec Hadoop Streaming

## I. Démarrer le Cluster Hadoop

### 1. Démarrage des Conteneurs

Démarrer le cluster Hadoop créé précédemment :

```bash
docker start hadoop-master hadoop-slave1 hadoop-slave2
```

### 2. Accéder au Master

Entrer dans le conteneur master pour commencer à l'utiliser :

```bash
docker exec -it hadoop-master bash
```

### 3. Démarrer Hadoop et YARN

Lancer Hadoop et YARN en utilisant un script fourni appelé `start-hadoop.sh` :

```bash
./start-hadoop.sh
```

À la fin du démarrage, vérifier si Hadoop et YARN ont démarré correctement. Pour ce faire :

- Resource Manager Web UI: http://localhost:8088
- HDFS Web UI: http://localhost:9870
- Utiliser la commande shell `jps` pour vérifier si les processus en relation sont en cours d'exécution

## II. Programmation avec l'API MapReduce

L'objectif de ce TP est de simuler l'exemple WordCount vu dans le cours. Pour rappel, le job à créer permet de compter le nombre d'occurrences de chaque mot présent dans un fichier texte. Ce traitement est réalisé en deux phases principales :

- **Phase de Mapping** : le texte est découpé en mots. Pour chaque mot identifié, le programme génère une paire clé/valeur sous la forme (mot, 1), indiquant que ce mot est apparu une fois.
- **Phase de Reducing** : les paires issues du mapping sont regroupées par mot (clé). Le réducteur applique une fonction d'agrégation (addition) sur toutes les valeurs associées à chaque mot, ce qui permet d'obtenir le nombre total d'occurrences du mot dans le document.

Dans cette partie, nous allons développer quelques JAR pour la manipulation des fichiers avec l'API MAPREDUCE.

### 1. Installation de l'Environnement de Développement

**Outils et environnement dont on aura besoin :**

- Visual Studio Code (ou tout autre IDE de votre choix)
- Java Version 1.8
- Unix-like ou Unix-based Systems

Créer un projet Maven (no archtype) dans VSCode (ajouter les extensions nécessaires : Maven for Java et Extension Pack for Java) :

- Choisir no archetype
- GroupId : `edu.ismagi.hadoop.mapreduce`
- ArtifactId : `lab3_mapreduce`
- Créer un répertoire `BigdataLabs` où vous allez mettre votre projet `lab3_mapreduce`
- Ajouter les dépendances au fichier `pom.xml`

```xml
<properties>
    <maven.compiler.source>1.8</maven.compiler.source>
    <maven.compiler.target>1.8</maven.compiler.target>
</properties>

<dependencies>
    <dependency>
        <groupId>org.apache.hadoop</groupId>
        <artifactId>hadoop-hdfs</artifactId>
        <version>3.2.0</version>
    </dependency>
    <dependency>
        <groupId>org.apache.hadoop</groupId>
        <artifactId>hadoop-common</artifactId>
        <version>3.2.0</version>
    </dependency>
    <dependency>
        <groupId>org.apache.hadoop</groupId>
        <artifactId>hadoop-mapreduce-client-core</artifactId>
        <version>3.2.0</version>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.8.1</version>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-jar-plugin</artifactId>
            <version>3.2.2</version>
            <configuration>
                <archive>
                    <manifest>
                        <mainClass>edu.ismagi.hadoop.mapreduce.MainJob</mainClass>
                    </manifest>
                </archive>
                <finalName>mapreduce-app</finalName>
            </configuration>
        </plugin>
    </plugins>
</build>
```

### 2. Classe Mapper

Créer une première classe Mapper :

```java
import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;

public class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable> {
    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

    public void map(Object key, Text value, Context context)
            throws IOException, InterruptedException {
        System.out.println(key.toString());
        StringTokenizer itr = new StringTokenizer(value.toString());
        while (itr.hasMoreTokens()) {
            word.set(itr.nextToken());
            context.write(word, one);
        }
    }
}
```

### 3. Classe Reducer

Créer la classe Reducer :

```java
import java.io.IOException;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Reducer;

public class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values, Context context)
            throws IOException, InterruptedException {
        int sum = 0;
        for (IntWritable val : values) {
            sum += val.get();
        }
        result.set(sum);
        context.write(key, result);
    }
}
```

### 4. Classe Principale

Créer la classe qui permettra de lancer le job :

```java
import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCount {
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");

        // Classe principale
        job.setJarByClass(WordCount.class);

        // Classe qui fait le map
        job.setMapperClass(TokenizerMapper.class);

        // Classe qui fait le shuffling et le reduce
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        // Spécifier le fichier d'entrée
        FileInputFormat.addInputPath(job, new Path(args[0]));

        // Spécifier le fichier contenant le résultat
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

### 5. Créer le JAR

Créer un fichier JAR que vous allez nommer `WordCount.jar` :

```bash
mvn clean package
```

Copier le JAR créé vers le dossier de partage `/hadoop_project`

Sur l'invité de commande shell de votre container, lancer la commande :

```bash
hadoop jar /shared_volume/WordCount.jar inputfile outputfolder
```

## MapReduce avec Python

L'objectif est d'implémenter l'exemple WordCount à base de MapReduce en Python et de l'utilitaire Hadoop Streaming.

### Mapper Python

Écrire le mapper qui implémente la logique map. Il lira les données de STDIN et divisera les lignes en mots, et générera une sortie de chaque mot avec une occurrence égale à 1 :

```python
#!/usr/bin/env python
import sys

# input comes from standard input STDIN
for line in sys.stdin:
    line = line.strip()  # remove leading and trailing whitespaces
    words = line.split()  # split the line into words and returns as a list
    for word in words:
        # write the results to standard output STDOUT
        print('%s\t%s' % (word, 1))  # print the results
```

Vous pouvez tester le mapper.py sur votre machine :

```bash
cat alice.txt | python mapper.py
```

### Reducer Python

Écrire le fichier reducer.py qui implémente la logique reduce. Il lira la sortie de mapper.py à partir de l'entrée standard et agrégera l'occurrence de chaque mot et écrira la sortie finale sur STDOUT :

```python
#!/usr/bin/env python
from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None

for line in sys.stdin:
    line = line.strip()  # remove leading and trailing whitespace
    # splitting the data on the basis of tab provided in mapper.py
    word, count = line.split('\t', 1)

    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:  # ignore/discard this line if count is not a number
        continue

    # Hadoop sorts map output by key (word) before it is passed to the reducer
    if current_word == word:
        current_count += count
    else:
        if current_word:
            # write result to STDOUT
            print('%s \t %s' % (current_word, current_count))
        current_count = count
        current_word = word

# output the last word
if current_word == word:
    print('%s\t%s' % (current_word, current_count))
```

### Vérifier le Reducer

Vérifier si le reducer fonctionne correctement :

```bash
cat alice.txt | python mapper.py | sort -k1,1 | python reducer.py
```

### Exécuter avec Hadoop Streaming

Pour exécuter le mapper.py et reducer.py, ouvrir le terminal du container master.

Localiser le fichier JAR de l'utilitaire Hadoop Streaming :

```bash
find / -name 'hadoop-streaming*.jar'
```

Le chemin devrait ressembler à `/opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar`

Finalement, exécuter le programme Map/Reduce avec la commande suivante :

```bash
hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
  -files chemin/mapper.py,chemin/reducer.py \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input chemin/inputfile \
  -output chemin/outputfolder
```

### Vérifier les Résultats

Vérifier les résultats de l'exécution sur HDFS

### Initialiser Git et Github

À chaque nouveau Lab :

```bash
git add lab2
git commit -m "Ajout du lab2 : …"
git push
```

Sortir de bash du hadoop-master et arrêter les conteneurs :

```bash
exit
docker stop hadoop-master hadoop-slave1 hadoop-slave2
```

## Exercice Ouvert

- Choisir un jeu de données de votre choix (calls.txt ou bien purchases.txt)
- Définir une problématique d'analyse pertinente (ex : identifier les produits les plus vendus)
- Charger le fichier sur HDFS
- Développer le job MapReduce
- Analyser les résultats
