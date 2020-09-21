import tweepy
import datetime
import time
import pandas as pd
import numpy as np
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys

# bring in bot
exec(open("tester.py").read())

out = pd.read_csv('../data/out.csv')
# out.to_csv('../data/baseline_checker.csv')
print(out.shape)
print(out.head())
print(out.dtypes)

consumer_key= '9C0nedFj98hB83LQCsW5xIDvZ' # Don't have these in the final
consumer_secret= 'J60uZyJ2JhZe0POGTdM7uUD6hno8kia42yg8TNBCIHHoUFS8l5'# Don't have these in the final
access_token= '1301167716456374272-F8USe9k5ztXa71US6qf3H5xlQvcx8Q'# Don't have these in the final
access_token_secret= 'jpsmsY6hddCUkzEIfyKLrGnOqk8nLSc3zMaWP9ugSpfYE'# Don't have these in the final

# Using the keys, setup the authorization
authorization = tweepy.OAuthHandler(consumer_key, consumer_secret)
authorization.set_access_token(access_token, access_token_secret)

# Add GPT-2 here

# out put of gpt-2 will got into {xi}

twitter = tweepy.API(auth)
for xi in range(out.shape[0]):
    twitter.update_status(f"@{out['username'][xi]} {xi}" , in_reply_to_status_id= out['id'][xi])
    time.sleep(200)
