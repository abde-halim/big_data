# Lab Spark SQL - FIFA World Cup Analysis

## Objective

This laboratory uses **Apache Spark SQL** to analyze FIFA World Cup data. The objectives are:

- Load and process CSV data with Spark
- Execute SQL queries on DataFrames Spark
- Analyze complex sports data
- Optimize distributed queries

## Description

This project analyzes a FIFA dataset containing World Cup match information including:

- Match dates and years
- Teams involved
- Scores and goals
- Tournaments and neutral venues
- Statistics by country and tournament

## Prerequisites

- Python 3.7+
- Apache Spark 3.0+
- Dataset file: `fifaworldcup.csv`

## Installation

```bash
# Install PySpark
pip install pyspark

# Optional: for enhanced display
pip install pandas
```

## Data

### File: `fifaworldcup.csv`

Main columns:
| Column | Type | Description |
|--------|------|-------------|
| date | Date | Match date |
| home_team | String | Home team |
| away_team | String | Away team |
| home_score | Integer | Goals (home) |
| away_score | Integer | Goals (away) |
| tournament | String | Tournament name |
| country | String | Host country |
| neutral | Boolean | Neutral venue? |

## Execution

```bash
python main.py
```

## SQL Queries

The script implements multiple analyses:

### Q1 - Total Matches

```sql
SELECT COUNT(*) AS total_matches FROM matches
```

### Q2 - Years Covered

```sql
SELECT MIN(YEAR(date)) AS first_year,
       MAX(YEAR(date)) AS last_year
FROM matches
```

### Q3 - Top 10 Tournaments

```sql
SELECT tournament, COUNT(*) AS nb_matches
FROM matches
GROUP BY tournament
ORDER BY nb_matches DESC
LIMIT 10
```

### Q4 - Neutral Venue Matches

```sql
SELECT COUNT(*) AS neutral_matches
FROM matches
WHERE neutral = true
```

### Q5 - Top 10 Countries by Matches

```sql
SELECT country, COUNT(*) AS nb_matches
FROM matches
GROUP BY country
ORDER BY nb_matches DESC
LIMIT 10
```

## Project Structure

```
lab_spark_sql_fifa/
├── README.md                   # This file
├── main.py                     # Main analysis script
├── CONTENT.md                  # Original PDF content (French)
└── fifaworldcup.csv           # FIFA data
```

## Key Concepts

### SparkSession

Entry point for Spark SQL functionality:

```python
spark = SparkSession.builder \
    .appName("Football Spark SQL Lab") \
    .master("local[*]") \
    .getOrCreate()
```

### DataFrame

Distributed structured data representation.

### Temporary Views

Temporary tables from DataFrames:

```python
df.createOrReplaceTempView("matches")
```

### SQL Operations

Standard SQL queries on DataFrames:

```python
spark.sql("SELECT ... FROM matches").show()
```

## Practical Exercises

1. **Count matches** per year
2. **Find team** with most matches
3. **Analyze victories** (goal differences)
4. **Calculate statistics** by tournament
5. **Identify trends** across decades
6. **Compare** home vs away performance

## Additional Queries

```sql
-- Matches per year
SELECT YEAR(date) AS year, COUNT(*) AS count
FROM matches
GROUP BY YEAR(date)
ORDER BY year

-- Most wins
SELECT home_team, COUNT(*) AS wins
FROM matches
WHERE home_score > away_score
GROUP BY home_team
ORDER BY wins DESC
LIMIT 10

-- Average goals per tournament
SELECT tournament, AVG(home_score + away_score) AS avg_goals
FROM matches
GROUP BY tournament
ORDER BY avg_goals DESC
```

## Execution Modes

The script uses **local[*]** mode:

- `local[*]`: Use all available cores locally
- `local[n]`: Use n specific cores
- `spark://master:7077`: Cluster mode (requires Spark cluster)

## Output Display

```python
# Default display
df.show()

# Without truncation
df.show(truncate=False)

# Custom row count
df.show(20)
```

## Troubleshooting

- **OutOfMemoryError**: Increase Spark memory: `--driver-memory 4g`
- **File not found**: Check CSV path
- **Missing columns**: Verify CSV column names and order

## Extensions

1. **Spark Streaming**: Real-time analysis
2. **MLlib**: Match result prediction
3. **GraphX**: Team network analysis
4. **Delta Lake**: Data versioning
5. **Visualization**: Charts with Matplotlib/Seaborn

## Next Steps

- **Lab 3**: MapReduce - Alternative batch processing
- **Lab 4**: Kafka - Real-time streaming
- **TP Spark Streaming**: Real-time Spark processing
