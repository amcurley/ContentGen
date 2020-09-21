
import tweepy
import datetime
import time
import pandas as pd
import numpy as np
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys

np.random.seed(42)

consumer_key= '9C0nedFj98hB83LQCsW5xIDvZ' # Don't have these in the final
consumer_secret= 'J60uZyJ2JhZe0POGTdM7uUD6hno8kia42yg8TNBCIHHoUFS8l5'# Don't have these in the final
access_token= '1301167716456374272-uzu12HXwfz4ibViifjX4k0oMyJtGGn'# Don't have these in the final
access_token_secret= 'ELaOZdOQwi02S1olN4SHQo55h0VseazfUumuOmLTEDwno'# Don't have these in the final

class StreamListener(tweepy.StreamListener):

    tweet_counter = 0 # Max tweet counter

    def on_status(self, status):

        count = 2 # This is to pull in only 1 tweet per loop so we do not get rate limited
        while count > 1:
            is_retweet = hasattr(status, "retweeted_status")
            if is_retweet: # If the tweet has the attribute "retweeted_status" pass
                pass
            else:
                is_quote = hasattr(status, "quoted_status")
                if is_quote: # If the tweet has the attribute "quoted_status" pass
                    pass
                else:
                    print(status.id_str) # The id of the tweets that we pull
                    # Extend tweet so it shows all 280 characters
                    if hasattr(status,"extended_tweet"):
                        text = status.extended_tweet["full_text"]
                    else:
                        text = status.text
                    # Remove characters that might cause problems with csv encoding
                    remove_characters = [",","#","\n"]
                    for c in remove_characters:
                        text = text.replace(c," ")

                    with open("../data/out.csv", "a", encoding='utf-8') as f:
                        f.write("%s,%s,%s,%s\n" % (status.user.screen_name,is_retweet,text, status.user.location)) # Need to fix this

            count -= 1

# Enter the maximum amount of tweets you want to pull below

            if StreamListener.tweet_counter <= 28: #This number plus 2 is the MAX amount of tweets it will pull!
                StreamListener.tweet_counter += 1
                pass
            else:
                stream.disconnect() # Disconnect stream when loop is finished


        time.sleep(2)
        count += 1

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
    with open("../data/out.csv", "w", encoding='utf-8') as f:
        f.write("user,is_retweet,tweet,location, state, state_1\n")

    tags = ['power went out', 'power outage', 'poweroutage', 'I have no power',
            'con edison', 'conedison']
    stream.filter(track = tags)
