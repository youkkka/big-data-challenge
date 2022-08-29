"""

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

    def save_to_mysql(df, batchID):
        url = "mysql:3306"
        df.write.jdbc(
            url="mysql:3306",
            table="counts",
            properties=db_target_properties
        )


    spark = SparkSession \
        .builder \
        .appName("Twitter Structured Streaming from Kafka") \
        .master("local[*]") \
        .getOrCreate()

    sc = spark.sparkContext
    sc.setLogLevel("WARN")

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "twitter") \
        .load()


    df = df.selectExpr("CAST(value AS STRING)")

    words = df.select(
    explode(
        split(df.value, " ")
    ).alias("word")
    )

    users = words.filter(col("word").startswith("@"))
    hashtags = words.filter(col("word").startswith("#"))

    moms = words.filter(
        (col("word").startswith("mother")) | (col("word").startswith("father"))
        )
    # dads = words.filter(col("word").startswith("father"))

    # userCounts = users.groupBy("word").count()

    # momCounts = moms.groupBy("word").count()

    query = moms \
        .writeStream \
        .foreachBatch(save_to_mysql) \
        .start()

    # query = moms \
    #     .writeStream \
    #     .format("console") \
    #     .start()

    query.awaitTermination()
