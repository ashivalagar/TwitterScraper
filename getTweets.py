import time
from datetime import datetime, date, timedelta
import GetOldTweets3 as got
import pandas as pd
from threading import Thread

init_chunk = True


def setLocation(state):
    global location_state
    location_state = state
    print(state)


def setInitChunk(value):
    global init_chunk
    init_chunk = value


def setCounter(value):
    global total_tweets
    total_tweets = value
    print(total_tweets)


def setTimeOut(download):
    downloadList = [[tweet.date, tweet.id, tweet.text, tweet.username, tweet.geo, location_state]
                    for tweet in download]
    temp = pd.DataFrame.from_records(
        downloadList, columns=["date", "id", "tweet", "user", "loc", "loc_assigned"])
    print(init_chunk)
    if init_chunk:
        setCounter(len(downloadList))
        temp.to_csv('./data/data.csv', index=False)
        setInitChunk(False)
    else:
        setCounter(total_tweets+len(downloadList))
        temp.to_csv('./data/data.csv', mode='a', index=False, header=False)
    print("Starting timeout")
    for i in range(10):
        time.sleep(60)
        print("{} sleep completed".format(i+1))
    print("TImeout end")


def getAllTweets(StartDate, EndDate, Location):
    curr_date = datetime.strptime(StartDate, '%Y-%m-%d')
    end_date = datetime.strptime(EndDate, '%Y-%m-%d')
    next_date = curr_date + timedelta(days=1)
    count = 1
    while curr_date != end_date:
        print('Starting download {}'.format(count))
        crit = got.manager.TweetCriteria().setNear(Location).setWithin('750mi').setSince(
            curr_date.strftime('%Y-%m-%d')).setUntil(next_date.strftime('%Y-%m-%d'))
        try:
            print("check 1")
            download = got.manager.TweetManager.getTweets(
                crit, receiveBuffer=setTimeOut, bufferLength=10000)
            print("check 2")
        except:
            print("Error date:", curr_date.strftime("%Y-%m-%d"))
            break

        curr_date = curr_date + timedelta(days=1)
        next_date = next_date + timedelta(days=1)
        count = count + 1


if __name__ == "__main__":
    setInitChunk(True)
    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
              "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
    for i in states:
        setLocation(i)
        getAllTweets('2020-07-01', '2020-08-01', i)

    # getAllTweets('2020-07-01', '2020-08-01', "AL")
