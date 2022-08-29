"""
this script is being run on spark container in docker-compose with the following command:
PYSPARK_PYTHON=python3 bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 /project/scripts/kafka_twitter_spark_streaming.py

"""

import pyspark
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.functions import from_json, col, udf



if __name__ == "__main__":

    db_target_properties = {"user":"localuser", "password":"localpwd"}

    # this function is supposed to write to mysql db but it doesn't (yet) :(
    def save_to_mysql(df, batchID):
        url = "mysql:3306"
        df.write.jdbc(
            url="mysql:3306",
            table="counts",
            properties=db_target_properties
        )

    # open a spark session
    spark = SparkSession \
        .builder \
        .appName("Twitter Structured Streaming from Kafka") \
        .master("local[*]") \
        .getOrCreate()

    # hide info logs in terminal
    sc = spark.sparkContext
    sc.setLogLevel("WARN")

    # initialize stream from kafka with topic twitter
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "twitter") \
        .load()

    # get only value
    df = df.selectExpr("CAST(value AS STRING)")

    # split into pieces on " "
    words = df.select(
    explode(
        split(df.value, " ")
    ).alias("word")
    )

    # get only users or hashtags (I didn't use that in the end)
    users = words.filter(col("word").startswith("@"))
    hashtags = words.filter(col("word").startswith("#"))

    # get only words mother and father (also getting some noise such as strings starting with mother but having somethingg else)
    momsanddads = words.filter(
        (col("word").startswith("mother")) | (col("word").startswith("father"))
        )

    # write df with mother and father to console
    query = momsanddads \
        .writeStream \
        .format("console") \
        .start()

    # # this query is supposed to call function save_to_mysql() for each batch but the function won't connect to mysql (yet)
    # query = momsanddads \
    #     .writeStream \
    #     .foreachBatch(save_to_mysql) \
    #     .start()

    query.awaitTermination()
