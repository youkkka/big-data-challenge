"""
RUNNING PROGRAM;
1-Start Apache Kafka
./kafka/kafka_2.11-0.11.0.0/bin/kafka-server-start.sh ./kafka/kafka_2.11-0.11.0.0/config/server.properties
2-Run kafka_push_listener.py (Start Producer)
ipython >> run kafka_push_listener.py
3-Run kafka_twitter_spark_streaming.py (Start Consumer)
PYSPARK_PYTHON=python3 bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.0 /project/scripts/kafka_twitter_spark_streaming.py
PYSPARK_PYTHON=python3 bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-9_2.11:2.2.0 /project/scripts/kafka_twitter_spark_streaming.py
PYSPARK_PYTHON=python3 bin/spark-submit /project/scripts/kafka_twitter_spark_streaming.py

PYSPARK_PYTHON=python3 bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 /project/scripts/kafka_twitter_spark_streaming.py

"""

import pyspark
# from pyspark import SparkContext
# from pyspark.streaming import StreamingContext
import json
from pyspark.sql import SparkSession



if __name__ == "__main__":
    # print('\n\n\n\n\n\n\n\n\n\nVERSION', pyspark.__version__, '\n\n\n\n\n')

	#Create Spark Context to Connect Spark Cluster
    # sc = pyspark.SparkContext(appName="PythonStreamingKafkaTweetCount")

	#Set the Batch Interval is 10 sec of Streaming Context
    # ssc = StreamingContext(sc, 10)

	#Create Kafka Stream to Consume Data Comes From Twitter Topic
	#localhost:2181 = Default Zookeeper Consumer Address
    # kafkaStream = pyspark.streaming.kafka.KafkaUtils.createStream(ssc, 'localhost:2181', 'spark-streaming', {'twitter':1})

    SparkJar = "file:///C://spark-3.1.2-bin-hadoop3.2//jar_files//commons-logging-1.1.3.jar," \
    "file:///C://spark-3.1.2-bin-hadoop3.2//jar_files//commons-pool2-2.6.2.jar,"\
    "file:///C://spark-3.1.2-bin-hadoop3.2//jar_files//hadoop-client-api-3.3.1.jar,"\
    "file:///C://spark-3.1.2-bin-hadoop3.2//jar_files//hadoop-client-runtime-3.3.1.jar,"\
    "file:///C://spark-3.1.2-bin-hadoop3.2//jar_files//htrace-core4-4.1.0-incubating.jar,"\
    "file:///C://spark-3.1.2-bin-hadoop3.2//jar_files//jsr305-3.0.0.jar,"\
    "file:///C://spark-3.1.2-bin-hadoop3.2//jar_files//kafka-clients-2.8.0.jar,"\
    "file:///C://spark-3.1.2-bin-hadoop3.2//jar_files//lz4-java-1.7.1.jar,"\
    "file:///C://spark-3.1.2-bin-hadoop3.2//jar_files//scala-library-2.12.15.jar,"\
    "file:///C://spark-3.1.2-bin-hadoop3.2//jar_files//slf4j-api-1.7.30.jar,"\
    "file:///C://spark-3.1.2-bin-hadoop3.2//jar_files//snappy-java-1.1.8.1.jar,"\
    "file:///C://spark-3.1.2-bin-hadoop3.2//jar_files//spark-sql-kafka-0-10_2.12-3.2.0.jar,"\
    "file:///C://spark-3.1.2-bin-hadoop3.2//jar_files//spark-tags_2.12-3.2.0.jar,"\
    "file:///C://spark-3.1.2-bin-hadoop3.2//jar_files//spark-token-provider-kafka-0-10_2.12-3.2.0.jar,"\
    "file:///C://spark-3.1.2-bin-hadoop3.2//jar_files//unused-1.0.0.jar," \
    "file:///C://spark-3.2.0-bin-hadoop3.2//jars//spark-sql_2.12-3.2.0.jar," \
    "file:///C://spark-3.2.0-bin-hadoop3.2//jars//spark-streaming_2.12-3.2.0.jar"

    spark = SparkSession \
        .builder \
        .appName("PySpark Structured Streaming with Kafka Demo") \
        .master("local[*]") \
        .getOrCreate()
        # .config("spark.jars",SparkJar) \
        # .config("spark.executor.extraClassPath", SparkJar) \
        # .config("spark.executor.extraLibrary", SparkJar) \
        # .config("spark.driver.extraClassPath", SparkJar) \
        # .getOrCreate()


    # Subscribe to 1 topic
    df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "twitter") \
    .load()

    df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
    
    df.printSchema()

    # df.writeStream.start()
    # print(df.collect())

    query = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
        .writeStream \
        .format("console") \
        .option("checkpointLocation", "path/to/HDFS/dir") \
        .start()

    query.awaitTermination()

    #Parse Twitter Data as json
    # parsed = kafkaStream.map(lambda v: json.loads(v[1]))

	#Count the number of tweets per User
    # user_counts = parsed.map(lambda tweet: (tweet['user']["screen_name"], 1)).reduceByKey(lambda x,y: x + y)

	#Print the User tweet counts
    # user_counts.pprint()

	#Start Execution of Streams
    # ssc.start()
    # ssc.awaitTermination()
