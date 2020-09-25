import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
import sys

consumer_key= 'hi' # Don't have these in the final
consumer_secret= 'hi'# Don't have these in the final
access_token= 'hi'# Don't have these in the final
access_token_secret= 'hi'

authorization = tweepy.OAuthHandler(consumer_key, consumer_secret)
authorization.set_access_token(access_token, access_token_secret)

twitter = tweepy.API(authorization, wait_on_rate_limit=True)

def input():
    tweets = tweepy.Cursor(twitter.search,
                           q = 'food',
                           lang='en').items(1)

    return print([tweet.text for tweet in tweets])

input()
