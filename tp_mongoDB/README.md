# TP MongoDB

## Objective

This laboratory explores **MongoDB**, a NoSQL document-oriented database. You will learn to:

- Model data in MongoDB
- Perform CRUD operations (Create, Read, Update, Delete)
- Write complex queries with aggregation
- Manage indexes and performance
- Create interactive dashboards

## Description

This project provides practical exploration of MongoDB with:

- MongoDB Atlas account and cluster setup
- Collection and document manipulation
- CRUD operations
- Advanced aggregation queries
- Index management and performance optimization

## Prerequisites

- MongoDB 4.0+ running
- MongoDB client (mongosh or mongo CLI)
- Python 3.7+ (for PyMongo if used)
- Optional: Node.js (for MongoDB driver)

## Installation

### MongoDB Installation

#### Linux (Ubuntu/Debian)

```bash
# Add GPG keys
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Install
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start service
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### macOS

```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

#### Docker

```bash
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo:6.0
```

### Python Client Installation

```bash
pip install pymongo
```

## Project Structure

```
tp_mongoDB/
├── README.md                    # This file
├── CONTENT.md                   # Original PDF content (French)
└── scripts/                     # Sample scripts
    ├── insert_data.py          # Data insertion
    ├── query_data.py           # Query examples
    ├── aggregation.py          # Aggregation pipeline
    └── index_performance.py    # Index management
```

## Fundamental Concepts

### Documents

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "addresses": [
    { "street": "123 Main St", "city": "Boston" }
  ],
  "createdAt": ISODate("2024-01-15")
}
```

### Collections

Similar to tables but with flexible schemas.

### Databases

Container for collections.

## CRUD Operations

### CREATE - Insertion

```javascript
// Single document
db.users.insertOne({
  name: "Alice",
  email: "alice@example.com",
  age: 28,
});

// Multiple documents
db.users.insertMany([
  { name: "Bob", email: "bob@example.com" },
  { name: "Carol", email: "carol@example.com" },
]);
```

### READ - Querying

```javascript
// All documents
db.users.find();

// With filters
db.users.find({ age: { $gt: 25 } });
db.users.find({ name: "Alice" });
db.users.find({ email: { $regex: "@example" } });

// Projection (columns)
db.users.find({}, { name: 1, email: 1, age: 0 });

// Sort and limit
db.users.find().sort({ age: -1 }).limit(10);

// Count
db.users.countDocuments({ age: { $gte: 25 } });
```

### UPDATE - Modification

```javascript
// Single document
db.users.updateOne({ name: "Alice" }, { $set: { age: 29 } });

// Multiple documents
db.users.updateMany({ age: { $lt: 25 } }, { $set: { status: "young" } });

// Increment
db.users.updateOne({ name: "Bob" }, { $inc: { age: 1 } });

// Array push
db.users.updateOne({ name: "Bob" }, { $push: { hobbies: "reading" } });
```

### DELETE - Removal

```javascript
// Single document
db.users.deleteOne({ name: "Alice" });

// Multiple documents
db.users.deleteMany({ age: { $lt: 18 } });

// All (caution!)
db.users.deleteMany({});
```

## Aggregation

### Aggregation Pipeline

```javascript
db.users.aggregate([
  { $match: { age: { $gte: 25 } } },
  { $group: { _id: "$city", count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 10 },
]);
```

### Common Stages

| Stage      | Description         |
| ---------- | ------------------- |
| `$match`   | Filter (like WHERE) |
| `$group`   | Group and aggregate |
| `$sort`    | Sort                |
| `$limit`   | Limit results       |
| `$project` | Projection          |
| `$lookup`  | Join                |
| `$unwind`  | Denormalize arrays  |
| `$facet`   | Multiple facets     |

### Aggregation Operators

```javascript
{
  $group: {
    _id: "$category",
    total: { $sum: "$price" },
    average: { $avg: "$price" },
    max: { $max: "$price" },
    min: { $min: "$price" },
    count: { $sum: 1 },
    items: { $push: "$name" }
  }
}
```

## Indexing

### Create Indexes

```javascript
// Simple index
db.users.createIndex({ email: 1 });

// Compound index
db.users.createIndex({ age: 1, city: 1 });

// Text index
db.users.createIndex({ bio: "text" });

// Unique index
db.users.createIndex({ email: 1 }, { unique: true });

// TTL index (auto-delete)
db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 3600 });
```

### Performance Analysis

```javascript
// Execution plan
db.users.find({ age: 25 }).explain("executionStats");

// List indexes
db.users.getIndexes();

// Drop index
db.users.dropIndex({ email: 1 });
```

## Python with PyMongo

### Connection and Setup

```python
from pymongo import MongoClient

# Connect
client = MongoClient("mongodb://localhost:27017")
db = client["myapp"]
users = db["users"]
```

### CRUD in Python

```python
# Insert
users.insert_one({
    "name": "Alice",
    "email": "alice@example.com",
    "age": 28
})

# Query
user = users.find_one({ "name": "Alice" })

# Update
users.update_one(
    { "name": "Alice" },
    { "$set": { "age": 29 } }
)

# Delete
users.delete_one({ "name": "Alice" })

# Close
client.close()
```

### Aggregation in Python

```python
results = users.aggregate([
    { "$match": { "age": { "$gte": 25 } } },
    { "$group": { "_id": "$city", "count": { "$sum": 1 } } }
])

for doc in results:
    print(doc)
```

## Practical Exercises

### 1. Create and Populate

```javascript
db.products.insertMany([
  { name: "Laptop", category: "Electronics", price: 999, stock: 5 },
  { name: "Mouse", category: "Electronics", price: 25, stock: 50 },
  { name: "Desk", category: "Furniture", price: 299, stock: 3 },
]);
```

### 2. Complex Queries

```javascript
// Filter by price
db.products.find({ price: { $gt: 100 } });

// Multiple conditions
db.products.find({ stock: { $gt: 0 }, category: "Electronics" });

// Sort
db.products.find().sort({ price: 1 });
```

### 3. Aggregation

```javascript
db.products.aggregate([
  { $match: { stock: { $gt: 0 } } },
  {
    $group: {
      _id: "$category",
      totalValue: { $sum: { $multiply: ["$price", "$stock"] } },
      avgPrice: { $avg: "$price" },
    },
  },
  { $sort: { totalValue: -1 } },
]);
```

### 4. Indexing Performance

```javascript
// Create index
db.products.createIndex({ price: 1 });

// Check execution
db.products.find({ price: { $gt: 100 } }).explain("executionStats");
```

## Schema Design Patterns

### One-to-Many (Embedding)

```json
{
  "_id": 1,
  "user": "john",
  "posts": [
    { "title": "Post 1", "content": "..." },
    { "title": "Post 2", "content": "..." }
  ]
}
```

### One-to-Many (References)

```json
// Users: { "_id": 1, "name": "john" }
// Posts: { "_id": 101, "userId": 1, "title": "Post 1" }
```

### Many-to-Many

```json
// Students: { "_id": 1, "name": "Alice", "courseIds": [101, 102] }
// Courses: { "_id": 101, "name": "Math", "studentIds": [1, 2, 3] }
```

## Transactions (MongoDB 4.0+)

```javascript
session = db.getMongo().startSession();
session.startTransaction();

try {
  users.updateOne({ _id: 1 }, { $inc: { balance: -100 } }, { session });
  accounts.updateOne({ _id: 2 }, { $inc: { balance: 100 } }, { session });
  session.commitTransaction();
} catch (error) {
  session.abortTransaction();
  throw error;
} finally {
  session.endSession();
}
```

## Backup and Restore

```bash
# Backup
mongodump --uri "mongodb://localhost:27017/myapp" --out ./backup

# Restore
mongorestore --uri "mongodb://localhost:27017" ./backup/myapp

# Export JSON
mongoexport --db myapp --collection users --out users.json

# Import JSON
mongoimport --db myapp --collection users --file users.json
```

## Troubleshooting

- **Connection refused**: Verify MongoDB is running
- **Database locked**: Check for blocking processes
- **Out of memory**: Increase resources
- **Index not used**: Check execution plan

## Best Practices

1. **Index frequently** queried fields
2. **Limit projection** to needed fields
3. **Use $match early** in pipeline
4. **Batch inserts** for performance
5. **Monitor with explain()** before production

## Next Steps

- **Lab 4**: Kafka for streaming to MongoDB
- **Spark Streaming**: Process data before storage
- **Lab 3**: MapReduce for massive aggregation
