from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Football Spark SQL Lab") \
    .master("local[*]") \
    .getOrCreate()

df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("fifaworldcup.csv")

df.show(5)
df.printSchema()
df.createOrReplaceTempView("matches")


# spark.sql("""
# SELECT COUNT(*) AS total_matches
# FROM matches
# """).show()

# spark.sql("""
# SELECT 
#     MIN(YEAR(date)) AS first_year,
#     MAX(YEAR(date)) AS last_year
# FROM matches
# """).show()

# spark.sql("""
# SELECT tournament, COUNT(*) AS nb_matches
# FROM matches
# GROUP BY tournament
# ORDER BY nb_matches DESC
# LIMIT 10
# """).show(truncate=False)


# spark.sql("""
#           select country,
#            count(*) as count from matches
#            group by country order by count desc
# """).show(5)


# spark.sql("""
#           select count(*) as count from matches
#            group by country order by count desc
# """).show(5)


# spark.sql("""
# SELECT date, home_team, away_team, home_score, away_score,
#        (home_score + away_score) AS total_goals
# FROM matches
# WHERE home_score + away_score > 6
# ORDER BY total_goals DESC
# """).show()

df.createOrReplaceTempView("matches")


spark.sql("""
SELECT team, COUNT(*) AS total_matches
FROM (
    SELECT home_team AS team FROM matches
    UNION ALL
    SELECT away_team AS team FROM matches
)
GROUP BY team
ORDER BY total_matches DESC;
""").show(10)

