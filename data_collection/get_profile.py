import argparse
import time
import tweepy
from tweepy import OAuthHandler
from config import consumer_key, consumer_secret, access_token, access_secret

class user_profile():
    
    def __init__(self, screen_name = "@vbd2017"):
        self.screen_name  = screen_name
        self.followers    = []
        self.hashtags     = []
        
    def find_ids(self, screen_name):
        ids = []
        for page in tweepy.Cursor(twitter_api.followers_ids, screen_name=screen_name).pages():
            ids.extend(page)
            
    def get_lastmonth_activity():
        
        
    def export():
        
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
