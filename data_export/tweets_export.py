import time
from pprint import pprint
from pymongo import MongoClient
import json
import time

if __name__ == "__main__":

    print("Connecting to Mongo database")
    client = MongoClient()
    db = client.twitter
    
    print("Read raw data text file")
    with open('../data_collection/files/twitter_stream_200617.txt') as tweets:
        for tweet in tweets:
            tweet = json.loads(tweet)
            if 'retweeted_status' in tweet:
                try:
                    print(tweet["id"], tweet["text"], tweet["created_at"])
                    db.tweets.update(
                        { 'id' : str(tweet["id"]) },
                        {
                            '$set' : { 
                                       'user': tweet["user"]["id_str"],
                                       'text': tweet["text"], 
                                       'created_at': time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet["created_at"],'%a %b %d %H:%M:%S +0000 %Y')),
                                       'hashtags' : [str(hashtag["text"]) for hashtag in tweet["entities"]["hashtags"]],
                                       'urls' : [str(urls["expanded_url"]) for urls in tweet["entities"]["urls"]],
                                       'mentions_user' : [str(mention["id"]) for mention in list(tweet["entities"]["user_mentions"])],
                                       'retweeted_user' : str(tweet["retweeted_status"]["user"]["id_str"]),
                                       'lang' : tweet["lang"]
                                     }
                        },
                        upsert = True, multi = True
    
                    )
                except BaseException as e:
                    if 'retweeted_status' not in tweet:
                        print("True")
                    print(e, pprint(tweet))
            else:
                try:
                    print(tweet["id"], tweet["text"], tweet["created_at"])
                    db.tweets.update(
                        { 'id' : str(tweet["id"]) },
                        {
                            '$set' : { 
                                       'user': tweet["user"]["id_str"],
                                       'text': tweet["text"], 
                                       'created_at': time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet["created_at"],'%a %b %d %H:%M:%S +0000 %Y')),
                                       'hashtags' : [str(hashtag["text"]) for hashtag in tweet["entities"]["hashtags"]],
                                       'urls' : [str(urls["expanded_url"]) for urls in tweet["entities"]["urls"]],
                                       'mentions_user' : [str(mention["id"]) for mention in list(tweet["entities"]["user_mentions"])],
                                       'retweeted_user' : "",
                                       'lang' : tweet["lang"]
                                     }
                        },
                        upsert = True, multi = True
    
                    )
                except BaseException as e:
                    if 'retweeted_status' not in tweet:
                        print("True")
                    print(e, pprint(tweet))
