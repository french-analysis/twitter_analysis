import time
from pprint import pprint
from pymongo import MongoClient
import json

current_milli_time = lambda: int(round(time.time() * 1000))

if __name__ == "__main__":

    print("Read raw data text file")
    with open('../data_collection/files/twitter_stream_200617.txt') as tweets:
        for tweet in tweets:
            tweet = json.loads(tweet)
            pprint(tweet)

