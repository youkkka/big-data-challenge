import pykafka
import tweepy
from tweepy import Stream, StreamRule
import twitter_keys

bearer_token = twitter_keys.bearer_token


#Twitter Stream Listener
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

print(twitter_stream.get_rules())
# twitter_stream.delete_rules(ids=['1563977449230286850'])
twitter_stream.add_rules(StreamRule('(happy OR happiness OR excited OR elated) lang:en -birthday -is:retweet -holidays'))
print(twitter_stream.get_rules())

twitter_stream.filter()