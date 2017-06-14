import time
import tweepy
from tweepy import OAuthHandler
from config import consumer_key, consumer_secret, access_token, access_secret

if __name__ == "__main__":

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    twitter_api = tweepy.API(auth)
    
    ids = []
    for page in tweepy.Cursor(twitter_api.followers_ids, screen_name="@vbd2017").pages():
        ids.extend(page)
        #time.sleep(60)
    
    with open('followers_ids.json', 'a') as f:
        f.write(''.join(str(e) for e in ids))
    print(ids)
