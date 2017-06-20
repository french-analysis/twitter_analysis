from pymongo import MongoClient
import time

current_milli_time = lambda: int(round(time.time() * 1000))

with open('twitter_stream.txt') as myfile:
    head = [next(myfile) for x in range(10)]
print(head)
