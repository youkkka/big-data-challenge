# from sys import api_version
# from kafka import SimpleProducer
import pykafka
# import json
import tweepy
from tweepy import OAuthHandler, OAuth1UserHandler
from tweepy import Stream, StreamRule
import twitter_keys

#TWITTER API CONFIGURATIONS
# consumer_key = twitter_keys.consumer_key
# consumer_secret = twitter_keys.consumer_secret
# access_token = twitter_keys.access_token
# access_secret = twitter_keys.access_secret

bearer_token = twitter_keys.bearer_token

# TWITTER API AUTH
# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_secret)

# auth = OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_secret)

# api = tweepy.API(auth)

#Twitter Stream Listener
class KafkaPushListener(tweepy.StreamingClient):
    def __init__(self, *args):
        super().__init__(*args)
        #localhost:9092 = Default Zookeeper Producer Host and Port Adresses
        self.client = pykafka.client.KafkaClient('kafka:9092')

        #Get Producer that has topic name is Twitter
        self.producer = self.client.topics[bytes("twitter", "ascii")].get_producer()
        # self.producer = pykafka.Producer(self.client, b'twitter-stream')

    def on_data(self, data):
		#Producer produces data for consumer
		#Data comes from Twitter
        # print(data)
        self.producer.produce(data)
        # self.producer.produce(bytes(data, "ascii"))
        return True
                                                                                                                                           
    def on_error(self, status):
        print(status)
        return True

    def on_status(self, status):
        print(status.id)

#Twitter Stream Config
# twitter_stream = Stream(auth, KafkaPushListener())
# twitter_stream = Stream(auth, KafkaPushListener(consumer_key, consumer_secret, access_token, access_secret))

# twitter_stream = KafkaPushListener(consumer_key, consumer_secret, access_token, access_secret)
twitter_stream = KafkaPushListener(bearer_token)
print(twitter_stream.get_rules())
# twitter_stream.delete_rules(ids=[])
twitter_stream.add_rules(StreamRule('(happy OR happiness OR excited OR elated) lang:en -birthday -is:retweet -holidays'))
print(twitter_stream.get_rules())

twitter_stream.filter()
# twitter_stream.sample()

# twitter_stream = Stream(consumer_key, consumer_secret, access_token, access_secret)

# twitter_stream.filter(track=['#Tweepy'])