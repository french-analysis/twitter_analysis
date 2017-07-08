from collections import Counter
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime, timedelta
import json
last1HourDateTime = datetime.now() - timedelta(hours = 1)
last3HourDateTime = datetime.now() - timedelta(hours = 3)
last6HourDateTime = datetime.now() - timedelta(hours = 6)
last12HourDateTime = datetime.now() - timedelta(hours = 12)
last24HourDateTime = datetime.now() - timedelta(hours = 24)

def connect_Mongo_twitter():
    print("Connecting to Mongo twitter database")
    client = MongoClient()
    return client.twitter

def connect_Mongo_prod():
    print("Connecting to Mongo prod database")
    client = MongoClient()
    return client.prod

def clean(hashtag):
    return hashtag.lower()


def get_hashtags(db):
    last_1hour_hashtags = []
    last_3hour_hashtags = []
    last_6hour_hashtags = []
    last_12hour_hashtags = []
    last_24hour_hashtags = []
    all_hashtags = []
    for tweet in db.tweets.find({}):
        #hashtags += [clean(hashtag) for hashtag in tweet["hashtags"]]
        """if tweet["created_at"] > last1HourDateTime.strftime('%Y-%m-%d %H:%M:%S'):
            last_1hour_hashtags += tweet["hashtags"]
            pprint(tweet)
        if tweet["created_at"] > last3HourDateTime.strftime('%Y-%m-%d %H:%M:%S'):
            last_3hour_hashtags += tweet["hashtags"]
            pprint(tweet)
        if tweet["created_at"] > last6HourDateTime.strftime('%Y-%m-%d %H:%M:%S'):
            last_6hour_hashtags += tweet["hashtags"]
            pprint(tweet)
        if tweet["created_at"] > last12HourDateTime.strftime('%Y-%m-%d %H:%M:%S'):
            last_12hour_hashtags += tweet["hashtags"]
        if tweet["created_at"] > last24HourDateTime.strftime('%Y-%m-%d %H:%M:%S'):
            last_24hour_hashtags += tweet["hashtags"]"""
        all_hashtags += tweet["hashtags"]
    #return [last_1hour_hashtags, last_3hour_hashtags, last_6hour_hashtags, last_12hour_hashtags, last_24hour_hashtags, all_hashtags]
    return [all_hashtags]

def export_hashtags_prod(id, hashtags, db):
    db.hashtags.update(
        { 'id' : str(id) },
        {
            '$set' : { 'hashtags' : hashtags }
        },
        upsert = True)
    return

def format_export(counter_list):
    export = []
    for element in counter_list:
        formatted = {
            'hashtag' : element[0],
            'count' : element[1]
        } 
        export.append(formatted)
    return export

if  __name__ == "__main__":

    main_id = "864042284505063424"

    twitter = connect_Mongo_twitter()
    counter_export = Counter(get_hashtags(twitter)[0]).most_common(15)
    print(format_export(counter_export))

    prod = connect_Mongo_prod()
    export_hashtags_prod(main_id, json.dumps(format_export(counter_export)), prod)


