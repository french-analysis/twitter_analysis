from collections import Counter
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime, timedelta
last12HourDateTime = datetime.now() - timedelta(hours = 12)
last24HourDateTime = datetime.now() - timedelta(hours = 24)
last48HourDateTime = datetime.now() - timedelta(hours = 48)
last72HourDateTime = datetime.now() - timedelta(hours = 72)

def connect_Mongo():
    print("Connecting to Mongo database")
    client = MongoClient()
    return client.twitter

def get_urls(db):
    last_12hour_urls = []
    last_24hour_urls = []
    last_48hour_urls = []
    last_72hour_urls = []
    all_urls = []
    for tweet in db.tweets.find({}):
        #urls += [clean(hashtag) for hashtag in tweet["urls"]]
        if tweet["created_at"] > last12HourDateTime.strftime('%Y-%m-%d %H:%M:%S'):
            last_12hour_urls += tweet["urls"]
        if tweet["created_at"] > last24HourDateTime.strftime('%Y-%m-%d %H:%M:%S'):
            last_24hour_urls += tweet["urls"]
        if tweet["created_at"] > last48HourDateTime.strftime('%Y-%m-%d %H:%M:%S'):
            last_48hour_urls += tweet["urls"]
        if tweet["created_at"] > last72HourDateTime.strftime('%Y-%m-%d %H:%M:%S'):
            last_72hour_urls += tweet["urls"]
        all_urls += tweet["urls"]
    return [last_12hour_urls, last_24hour_urls, last_48hour_urls, last_72hour_urls, all_urls]

if  __name__ == "__main__":

    db = connect_Mongo()
    list_hours = [12, 24, 48, 72, "all"]
    for delta, urls in zip(list_hours, get_urls(db)):
        print("URLS over the last", delta, "hours : ", Counter(urls).most_common(10))
