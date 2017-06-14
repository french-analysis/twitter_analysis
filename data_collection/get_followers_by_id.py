import time
import tweepy
from tweepy import OAuthHandler
from config import consumer_key, consumer_secret, access_token, access_secret
from pymongo import MongoClient

if __name__ == "__main__":

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    twitter_api = tweepy.API(auth)
    
    follower_ids = []
    for page in tweepy.Cursor(twitter_api.followers_ids, screen_name="@vbd2017").pages():
        follower_ids.extend(page)
        #time.sleep(60)
    
    with open('followers_ids.json', 'a') as f:
        f.write(" ".join(str(id) for id in follower_ids))
    print(follower_ids)

    client = MongoClient()
    db = client.twitter

    for id in follower_ids:
        db.followers.insert({str(id):'@vbd2017'})
