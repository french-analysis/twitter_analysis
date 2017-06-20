import time
from pprint import pprint
from pymongo import MongoClient
import json

current_milli_time = lambda: int(round(time.time() * 1000))

if __name__ == "__main__":

    print("Connecting to Mongo database")
    client = MongoClient()
    db = client.twitter
    
    print("Read raw data text file")
    with open('../data_collection/files/twitter_stream_200617.txt') as tweets:
        for tweet in tweets:
            tweet = json.loads(tweet)
            try:
                print(tweet["id"], tweet["text"], tweet["created_at"])
            except BaseException as e:
                print(tweet)
            """db.followers.update(
                { 'followee' : target_userid, 'follower' : str(id) },
                {
                    '$set' : { 'last': current_milli_time() },
                    '$setOnInsert' : { 'first': current_milli_time() }
                },
                upsert = True, multi = True
    
            ) """
