import tweepy
from tweepy import OAuthHandler
from config import consumer_key, consumer_secret, access_token, access_secret
from tweepy import Stream
from tweepy.streaming import StreamListener

class tweetListener(StreamListener): 

    def __init__(self, max_num_tweets):
        self.counter = 0
        self.max_num_tweets = max_num_tweets

    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data['text'])
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True

if __name__ == "__main__":

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    twitter_api = tweepy.API(auth)

    # Search stuff
    search_results = tweepy.Cursor(twitter_api.search, q="Python").items(5)
    for result in search_results:
        print(result.text)

    trends = twitter_api.trends_place(1)

    for trend in trends[0]["trends"]:
        print(trend['name'])

    twitter_stream = Stream(auth, twitter_listener(num_tweets_to_grab=10))
    try:
        twitter_stream.sample()
    except Exception as e:
        print(e.__doc__) 
