from collections import Counter
from pymongo import MongoClient
from pprint import pprint

def connect_Mongo():
    print("Connecting to Mongo database")
    client = MongoClient()
    return client.twitter

def clean(hashtag):
    return hashtag.lower()


def get_hashtags(db):
    hashtags = []
    for tweet in db.tweets.find():
        #hashtags += [clean(hashtag) for hashtag in tweet["hashtags"]]
        hashtags += tweet["hashtags"] 
    return hashtags

if  __name__ == "__main__":

    db = connect_Mongo()
    print(Counter(get_hashtags(db)).most_common(10))
