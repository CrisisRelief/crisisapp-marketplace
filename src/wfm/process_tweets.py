
import tweepy
from src.datasources.twitter.configs.creds import *
from pymongo import MongoClient
from src.common import db_config as config
import json

from src.nlp.pre_process import preprocess
from src.nlp import token_matcher as tm

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


class retrieve_tweets(object):

    def __init__(self):
        self.db_client = MongoClient(port=27017)
        self.db = self.db_client[config.db_name]
        fp = open("acc_match.json", "a")
        self.pp = preprocess()
        return

    def fetch_tweets(self, coll="covid19_tweets"):
        op = list(self.db[coll].find({}))
        return op

    def process_tweets(self):
        processed_tweets = []
        
        op = self.fetch_tweets()

        for tweet in op:

            if 'retweeted_status' in tweet.keys() and tweet['retweeted_status']:
                if 'extended_tweet' in tweet['retweeted_status'].keys():
                    text = tweet['retweeted_status']['extended_tweet']['full_text']
                else:
                    text = tweet['retweeted_status']['text']
                id = tweet['retweeted_status']['id']
            elif 'extended_tweet' in tweet.keys():
                text = tweet['extended_tweet']['full_text']
                id = tweet['id']
            else:
                text = tweet['text']
                id = tweet['id']
                
            #this is to avoid processing retweets
            if id in processed_tweets:
                continue

            cleansed_tweet = self.pp.lemmatize(text)
            results = tm.detect_patterns([cleansed_tweet])
            if results:
                match = {}
                match['tweet_id'] = tweet['id_str']
                match['results'] = results
                match['text'] = text
                processed_tweets.append(id)
                with open("pickup_results.json", "a") as fp:
                    json.dump(match, fp)
                    fp.close()

   
        
rt = retrieve_tweets()
rt.process_tweets()
