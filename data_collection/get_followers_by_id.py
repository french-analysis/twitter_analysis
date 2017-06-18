import time
import tweepy
from tweepy import OAuthHandler
from config import consumer_key, consumer_secret, access_token, access_secret
from pymongo import MongoClient

current_milli_time = lambda: int(round(time.time() * 1000))
target_userid = '376252824'

if __name__ == "__main__":

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    twitter_api = tweepy.API(auth)
    
    follower_ids = []
    for page in tweepy.Cursor(twitter_api.followers_ids, user_id = target_userid).pages():
        follower_ids.extend(page)

    print([str(id) for id in follower_ids])

    print("Connecting to Mongo database")
    client = MongoClient()
    db = client.twitter

    print('Start insertion')
    for id in follower_ids:
        db.followers.update(
            { 'followee' : target_userid, 'follower' : str(id) },
            { 
                '$set' : { 'last': current_milli_time() },
                '$setOnInsert' : { 'first': current_milli_time() }
            },
            upsert = True, multi = True
            
        )
        
    print('Updated %s followers for user %s' % (len(follower_ids), target_userid))
    
