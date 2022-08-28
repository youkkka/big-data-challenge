import tweepy
import configparser
import twitter_keys

config = configparser.ConfigParser()
config.read('config.ini')

# consumer_key = config['twitter']['consumer_key']
# consumer_secret = config['twitter']['consumer_secret']
# access_token = config['twitter']['access_token']
# access_secret = config['twitter']['access_secret']
# bearer_token = config['twitter']['bearer_token']

consumer_key = twitter_keys.consumer_key
consumer_secret = twitter_keys.consumer_secret
access_token = twitter_keys.access_token
access_secret = twitter_keys.access_secret
bearer_token = twitter_keys.bearer_token

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

public_tweets = api.get_followers()

for t in public_tweets:
    print(t.text)