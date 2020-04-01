
import tweepy
from src.datasources.twitter.configs.creds import *
from pymongo import MongoClient
from src.common import db_config as config

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


class retrieve_tweets(object):

    def __init__(self):
        self.db_client = MongoClient(port=27017)
        self.db = self.db_client[config.db_name]
        return

    def fetch_tweets(self, coll="covid19_tweets_3"):
        op = list(self.db[coll].find({}))
        return op

rt = retrieve_tweets()
op =rt.fetch_tweets()
print(len(op))

   
        
