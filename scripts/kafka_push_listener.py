import pykafka
import tweepy
import twitter_keys
import json

bearer_token = twitter_keys.bearer_token

class KafkaPushListener(tweepy.StreamingClient):
    def __init__(self, *args):
        super().__init__(*args)
        self.client = pykafka.client.KafkaClient('kafka:9092')
        self.producer = self.client.topics[bytes("twitter", "ascii")].get_producer()

    def on_data(self, data):
        print(data)
        self.producer.produce(data)
        return True
                                                                                                                                           
    def on_error(self, status):
        print(status)
        return True

    def on_status(self, status):
        print(status.id)

twitter_stream = KafkaPushListener(bearer_token)

# print(twitter_stream.get_rules())
# twitter_stream.delete_rules(ids=['1564004005008875523', '1563995451443085317'])
twitter_stream.add_rules(tweepy.StreamRule('(mother OR father) lang:en -is:retweet'))
# print(twitter_stream.get_rules())

twitter_stream.filter()