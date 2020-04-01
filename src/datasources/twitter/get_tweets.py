
import tweepy
from src.datasources.twitter.configs.creds import *
from pymongo import MongoClient
from src.common import db_config as config

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):

    def __init__(self):
        self.db_client = MongoClient(port=27017)
        self.db = self.db_client[config.db_name]
        super(MyStreamListener, self).__init__()
        return
    
    def on_status(self, status):
        print(status.text)
        self.db["covid19_tweets_4"].insert_one(status._json, config.coll)

    def on_error(self, status_code):
        if status_code == 420:
            return False
        

mystreamlistener = MyStreamListener()
my_stream = tweepy.Stream(auth = api.auth, listener=mystreamlistener)
my_stream.filter(track = ['#covid19au'], is_async = True)

'''
t = test()
t.fetch_tweets()
class test(object):

    def __init__(self):
        self.db_client = MongoClient(port=27017)
        self.db = self.db_client[config.db_name]

        return

    def fetch_tweets(self):
        public_tweets = api.home_timeline()
        for tweet in public_tweets[:10]:
            print(tweet.text)
            self.db['covid19_tweets'].insert_one(tweet._json, config.coll)

        return
'''
