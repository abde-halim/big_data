from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split
import argparse
import os
import tempfile
import csv
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


def create_sample_text_file():
    text = (
        "the quick brown fox jumps over the lazy dog\n"
        "the fox is quick and clever\n"
        "the dog is lazy\n"
        "fox and dog are animals\n"
        "quick brown fox is clever\n"
    ) * 10
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w")
    tf.write(text)
    tf.close()
    return tf.name


def wordcount(hdfs_input=None, hdfs_output=None, local=False):
    spark = get_spark("wordcount")

    if local or not hdfs_input:
        input_file = create_sample_text_file()
        output_dir = tempfile.mkdtemp()
        print(f"[LOCAL MODE] Using sample file: {input_file}")
    else:
        input_file = hdfs_input
        output_dir = hdfs_output or "hdfs://cluster-master:9000/user/root/output/wordcount"
        print(f"[HDFS MODE] Reading from: {input_file}")

    # For local files ensure Spark reads from local filesystem
    if local and os.path.isabs(input_file):
        input_path = f"file://{input_file}"
    else:
        input_path = input_file

    lines = spark.read.text(input_path)
    words = lines.select(explode(split(col("value"), " ")).alias("word"))
    words.createOrReplaceTempView("word_table")

    df_counts = words.filter(col("word") != "").groupBy("word").count().orderBy(col("count").desc())
    print("=== Top words (DataFrame) ===")
    df_counts.show(10, truncate=False)

    print("=== Top words (Spark SQL) ===")
    sql_counts = spark.sql(
        """
        SELECT word, COUNT(*) as count
        FROM word_table
        WHERE word != ''
        GROUP BY word
        ORDER BY count DESC
        LIMIT 20
        """
    )
    sql_counts.show(20, truncate=False)

    sql_counts.write.csv(output_dir, mode="overwrite")
    print(f"✓ Results saved to {output_dir}")

    spark_df = sql_counts
    # Visualization helper: convert to Pandas and plot top words
    def visualize_wordcount(spark_df, out_dir):
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
        except Exception:
            print("matplotlib/seaborn not available — install via requirements.txt to visualize")
            return
        pdf = spark_df.limit(20).toPandas()
        if pdf.empty:
            print("No data to visualize")
            return
        plt.figure(figsize=(10,6))
        sns.barplot(x='count', y='word', data=pdf, palette='viridis')
        plt.title('Top words')
        plt.tight_layout()
        out_path = os.path.join(out_dir, 'wordcount_top_words.png')
        plt.savefig(out_path)
        plt.close()
        print(f"✓ Visualization saved to {out_path}")

    # Run visualization if requested via env var (CLI flag handled in main)
    # main passes VISUALIZE env var when appropriate
    if os.environ.get('VISUALIZE') == '1':
        visualize_wordcount(spark_df, output_dir)

    spark.stop()


def dataframe_aggregation(hdfs_input=None, hdfs_output=None, local=False):
    spark = get_spark("dataframe_agg")

    if local or not hdfs_input:
        csv_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", newline="")
        writer = csv.writer(csv_file)
        writer.writerow(["name", "age", "salary", "department"])
        writer.writerows([
            ["Alice", "28", "50000", "IT"],
            ["Bob", "32", "60000", "IT"],
            ["Charlie", "25", "45000", "HR"],
            ["David", "35", "70000", "IT"],
            ["Eve", "29", "55000", "HR"],
        ])
        csv_file.close()
        # ensure local file is read from local FS
        df = spark.read.csv(f"file://{csv_file.name}", header=True, inferSchema=True)
        output_dir = tempfile.mkdtemp()
        print(f"[LOCAL MODE] Using sample CSV: {csv_file.name}")
    else:
        if not hdfs_input:
            raise ValueError("hdfs_input required for HDFS mode")
        df = spark.read.csv(hdfs_input, header=True, inferSchema=True)
        output_dir = hdfs_output or "hdfs://cluster-master:9000/user/root/output/agg"
        print(f"[HDFS MODE] Reading from: {hdfs_input}")

    print("=== DataFrame aggregation ===")
    agg_result = df.groupBy("department").agg({"age": "avg", "salary": "sum"})
    agg_result.show()

    agg_result.write.csv(output_dir, mode="overwrite")
    print(f"✓ Aggregation results saved to {output_dir}")
    # Visualization: bar chart of dept vs sum(salary)
    def visualize_aggregation(df, out_dir):
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
        except Exception:
            print("matplotlib/seaborn not available — install via requirements.txt to visualize")
            return
        pdf = df.toPandas()
        if pdf.empty:
            print("No aggregation data to visualize")
            return
        # normalize column names
        cols = pdf.columns.tolist()
        if len(cols) >= 2:
            xcol = cols[0]
            # choose a numeric column for x
            ycol = cols[1]
        else:
            print("Unexpected aggregation schema for visualization")
            return
        plt.figure(figsize=(8,5))
        import seaborn as sns
        sns.barplot(x=ycol, y=xcol, data=pdf, palette='muted')
        plt.title('Aggregation by ' + xcol)
        plt.tight_layout()
        out_path = os.path.join(out_dir, 'aggregation.png')
        plt.savefig(out_path)
        plt.close()
        print(f"✓ Visualization saved to {out_path}")

    if os.environ.get('VISUALIZE') == '1':
        viz_df = agg_result
        visualize_aggregation(viz_df, output_dir)

    spark.stop()


def dataframe_joins(employees_csv=None, departments_csv=None, hdfs_output=None, local=False):
    spark = get_spark("dataframe_join")

    if local or (not employees_csv and not departments_csv):
        emp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", newline="")
        dept_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", newline="")
        e_writer = csv.writer(emp_file)
        d_writer = csv.writer(dept_file)
        e_writer.writerow(["emp_id", "name", "dept_id"])
        e_writer.writerows([["1", "Alice", "10"], ["2", "Bob", "20"], ["3", "Charlie", "10"], ["4", "David", "30"]])
        d_writer.writerow(["dept_id", "dept_name"])
        d_writer.writerows([["10", "Engineering"], ["20", "Sales"], ["30", "HR"]])
        emp_file.close()
        dept_file.close()
        employees = spark.read.csv(f"file://{emp_file.name}", header=True, inferSchema=True)
        departments = spark.read.csv(f"file://{dept_file.name}", header=True, inferSchema=True)
        output_dir = tempfile.mkdtemp()
        print(f"[LOCAL MODE] Using sample files: {emp_file.name}, {dept_file.name}")
    else:
        if not employees_csv or not departments_csv:
            raise ValueError("employees_csv and departments_csv required for HDFS mode")
        employees = spark.read.csv(employees_csv, header=True, inferSchema=True)
        departments = spark.read.csv(departments_csv, header=True, inferSchema=True)
        output_dir = hdfs_output or "hdfs://cluster-master:9000/user/root/output/emp_dept_join"
        print(f"[HDFS MODE] Reading from provided files")

    print("=== Employees ===")
    employees.show()
    print("=== Departments ===")
    departments.show()
    result = employees.join(departments, on="dept_id", how="inner")
    result.show()

    result.write.csv(output_dir, mode="overwrite")
    print(f"✓ Join results saved to {output_dir}")
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
    stats = {"count": col.count_documents({})}
    print("Collection stats:", stats)
    client.close()


def main():
    parser = argparse.ArgumentParser(description="Consolidated Spark lab exercises")
    parser.add_argument("--exercise", choices=["wordcount", "agg", "join", "mongo", "all"], default="wordcount")
    parser.add_argument("--input", help="HDFS or local input path (csv for agg)")
    parser.add_argument("--employees", help="employees csv path for join")
    parser.add_argument("--departments", help="departments csv path for join")
    parser.add_argument("--mongo_uri", help="MongoDB connection URI")
    parser.add_argument("--local", action="store_true", help="Run in local mode with sample data (no HDFS)")
    parser.add_argument("--visualize", action="store_true", help="Generate visualizations for results")
    args = parser.parse_args()

    # set VISUALIZE env var for downstream functions
    if args.visualize:
        os.environ['VISUALIZE'] = '1'

    if args.exercise in ("wordcount", "all"):
        wordcount(hdfs_input=args.input, hdfs_output=args.input, local=args.local)
    if args.exercise in ("agg", "all"):
        dataframe_aggregation(hdfs_input=args.input, hdfs_output=args.input, local=args.local)
    if args.exercise in ("join", "all"):
        dataframe_joins(employees_csv=args.employees, departments_csv=args.departments, hdfs_output=args.input, local=args.local)
    if args.exercise in ("mongo", "all"):
        print("To run MongoDB steps, call the 'mongodb_example' function or run with --mongo_uri and provide records programmatically.")


if __name__ == '__main__':
    main()
