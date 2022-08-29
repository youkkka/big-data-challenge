# Big Data Management Challenge

This small project has been developed while applying for a Junior Big Data Engineer position at KPMG to demonstrate my ability to quickly grasp and apply technologies that are new to me.

## Docker-compose

Project contains file docker-compose.yml that consists of six containers:
- zookeeper
- kafka
- spark (master node)
- python
- mysql
- adminer (for webui mysql)


## How to run the project?

Make sure you have docker engine and docker compose installed. In command line go to project directory and run

```
docker-compose up
```

## What does it do?

The system gets stream of data from Twitter-API in real-time on all the tweets that contain words "apple" or "orange". The end-goal of this mini-project is to assess which of them is more popular on twitter. Initial idea was to assess two popular technologies but in order to demonstrate a really large stream of data I had to switch to these more common random words.

## What happens inside?

Kafka producer runs in python-scripts container, gets connected to Twitter-API and listens to all tweets that contain words "apple" or "orange".

Kafka consumer runs in spark container, subcribes to topic "twitter" from kafka-producer and gets the stream.

With Structured Streaming Spark gets data stream from kafka consumer, partitions it into separate words and filters only those that start with "apple" or "orange". After filtering, Spark outputs results in mini-batches to docker console.

## Work In Progress

My goal was to count words "apple" and "orange" and write the results into a simple table in MySQL database to assess what is more popular on Twitter.

MySQL database is up and accessible via adminer on localhost:8081. As an example, script mysql_db.py has full access to the database. The point of struggle at the moment is to write from Spark Structured Streaming into MySQL. Possible reason for this is that there is no mysql-connector inside Spark container.

Word count can run but does not output any results in console due to output mode (for aggregated queries it is either "complete" or "update" which cannot be printed ad-hoc as opposed to "append"). To get printed results and not a silent spark node, I decided to print dataframe with words.

Also, at the moment printed results contain not only "apple" and "orange" but some noise such as "apple'},"id":{..." It is due to specific string format of kafka data and split parameters. It was not instantly srtraightforward how to split the data using several symbols and I put it on low-priority.

