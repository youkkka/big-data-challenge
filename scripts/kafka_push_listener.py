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
# twitter_stream.delete_rules(ids=['1564004005008875523', '1563995451443085317'])

# all tweets that have mother or father in english not reposted
twitter_stream.add_rules(tweepy.StreamRule('(mother OR father) lang:en -is:retweet'))

twitter_stream.filter()