import random
import sys
import subprocess
import time
import datetime

start_time = time.time()

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

print(file_len('data_collection/data/twitter_stream_aa'))
