#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

MASTER="cluster-master"
HDFS_INPUT="/user/root/input"
HDFS_OUTPUT="/user/root/output"
SCRIPTS_DIR="$(pwd)/exercises"

print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

#  EXERCISE 1: WORDCOUNT ANALYSIS WITH SPARK SQL

exercise_1_wordcount_sql() {
    print_header "Exercise 1: WordCount Analysis (consolidated)"
    mkdir -p "$SCRIPTS_DIR"
    # Create single consolidated python file if not present
    if [ ! -f "$SCRIPTS_DIR/lab_exercises.py" ]; then
        echo "Please run './collab.sh all' to generate the consolidated exercises file or create $SCRIPTS_DIR/lab_exercises.py manually." 
    fi
    print_info "Use the consolidated exercises file: $SCRIPTS_DIR/lab_exercises.py"
    echo "Run wordcount inside Docker with:"
    echo "  docker cp exercises/lab_exercises.py cluster-master:/tmp/"
    echo "  docker exec cluster-master spark-submit /tmp/lab_exercises.py --exercise wordcount"
}

#  EXERCISE 2: DATAFRAME AGGREGATION

exercise_2_dataframe_agg() {
    print_header "Exercise 2: DataFrame Aggregation"
    
    mkdir -p "$SCRIPTS_DIR"
    
    # Create sample data
    cat > /tmp/sales.csv << 'EOF'
date,product,amount,region
2026-01-01,laptop,1500,US
2026-01-01,mouse,25,US
2026-01-01,laptop,1500,EU
2026-01-02,keyboard,75,US
2026-01-02,mouse,25,EU
2026-01-02,laptop,1500,ASIA
EOF

    cat > "$SCRIPTS_DIR/dataframe_agg.py" << 'PYSCRIPT'
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum, avg, count, col

spark = SparkSession.builder.master("local[*]").appName('dataframe_agg').getOrCreate()

print("\n=== Loading sales data ===")
df = spark.read.csv("hdfs://hadoop-master:9000/user/root/input/sales.csv", 
                     header=True, inferSchema=True)
df.show()

print("\n=== Total sales by region ===")
by_region = df.groupBy("region").agg(spark_sum("amount").alias("total_sales"))
by_region.show()

print("\n=== Average product price ===")
by_product = df.groupBy("product").agg(
    spark_sum("amount").alias("total"),
    avg("amount").alias("avg_price"),
    count("*").alias("units")
)
by_product.show()

# Save
by_region.write.parquet("hdfs://hadoop-master:9000/user/root/output/sales_by_region", mode="overwrite")
print("\n✓ Results saved to HDFS")

spark.stop()
PYSCRIPT

    print_success "Created: $SCRIPTS_DIR/dataframe_agg.py"
    echo "Upload data first:"
    echo "  docker cp /tmp/sales.csv cluster-master:/tmp/"
    echo "  docker exec cluster-master bash -c 'hdfs dfs -put -f /tmp/sales.csv /user/root/input/'"
    echo ""
    echo "Then run:"
    echo "  docker cp exercises/dataframe_agg.py cluster-master:/tmp/"
    echo "  docker exec cluster-master spark-submit /tmp/dataframe_agg.py"
}

#  EXERCISE 3: DATAFRAME JOINS

exercise_3_joins() {
    print_header "Exercise 3: DataFrame Joins"
    
    mkdir -p "$SCRIPTS_DIR"
    
    # Create sample data
    cat > /tmp/employees.csv << 'EOF'
emp_id,name,dept_id
1,Alice,10
2,Bob,20
3,Charlie,10
EOF

    cat > /tmp/departments.csv << 'EOF'
dept_id,dept_name
10,Engineering
20,Sales
30,HR
EOF

    cat > "$SCRIPTS_DIR/dataframe_join.py" << 'PYSCRIPT'
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").appName('df_join').getOrCreate()

print("\n=== Loading datasets ===")
employees = spark.read.csv("hdfs://hadoop-master:9000/user/root/input/employees.csv", 
                           header=True, inferSchema=True)
departments = spark.read.csv("hdfs://hadoop-master:9000/user/root/input/departments.csv", 
                            header=True, inferSchema=True)

print("\n=== Employees ===")
employees.show()

print("\n=== Departments ===")
departments.show()

print("\n=== INNER JOIN: Employees with departments ===")
result = employees.join(departments, on="dept_id", how="inner")
result.show()

# Save
result.write.csv("hdfs://hadoop-master:9000/user/root/output/emp_dept_join", mode="overwrite")
print("\n✓ Results saved to HDFS")

spark.stop()
PYSCRIPT

    print_success "Created: $SCRIPTS_DIR/dataframe_join.py"
    echo "Upload data first:"
    echo "  docker cp /tmp/employees.csv /tmp/departments.csv cluster-master:/tmp/"
    echo "  docker exec cluster-master bash -c 'hdfs dfs -put -f /tmp/employees.csv /tmp/departments.csv /user/root/input/'"
    echo ""
    echo "Then run:"
    echo "  docker cp exercises/dataframe_join.py cluster-master:/tmp/"
    echo "  docker exec cluster-master spark-submit /tmp/dataframe_join.py"
}

#  EXERCISE 4: MONGODB INTEGRATION

exercise_4_mongodb() {
    print_header "Exercise 4: MongoDB Integration with PyMongo"
    
    mkdir -p "$SCRIPTS_DIR"
    
    cat > "$SCRIPTS_DIR/mongodb_integration.py" << 'PYSCRIPT'
from pymongo import MongoClient
from datetime import datetime

# MongoDB Atlas Connection
MONGO_URI = "mongodb+srv://abdelilahhalim05_db_user:C2X4AXnO7MJWm52Z@cluster0.htrgtlb.mongodb.net/"
client = MongoClient(MONGO_URI)

# Create/Access Database and Collection
db = client['spark_lab']
employees_col = db['employees']
departments_col = db['departments']
transactions_col = db['transactions']

print("\n=== MongoDB Integration ===\n")

# Clear collections
employees_col.delete_many({})
departments_col.delete_many({})
transactions_col.delete_many({})
print("✓ Cleared collections")

# Insert Employees
employees = [
    {"emp_id": 1, "name": "Alice", "dept_id": 10, "salary": 85000},
    {"emp_id": 2, "name": "Bob", "dept_id": 20, "salary": 75000},
    {"emp_id": 3, "name": "Charlie", "dept_id": 10, "salary": 90000}
]
employees_col.insert_many(employees)
print(f"✓ Inserted {len(employees)} employees")

# Insert Departments
departments = [
    {"dept_id": 10, "dept_name": "Engineering", "location": "San Francisco"},
    {"dept_id": 20, "dept_name": "Sales", "location": "New York"},
    {"dept_id": 30, "dept_name": "HR", "location": "Boston"}
]
departments_col.insert_many(departments)
print(f"✓ Inserted {len(departments)} departments")

# Insert Sample Transactions
transactions = [
    {"trans_id": 101, "emp_id": 1, "amount": 5000, "date": "2026-01-15", "type": "salary"},
    {"trans_id": 102, "emp_id": 2, "amount": 3000, "date": "2026-01-16", "type": "expense"},
    {"trans_id": 103, "emp_id": 3, "amount": 2000, "date": "2026-01-17", "type": "bonus"},
    {"trans_id": 104, "emp_id": 1, "amount": 1500, "date": "2026-01-18", "type": "expense"}
]
transactions_col.insert_many(transactions)
print(f"✓ Inserted {len(transactions)} transactions")

print("\n=== CRUD Operations ===\n")

# READ: Find employees in Engineering department
print("Employees in Engineering department:")
eng_employees = employees_col.find({"dept_id": 10})
for emp in eng_employees:
    print(f"  - {emp['name']} (ID: {emp['emp_id']}, Salary: ${emp['salary']})")

# UPDATE: Raise Alice's salary by 5%
employees_col.update_one({"emp_id": 1}, {"$set": {"salary": 89250}})
print("\n✓ Updated Alice's salary to $89,250")

# DELETE: Remove HR department (no employees)
departments_col.delete_one({"dept_id": 30})
print("✓ Deleted HR department")

print("\n=== Aggregation Pipeline ===\n")

# Aggregation: Employee salary by department
pipeline = [
    {"$group": {
        "_id": "$dept_id",
        "avg_salary": {"$avg": "$salary"},
        "count": {"$sum": 1},
        "total_salary": {"$sum": "$salary"}
    }},
    {"$sort": {"avg_salary": -1}}
]

print("Salary statistics by department:")
for result in employees_col.aggregate(pipeline):
    print(f"  Dept {result['_id']}: Avg=${result['avg_salary']:.2f}, Count={result['count']}, Total=${result['total_salary']}")

# Aggregation: Transaction summary
trans_pipeline = [
    {"$group": {
        "_id": "$type",
        "total": {"$sum": "$amount"},
        "count": {"$sum": 1},
        "avg": {"$avg": "$amount"}
    }},
    {"$sort": {"total": -1}}
]

print("\nTransaction summary by type:")
for result in transactions_col.aggregate(trans_pipeline):
    print(f"  {result['_id'].upper()}: Total=${result['total']}, Count={result['count']}, Avg=${result['avg']:.2f}")

print("\n=== Indexes ===\n")

# Create indexes for performance
employees_col.create_index("emp_id")
departments_col.create_index("dept_id")
transactions_col.create_index([("emp_id", 1), ("date", 1)])
print("✓ Created indexes on emp_id, dept_id, (emp_id, date)")

print("\n=== Collection Statistics ===\n")
print(f"Employees count: {employees_col.count_documents({})}")
print(f"Departments count: {departments_col.count_documents({})}")
print(f"Transactions count: {transactions_col.count_documents({})}")

print("\n✓ MongoDB integration complete!")
client.close()
PYSCRIPT

    print_success "Created: $SCRIPTS_DIR/mongodb_integration.py"
    echo ""
    echo "Run with:"
    echo "  pip install pymongo"
    echo "  python exercises/mongodb_integration.py"
}

#  MAIN MENU
show_menu() {
    print_header "CLUSTER SPARK - ESSENTIAL EXERCISES"
    
    echo "Usage: ./collab.sh [option]"
    echo ""
    echo "Options:"
    echo "  1   - WordCount Analysis with Spark SQL"
    echo "  2   - DataFrame Aggregation"
    echo "  3   - DataFrame Joins"
    echo "  4   - MongoDB Integration"
    echo "  all - Generate all exercises"
    echo ""
}

case "${1:-menu}" in
    1) exercise_1_wordcount_sql ;;
    2) exercise_2_dataframe_agg ;;
    3) exercise_3_joins ;;
    4) exercise_4_mongodb ;;
    all)
        exercise_1_wordcount_sql
        echo ""
        exercise_2_dataframe_agg
        echo ""
        exercise_3_joins
        echo ""
        exercise_4_mongodb
        echo ""
        print_header "All exercises generated in: $SCRIPTS_DIR/"
        ls -1 "$SCRIPTS_DIR/"
        ;;
    menu|help|--help|-h)
        show_menu
        ;;
    *)
        echo "Unknown option: $1"
        show_menu
        exit 1
        ;;
esac
