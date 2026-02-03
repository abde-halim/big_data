# Lab 4: Initiation à MongoDB

## Objectif

L'objectif de cet atelier est de :

- Créer un compte MongoDB Atlas et déployer un cluster
- Se connecter à la base de données avec MongoDB Compass ou MongoDB Shell
- Créer une collection et insérer des documents
- Exécuter des requêtes pour récupérer des données
- Mettre à jour et supprimer des documents
- Importation des fichiers
- Exemple Map Reduce

## Introduction

MongoDB est un SGBD NoSQL orienté documents. Il est particulièrement apprécié pour sa capacité à passer en mode distribué pour répartir le stockage et les traitements de données. MongoDB fournit une API en Python et autres langages pour pouvoir manipuler programmatiquement les données de la base.

## 1. Création d'un Compte et Déploiement d'un Cluster

Pour faciliter l'utilisation de MongoDB, nous allons exploiter MongoDB Atlas. Il s'agit d'un service cloud entièrement géré qui simplifie le déploiement, l'évolutivité et la gestion des bases de données MongoDB.

**Étapes :**

1. Allez sur MongoDB Atlas
2. Inscrivez-vous ou connectez-vous (à l'aide d'un compte Gmail par exemple)
3. Cliquez sur "Créer un cluster" (Choisissez un cluster gratuit si disponible)
4. Sélectionnez "M0 Sandbox" et choisissez un fournisseur de cloud et une région
5. Configurez votre base de données (Nom du cluster par défaut ou personnalisé)
6. Cliquez sur "Créer un cluster" (cela peut prendre quelques minutes)
7. Créer un utilisateur avec un mot de passe (garder les deux pour un usage ultérieur)

MongoDB fonctionne en mode client/serveur :

- **Le serveur** est en attente
- **Le client** peut être :
  - l'interpréteur de commande (shell) `mongo`
  - une application UI pour simplifier l'usage telle que Compass, RoboMongo ou bien Studio3T
  - Un programme développé
  - l'interface MongoDB Atlas

## 2. Connexion à MongoDB Atlas

- Une fois le cluster créé, allez dans "Database" > "Connect"
- Choisissez "MongoDB Compass" (interface graphique) ou "MongoDB Shell" (ligne de commande)
- Copiez l'URI de connexion et utilisez-le pour vous connecter (n'oublier pas de copier votre mot de passe)

Exemple :

```
mongodb+srv://yalami:<db_password>@cluster0.apxc2.mongodb.net/
```

## 3. Création d'une Base de Données et d'une Collection

Dans MongoDB Shell :

Pour se placer dans une base :

```javascript
use <nombase>
```

Créer une collection nommée `users` :

```javascript
db.createCollection("users");
```

Lister les collections de la base :

```javascript
show collections
```

Insérer un document JSON dans la collection `users` :

```javascript
db.users.insertOne({ name: "Mohamed", age: 20, city: "Casablanca" });
```

Insérer maintenant plusieurs tuples dans la collection `users` :

```javascript
db.users.insertMany([
  { name: "Alice", age: 25, city: "Paris" },
  { name: "Bob", age: 30, city: "Lyon" },
  { name: "Charlie", age: 28, city: "Marseille" },
]);
```

## 4. Requêtes pour Récupérer des Données

L'objet (JavaScript) implicite `db`, permet de soumettre des demandes d'exécution de certaines méthodes.

Afficher tous les utilisateurs de la collection :

```javascript
db.users.find();
```

Insérer un autre document avec les informations de votre choix :

```javascript
// À compléter par vos données
```

Compter le nombre de documents dans la collection :

```javascript
db.users.count();
```

Récupérer un utilisateur spécifique :

```javascript
db.users.findOne({ name: "Alice" });
```

Filtrer les utilisateurs par âge (age > 20) :

```javascript
db.users.find({ age: { $gt: 20 } });
```

Modifier l'âge d'un utilisateur :

```javascript
db.users.updateOne({ name: "Alice" }, { $set: { age: 26 } });
```

Supprimer un utilisateur :

```javascript
db.users.deleteOne({ name: "Charlie" });
```

Supprimer une collection :

```javascript
db.users.drop();
```

## 5. Importation de Fichier dans une Collection

L'utilitaire d'import de MongoDB prend en entrée un tableau JSON contenant la liste des objets à insérer. Dans notre cas, nous allons utiliser des données sur les transactions bancaires.

Cet ensemble de données contient 1 000 transactions bancaires synthétiques, incluant divers types de transactions tels que les virements, les retraits et les dépôts. Chaque enregistrement contient des attributs détaillés tels que l'identifiant de la transaction, les identifiants des comptes émetteur et récepteur, le montant de la transaction, l'horodatage, le statut de la transaction (réussite ou échec), l'indicateur de fraude, la géolocalisation, l'appareil utilisé, l'identifiant de la tranche réseau, la latence, la bande passante de la tranche et le code PIN associé.

**Procédure :**

Télécharger le fichier `transactions.json`

Après avoir créé la base de données appelée « BankDB » et la collection « transactions », importer le fichier dans la collection :

**Méthode 1 : depuis l'interface graphique**

**Méthode 2 : en utilisant la commande `mongoimport`**

Ceci suppose l'installation de mongoshell sur votre machine :

```bash
mongoimport --uri "mongodb+srv://<username>:<password>@cluster0.mongodb.net/BankDB" \
    --collection transactions \
    --file transactions.json \
    --jsonArray
```

Dans MongoDB Shell ou MongoDB Compass, connectez-vous à la base de données BankDB :

```javascript
use BankDB
db.transactions.find().pretty()
```

Afficher les informations sur une transaction pour comprendre la structure

Questions :

- Combien y a-t-il de transactions dans la base de données ?
- Trouver toutes les transactions échouées ("Transaction Status": "Failed")
- Vérifier les transactions suspectes ("Fraud Flag" : "True")

## 6. Requêtes d'Agrégation

Nombre total de transactions par statut :

```javascript
db.transactions.aggregate([
  { $group: { _id: "$Transaction Status", total: { $count: {} } } },
]);
```

Montant moyen des transactions par type :

```javascript
db.transactions.aggregate([
  {
    $group: {
      _id: "$Transaction Type",
      avgAmount: { $avg: "$Transaction Amount" },
    },
  },
]);
```

Top 5 des comptes qui envoient le plus d'argent :

```javascript
db.transactions.aggregate([
  {
    $group: {
      _id: "$Sender Account ID",
      totalSent: { $sum: "$Transaction Amount" },
    },
  },
  { $sort: { totalSent: -1 } },
  { $limit: 5 },
]);
```

Calculer le montant total des transactions par type :

```javascript
db.transactions.aggregate([
  {
    $group: {
      _id: "$Transaction Type",
      total: { $sum: "$Transaction Amount" },
    },
  },
]);
```

Vérifier la latence moyenne par "Network Slice ID" :

```javascript
db.transactions.aggregate([
  {
    $group: { _id: "$Network Slice ID", avgLatency: { $avg: "$Latency (ms)" } },
  },
]);
```

Transactions échouées par appareil utilisé :

```javascript
db.transactions.aggregate([
  { $match: { "Transaction Status": "Failed" } },
  { $group: { _id: "$Device Used", totalFailed: { $count: {} } } },
]);
```

Trouver les transactions suspectes (fraude et montant élevé > 1000) :

```javascript
db.transactions.find({
  "Fraud Flag": "True",
  "Transaction Amount": { $gt: 1000 },
});
```

Combien transactions ont un montant entre 100 et 200 ?

## 7. Indicateurs Clés (KPI)

On veut maintenant mettre en place plusieurs indicateurs clés (KPI) pour surveiller l'activité financière, détecter les fraudes et analyser la performance des transactions.

Afficher nombre total des transactions :

```javascript
db.transactions.countDocuments({});
```

Afficher Montant total des transactions :

```javascript
db.transactions.aggregate([
  { $group: { _id: null, totalAmount: { $sum: "$Transaction Amount" } } },
]);
```

Afficher Taux d'échec des transactions (%) :

```javascript
db.transactions.aggregate([
  { $group: { _id: "$Transaction Status", count: { $count: {} } } },
]);
```

Afficher le Nombre de transactions frauduleuses :

```javascript
db.transactions.countDocuments({ "Fraud Flag": "True" });
```

## 8. Manipuler MapReduce sur la Collection Transactions

Une fois connecté à MongoDB Atlas, vous pouvez utiliser MapReduce pour effectuer des analyses. L'exemple suivant montre comment utiliser MapReduce pour calculer le montant total des transactions par type de transaction (par exemple, "Dépôt", "Transfert", etc.).

**Procédure :**

Créer un nouveau notebook sur Colab

Exécutez la cellule suivante dans Google Colab pour installer PyMongo :

```bash
!pip install pymongo
```

Se connecter à MongoDB Atlas :

```python
from pymongo import MongoClient

# Remplacez par votre URI MongoDB Atlas
uri = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/bankdb?retryWrites=true&w=majority"
client = MongoClient(uri)

# Accéder à la base de données
db = client["bankdb"]
transactions_collection = db["transactions"]

# Vérification de la connexion
print("Connexion à MongoDB Atlas réussie!")
```

Étant donné que `map_reduce()` est obsolète, utilisez le framework d'agrégation de MongoDB pour additionner les montants des transactions par type de transaction :

```python
# Créer un pipeline d'Aggregation pour calculer le montant total transaction par type
pipeline = [
    {"$group": {"_id": "$Transaction Type", "totalAmount": {"$sum": "$Transaction Amount"}}}
]

# Exécuter la requête d'agrégation
result = transactions_collection.aggregate(pipeline)

# Afficher les résultats
for doc in result:
    print(f"Transaction Type: {doc['_id']}, Total Amount: {doc['totalAmount']}")
```

Réaliser d'autres opérations d'agrégation de votre choix

## 9. Dashboard avec MongoDB Atlas

MongoDB Atlas propose un outil appelé **MongoDB Charts**, qui permet de visualiser et d'analyser les données directement depuis votre base de données sans besoin d'exportation. Cet outil est idéal pour créer des tableaux de bord interactifs basés sur vos données en temps réel.

### Activer MongoDB Charts

1. Connectez-vous à MongoDB Atlas (https://www.mongodb.com/atlas)
2. Sélectionnez votre cluster
3. Cliquez sur "Charts" dans le menu de gauche
4. Créez un nouveau tableau de bord

### Connecter une Source de Données

1. Cliquez sur "Add Data Source"
2. Sélectionnez votre base de données (bankdb) et votre collection (transactions)
3. Configurez les autorisations si nécessaire

### Créer des Visualisations

1. Sélectionnez un type de graphique (barres, lignes, camembert, etc.)
2. Définissez les axes :
   - X-axis : "Transaction Type"
   - Y-axis : "Transaction Amount" (somme des montants)
3. Appliquez des filtres si nécessaire (ex. afficher uniquement les transactions réussies)
4. Enregistrez et ajoutez le graphique à votre tableau de bord

### Personnaliser et Partager

- Ajoutez plusieurs graphiques à votre tableau de bord
- Personnalisez les couleurs et les titres
- Partagez le tableau avec d'autres utilisateurs via un lien
