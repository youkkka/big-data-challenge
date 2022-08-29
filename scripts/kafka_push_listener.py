import pykafka
import tweepy
import twitter_keys
import json

# token from twitter api
bearer_token = twitter_keys.bearer_token

class KafkaPushListener(tweepy.StreamingClient):
    def __init__(self, *args):
        super().__init__(*args)
        # get client from kafka container
        self.client = pykafka.client.KafkaClient('kafka:9092')
        # get producer with topic twitter
        self.producer = self.client.topics[bytes("twitter", "ascii")].get_producer()

    def on_data(self, data):
        # print what we got
        print(data)
        # produce what we got
        self.producer.produce(data)
        return True
                                                                                                                                           
    def on_error(self, status):
        print(status)
        return True

    def on_status(self, status):
        print(status.id)

# initialize stream
twitter_stream = KafkaPushListener(bearer_token)

# some commented lines to manage the rules, they are stored in twitter api
# print(twitter_stream.get_rules())
# twitter_stream.delete_rules(ids=['1564249362288590849'])

# all tweets that have one or the other in english not reposted
twitter_stream.add_rules(tweepy.StreamRule('(apple OR orange) lang:en -is:retweet'))
# print(twitter_stream.get_rules())
twitter_stream.filter()