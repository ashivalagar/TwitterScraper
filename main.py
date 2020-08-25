import GetOldTweets3 as got
import tweepy
import pandas as pd
import datetime
import config as cfg
import time

auth = tweepy.OAuthHandler(
    cfg.twitter_creds["consumer_key"], cfg.twitter_creds["consumer_secret"])
auth.set_access_token(
    cfg.twitter_creds["access_token"], cfg.twitter_creds["access_token_secret"])

api = tweepy.API(auth)


def setInitChunk(value):
    global init_chunk
    init_chunk = value


def setCounter(value):
    global total_tweets
    total_tweets = value
    print(total_tweets)


def setTimeOut(download):
    downloadList = list()
    print(len(download))

    for tweet in download:
        user = tweet.username
        userDetails = api.get_user(user)
        if (userDetails.followers_count >= 100000):
            downloadList.append(
                [tweet.date, tweet.id, tweet.text, user, tweet.geo])

    temp = pd.DataFrame.from_records(
        downloadList, columns=["date", "id", "tweet", "user", "loc"])
    if init_chunk:
        setCounter(len(downloadList))
        temp.to_csv('./data/data.csv', index=False)
        setInitChunk(False)
    else:
        setCounter(total_tweets+len(downloadList))
        temp.to_csv('./data/data.csv', mode='a', index=False, header=False)
    print("Starting timeout")
    for i in range(10):
        time.sleep(45)
        print("{} sleep completed".format(i+1))
    print("TImeout end")


def getAllTweets():
    tweetCriteria = got.manager.TweetCriteria().setNear('US').setSince(
        '2020-07-01').setUntil('2020-08-01').setWithin('5000mi')

    tweets = got.manager.TweetManager.getTweets(
        tweetCriteria, receiveBuffer=setTimeOut, bufferLength=10000)


if __name__ == "__main__":
    setInitChunk(True)
    getAllTweets()
