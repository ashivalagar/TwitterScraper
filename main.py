import GetOldTweets3 as got
import tweepy
import pandas as pd
import config as cfg
import time

def setUpTwitterAuth(cfg):
    '''
    Initialises the twitter api by passing our credentials to the api.

    We can add in our credentials in config.py.
    '''
    auth = tweepy.OAuthHandler(
    cfg.twitter_creds["consumer_key"], cfg.twitter_creds["consumer_secret"])
    auth.set_access_token(
    cfg.twitter_creds["access_token"], cfg.twitter_creds["access_token_secret"])
    api = tweepy.API(auth)


def setInitChunk(value):
    '''
    Set state function for init chunk.

    Controls whether a new csv is created or we append data to an existing csv.
    '''
    global init_chunk
    init_chunk = value


def setCounter(value):
    '''
    Set state function for tweet counter.

    Counter for the total number of tweets scraped for progress check while executing script.
    '''
    global total_tweets
    total_tweets = value
    print(total_tweets)


def setTimeOut(download):
    '''
    Callback function for writing scraped tweets into csv and setting the program to sleep to prevent error
    #429 too many requests.
    '''
    downloadList = list()
    print(len(download))

    for tweet in download:
        user = tweet.username
        # use tweepy to get user details and check for follower count.
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
    '''
    Setting the tweet scraping criteria and starting the getOldTweets3 scraping api.
    '''
    tweetCriteria = got.manager.TweetCriteria().setNear('US').setSince(
        '2020-07-01').setUntil('2020-08-01').setWithin('5000mi')

    tweets = got.manager.TweetManager.getTweets(
        tweetCriteria, receiveBuffer=setTimeOut, bufferLength=10000)


if __name__ == "__main__":
    setUpTwitterAuth(cfg)
    setInitChunk(True)
    getAllTweets()
