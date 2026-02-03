from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Football Spark SQL Lab") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")


df = spark.read \
    .option("header", True) \
    .option("inferSchema", True) \
    .csv("fifaworldcup.csv")

df.createOrReplaceTempView("matches")

# Q1
spark.sql("SELECT COUNT(*) AS total_matches FROM matches").show()

# Q2
spark.sql("""
SELECT MIN(YEAR(date)) AS first_year,
       MAX(YEAR(date)) AS last_year
FROM matches
""").show()

# Q3
spark.sql("""
SELECT tournament, COUNT(*) AS nb_matches
FROM matches
GROUP BY tournament
ORDER BY nb_matches DESC
LIMIT 10
""").show(truncate=False)

# Q4
spark.sql("""
SELECT COUNT(*) AS neutral_matches
FROM matches
WHERE neutral = true
""").show()

# Q5
spark.sql("""
SELECT country, COUNT(*) AS nb_matches
FROM matches
GROUP BY country
ORDER BY nb_matches DESC
LIMIT 10
""").show(truncate=False)

# Q6
spark.sql("""
SELECT COUNT(*) AS draws
FROM matches
WHERE home_score = away_score
""").show()

# Q7
spark.sql("""
SELECT date, home_team, away_team,
       home_score, away_score,
       (home_score + away_score) AS total_goals
FROM matches
WHERE home_score + away_score > 6
ORDER BY total_goals DESC
""").show(truncate=False)

# Q8
spark.sql("""
SELECT team, COUNT(*) AS total_matches
FROM (
    SELECT home_team AS team FROM matches
    UNION ALL
    SELECT away_team AS team FROM matches
)
GROUP BY team
ORDER BY total_matches DESC
""").show(truncate=False)

# Q9
spark.sql("""
SELECT team, SUM(goals) AS total_goals
FROM (
    SELECT home_team AS team, home_score AS goals FROM matches
    UNION ALL
    SELECT away_team AS team, away_score AS goals FROM matches
)
GROUP BY team
ORDER BY total_goals DESC
LIMIT 10
""").show(truncate=False)

# Q10
spark.sql("""
SELECT (YEAR(date)/10)*10 AS decade,
       AVG(home_score + away_score) AS avg_goals
FROM matches
GROUP BY (YEAR(date)/10)*10
ORDER BY decade
""").show()

# Q11
spark.sql("""
SELECT tournament, YEAR(date) AS year,
       COUNT(*) AS nb_matches
FROM matches
GROUP BY tournament, YEAR(date)
ORDER BY tournament, year
""").show(truncate=False)

# Q12
spark.sql("""
SELECT home_team AS team, COUNT(*) AS home_wins
FROM matches
WHERE home_score > away_score
GROUP BY home_team
ORDER BY home_wins DESC
""").show(truncate=False)

# Q13
spark.sql("""
SELECT team,
       SUM(win) AS wins,
       SUM(draw) AS draws,
       SUM(loss) AS losses
FROM (
    SELECT home_team AS team,
           CASE WHEN home_score > away_score THEN 1 ELSE 0 END AS win,
           CASE WHEN home_score = away_score THEN 1 ELSE 0 END AS draw,
           CASE WHEN home_score < away_score THEN 1 ELSE 0 END AS loss
    FROM matches
    UNION ALL
    SELECT away_team,
           CASE WHEN away_score > home_score THEN 1 ELSE 0 END,
           CASE WHEN home_score = away_score THEN 1 ELSE 0 END,
           CASE WHEN away_score < home_score THEN 1 ELSE 0 END
    FROM matches
)
GROUP BY team
ORDER BY wins DESC
""").show(truncate=False)

# Q14
spark.sql("""
SELECT neutral,
       AVG(home_score + away_score) AS avg_goals
FROM matches
GROUP BY neutral
""").show()

# Q15
spark.sql("""
SELECT date, home_team, away_team,
       home_score, away_score,
       ABS(home_score - away_score) AS goal_diff
FROM matches
ORDER BY goal_diff DESC
LIMIT 5
""").show(truncate=False)

# Q16 
spark.sql("""
SELECT team,
       SUM(scored) - SUM(conceded) AS goal_average
FROM (
    SELECT home_team AS team,
           home_score AS scored,
           away_score AS conceded
    FROM matches
    UNION ALL
    SELECT away_team,
           away_score,
           home_score
    FROM matches
)
GROUP BY team
ORDER BY goal_average DESC
""").show(truncate=False)

# Q17 
spark.sql("""
SELECT year, team, wins,
       ROW_NUMBER() OVER (PARTITION BY year ORDER BY wins DESC) AS rank
FROM (
    SELECT YEAR(date) AS year,
           home_team AS team,
           COUNT(*) AS wins
    FROM matches
    WHERE home_score > away_score
    GROUP BY YEAR(date), home_team
)
ORDER BY year, rank
""").show(truncate=False)

# Q18 
spark.sql("""
SELECT (YEAR(date)/10)*10 AS decade,
       COUNT(*) AS nb_matches
FROM matches
GROUP BY (YEAR(date)/10)*10
ORDER BY decade
""").show()

# Q19 
spark.sql("""
SELECT team, year
FROM (
    SELECT team, year, SUM(loss) AS losses
    FROM (
        SELECT home_team AS team, YEAR(date) AS year,
               CASE WHEN home_score < away_score THEN 1 ELSE 0 END AS loss
        FROM matches
        UNION ALL
        SELECT away_team, YEAR(date),
               CASE WHEN away_score < home_score THEN 1 ELSE 0 END
        FROM matches
    )
    GROUP BY team, year
)
WHERE losses = 0
""").show(truncate=False)

# Q20 –
spark.sql("""
WITH results AS (
    SELECT date, team, result,
           ROW_NUMBER() OVER (PARTITION BY team ORDER BY date) -
           ROW_NUMBER() OVER (PARTITION BY team, result ORDER BY date) AS grp
    FROM (
        SELECT date, home_team AS team,
               CASE WHEN home_score > away_score THEN 'W' ELSE 'N' END AS result
        FROM matches
        UNION ALL
        SELECT date, away_team,
               CASE WHEN away_score > home_score THEN 'W' ELSE 'N' END
        FROM matches
    )
),
streaks AS (
    SELECT team, COUNT(*) AS win_streak
    FROM results
    WHERE result = 'W'
    GROUP BY team, grp
)
SELECT team, MAX(win_streak) AS longest_win_streak
FROM streaks
GROUP BY team
ORDER BY longest_win_streak DESC
""").show(truncate=False)

# Q21 
spark.sql("""
SELECT tournament, team, wins
FROM (
    SELECT tournament, team, COUNT(*) AS wins,
           ROW_NUMBER() OVER (PARTITION BY tournament ORDER BY COUNT(*) DESC) AS rnk
    FROM (
        SELECT tournament, home_team AS team
        FROM matches WHERE home_score > away_score
        UNION ALL
        SELECT tournament, away_team
        FROM matches WHERE away_score > home_score
    )
    GROUP BY tournament, team
)
WHERE rnk = 1
""").show(truncate=False)

# Q22 
spark.sql("""
SELECT team,
       SUM(home_wins) AS home_wins,
       SUM(away_wins) AS away_wins
FROM (
    SELECT home_team AS team,
           CASE WHEN home_score > away_score THEN 1 ELSE 0 END AS home_wins,
           0 AS away_wins
    FROM matches
    UNION ALL
    SELECT away_team,
           0,
           CASE WHEN away_score > home_score THEN 1 ELSE 0 END
    FROM matches
)
GROUP BY team
""").show(truncate=False)


spark.stop()
print("park stopped")
