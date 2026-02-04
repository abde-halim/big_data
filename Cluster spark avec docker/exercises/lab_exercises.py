from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split
import argparse
import os
try:
    from pymongo import MongoClient
except Exception:
    MongoClient = None


def get_spark(app_name="lab_exercises", master=None):
    builder = SparkSession.builder.appName(app_name)
    if master:
        builder = builder.master(master)
    else:
        builder = builder.master(os.environ.get("SPARK_MASTER", "local[*]"))
    return builder.getOrCreate()


def wordcount(hdfs_input="hdfs://hadoop-master:9000/user/root/input/alice.txt", hdfs_output="hdfs://hadoop-master:9000/user/root/output/wordcount"):
    spark = get_spark("wordcount")
    lines = spark.read.text(hdfs_input)
    words = lines.select(explode(split(col("value"), " ")).alias("word"))
    words.createOrReplaceTempView("word_table")

    # DataFrame API
    df_counts = words.filter(col("word") != "").groupBy("word").count().orderBy(col("count").desc())
    print("=== Top words (DataFrame) ===")
    df_counts.show(10, truncate=False)

    # SQL API
    print("=== Top words (Spark SQL) ===")
    sql_counts = spark.sql("""
        SELECT word, COUNT(*) as count
        FROM word_table
        WHERE word != ''
        GROUP BY word
        ORDER BY count DESC
        LIMIT 20
    """)
    sql_counts.show(20, truncate=False)

    sql_counts.write.csv(hdfs_output, mode="overwrite")
    print(f"✓ Results saved to {hdfs_output}")
    spark.stop()


def dataframe_aggregation(hdfs_input=None, hdfs_output="hdfs://hadoop-master:9000/user/root/output/agg"):
    spark = get_spark("dataframe_agg")
    if hdfs_input:
        df = spark.read.csv(hdfs_input, header=True, inferSchema=True)
    else:
        raise ValueError("hdfs_input must be provided for dataframe_aggregation")

    print("=== Schema ===")
    df.printSchema()
    print("=== Aggregations ===")
    df.groupBy("Transaction Type").sum("Amount").show()
    df.groupBy("Transaction Type").avg("Amount").show()
    df.write.mode("overwrite").parquet(hdfs_output)
    print(f"✓ Aggregation results saved to {hdfs_output}")
    spark.stop()


def dataframe_joins(employees_csv, departments_csv, hdfs_output="hdfs://hadoop-master:9000/user/root/output/emp_dept_join"):
    spark = get_spark("dataframe_join")
    employees = spark.read.csv(employees_csv, header=True, inferSchema=True)
    departments = spark.read.csv(departments_csv, header=True, inferSchema=True)
    print("=== Employees ===")
    employees.show()
    print("=== Departments ===")
    departments.show()
    result = employees.join(departments, on="dept_id", how="inner")
    result.show()
    result.write.csv(hdfs_output, mode="overwrite")
    print(f"✓ Join results saved to {hdfs_output}")
    spark.stop()


def mongodb_example(records, mongo_uri=None, dbname="spark_lab", collection="transactions"):
    if MongoClient is None:
        raise RuntimeError("PyMongo is not installed. Install with: pip install pymongo")
    uri = mongo_uri or os.environ.get("MONGO_URI")
    if not uri:
        raise ValueError("MongoDB URI must be provided via argument or MONGO_URI env var")
    client = MongoClient(uri)
    db = client[dbname]
    col = db[collection]
    col.delete_many({})
    if records:
        col.insert_many(records)
        print(f"✓ Inserted {len(records)} records into {dbname}.{collection}")
    else:
        print("No records provided to insert")
    stats = {
        "count": col.count_documents({})
    }
    print("Collection stats:", stats)
    client.close()


def main():
    parser = argparse.ArgumentParser(description="Consolidated Spark lab exercises")
    parser.add_argument("--exercise", choices=["wordcount", "agg", "join", "mongo", "all"], default="all")
    parser.add_argument("--input", help="HDFS or local input path (csv for agg)")
    parser.add_argument("--employees", help="employees csv path for join")
    parser.add_argument("--departments", help="departments csv path for join")
    parser.add_argument("--mongo_uri", help="MongoDB connection URI")
    args = parser.parse_args()

    if args.exercise in ("wordcount", "all"):
        wordcount()
    if args.exercise in ("agg", "all") and args.input:
        dataframe_aggregation(hdfs_input=args.input)
    if args.exercise in ("join", "all") and args.employees and args.departments:
        dataframe_joins(args.employees, args.departments)
    if args.exercise in ("mongo", "all"):
        # For demo, we pass no records here; caller can call mongodb_example programmatically
        print("To run MongoDB steps, call the 'mongodb_example' function or run with --mongo_uri and provide records programmatically.")


if __name__ == '__main__':
    main()
