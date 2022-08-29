"""

PYSPARK_PYTHON=python3 bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 /project/scripts/kafka_twitter_spark_streaming.py

"""

import pyspark
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split



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

    # df = df.map(lambda v: json.loads(v[1]))


    df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    # Split the lines into words
    words = df.select(
    explode(
        split(df.value, " ")
    ).alias("word")
    )

    # Generate running word count
    wordCounts = words.groupBy("word").count()

     # Start running the query that prints the running counts to the console
    query = wordCounts \
        .writeStream \
        .format("console") \
        .outputMode("Update") \
        .option("truncate", "false") \
        .start()

    #query.awaitTermination()
    
    # df.printSchema()

    # query = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
    #     .writeStream \
    #     .format("console") \
    #     .option("truncate", "false") \
    #     .start()



    print(query.recentProgress)
    print(query.status)