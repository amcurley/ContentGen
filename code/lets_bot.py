import tweepy
import os

# Read all the auth keys from environment variables
consumer_key= '9C0nedFj98hB83LQCsW5xIDvZ' # Don't have these in the final
consumer_secret= 'J60uZyJ2JhZe0POGTdM7uUD6hno8kia42yg8TNBCIHHoUFS8l5'# Don't have these in the final
access_token= '1301167716456374272-F8USe9k5ztXa71US6qf3H5xlQvcx8Q'# Don't have these in the final
access_token_secret= 'jpsmsY6hddCUkzEIfyKLrGnOqk8nLSc3zMaWP9ugSpfYE'# Don't have these in the final

# Using the keys, setup the authorization
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Create the API object
twitter = tweepy.API(auth)

# # Text Tweet
twitter.update_status("Test tweet")
#
# #Reply to a Tweet
# id_of_tweet_to_reply = "945049796238118912"
# twitter.update_status("Reply to a tweet using #tweepy", in_reply_to_status_id=id_of_tweet_to_reply)
