import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('kafka')
install('pykafka')
install('tweepy')
# install('pyspark==2.4.6')

import kafka_push_listener
# import kafka_twitter_spark_streaming

# import twitter_api

# import example_producer