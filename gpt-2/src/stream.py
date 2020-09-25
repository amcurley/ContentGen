import tweepy
import datetime
import time
# import pandas as pd
# import numpy as np
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys

consumer_key= '9C0nedFj98hB83LQCsW5xIDvZ' # Don't have these in the final
consumer_secret= 'J60uZyJ2JhZe0POGTdM7uUD6hno8kia42yg8TNBCIHHoUFS8l5'# Don't have these in the final
access_token= '1301167716456374272-F8USe9k5ztXa71US6qf3H5xlQvcx8Q'# Don't have these in the final
access_token_secret= 'jpsmsY6hddCUkzEIfyKLrGnOqk8nLSc3zMaWP9ugSpfYE'# Don't have these in the final

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        is_retweet = hasattr(status, "retweeted_status")
        if is_retweet: # If the tweet has the attribute "retweeted_status" pass
            pass
        else:
            is_quote = hasattr(status, "quoted_status")
            if is_quote: # If the tweet has the attribute "quoted_status" pass
                pass
            else:
                # Extend tweet so it shows all 280 characters
                if hasattr(status,"extended_tweet"):
                    text = status.extended_tweet["full_text"]
                else:
                    text = status.text

                remove_characters = [",","#","\n"]
                for c in remove_characters:
                    text = text.replace(c," ")

                return status.user.screen_name, status.id_str, text, stream.disconnect()

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()

if __name__ == "__main__":
    # Complete authorization and initialize API endpoint
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Initialize stream
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener,tweet_mode='extended')

    tags = ['food', 'hungry', 'I am hungry']
    stream.filter(track = tags, languages=['en'])
