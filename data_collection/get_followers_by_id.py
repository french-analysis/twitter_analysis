import time
import tweepy
from tweepy import OAuthHandler
from config import consumer_key, consumer_secret, access_token, access_secret

consumer_key = consumer_key
consumer_secret = consumer_secret
access_token = access_token
access_secret = access_secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

ids = []
for page in tweepy.Cursor(api.followers_ids, screen_name="@vbd2017").pages():
    ids.extend(page)
    #time.sleep(60)

print(ids)
