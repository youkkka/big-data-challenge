"""

PYSPARK_PYTHON=python3 bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 /project/scripts/kafka_twitter_spark_streaming.py

"""

import pyspark
import json
from pyspark.sql import SparkSession



if __name__ == "__main__":

    spark = SparkSession \
        .builder \
        .appName("PySpark Structured Streaming with Kafka Demo") \
        .master("local[*]") \
        .getOrCreate()

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "twitter") \
        .load()
    
    df.printSchema()

    query = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
        .writeStream \
        .format("console") \
        .option("truncate", "false") \
        .start()

    print(query.recentProgress)
    print(query.status)