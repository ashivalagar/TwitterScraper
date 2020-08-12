import GetOldTweets3 as got
import tweepy
import pandas as pd
import datetime
import config as cfg

auth = tweepy.OAuthHandler(
    cfg.twitter_creds["consumer_key"], cfg.twitter_creds["consumer_secret"])
auth.set_access_token(
    cfg.twitter_creds["access_token"], cfg.twitter_creds["access_token_secret"])

api = tweepy.API(auth)

tweetCriteria = got.manager.TweetCriteria().setNear('US').setSince(
    '2020-07-01').setUntil('2020-08-01').setMaxTweets(1).setWithin('1000mi')
tweets = got.manager.TweetManager.getTweets(tweetCriteria)
final_tweets = list()
for tweet in tweets:
    curr_date = tweet.date.isoformat()
    user = tweet.username
    content = tweet.text
    userDetails = api.get_user(user)
    location = tweet.geo
    # print(userDetails.followers_count)
    final_tweets.append((curr_date, content, user, location))

print(final_tweets)
