import time
from datetime import datetime, date, timedelta
import GetOldTweets3 as got
import pandas as pd


def DownloadTweets(SinceDate, UntilDate, Location):
    '''
    Downloads all tweets from a certain month in three sessions in order to avoid sending too many requests. 
    Date format = 'yyyy-mm-dd'. 
    Query=string.
    '''
    since = datetime.strptime(SinceDate, '%Y-%m-%d')
    until = datetime.strptime(UntilDate, '%Y-%m-%d')
    tenth = since + timedelta(days=10)
    twentieth = since + timedelta(days=20)

    print('starting first download')
    first = got.manager.TweetCriteria().setNear(Location).setWithin('20000mi').setSince(
        since.strftime('%Y-%m-%d')).setUntil(tenth.strftime('%Y-%m-%d'))
    firstdownload = got.manager.TweetManager.getTweets(first)
    firstlist = [[tweet.date, tweet.text, tweet.username]
                 for tweet in firstdownload]

    df_1 = pd.DataFrame.from_records(firstlist, columns=["date", "tweet"])
    #df_1.to_csv("%s_1.csv" % SinceDate)

    time.sleep(600)

    print('starting second download')
    second = got.manager.TweetCriteria().setNear(Location).setWithin('20000mi').setSince(
        tenth.strftime('%Y-%m-%d')).setUntil(twentieth.strftime('%Y-%m-%d'))
    seconddownload = got.manager.TweetManager.getTweets(second)
    secondlist = [[tweet.date, tweet.text, tweet.username]
                  for tweet in seconddownload]

    df_2 = pd.DataFrame.from_records(secondlist, columns=["date", "tweet"])
    #df_2.to_csv("%s_2.csv" % SinceDate)

    time.sleep(600)

    print('starting third download')
    third = got.manager.TweetCriteria().setNear(Location).setWithin('20000mi').setSince(
        twentieth.strftime('%Y-%m-%d')).setUntil(until.strftime('%Y-%m-%d'))
    thirddownload = got.manager.TweetManager.getTweets(third)
    thirdlist = [[tweet.date, tweet.text, tweet.username]
                 for tweet in thirddownload]

    df_3 = pd.DataFrame.from_records(thirdlist, columns=["date", "tweet"])
    #df_3.to_csv("%s_3.csv" % SinceDate)

    df = pd.concat([df_1, df_2, df_3])
    df.to_csv("%s.csv" % SinceDate)

    return df


def getAllTweets(StartDate, EndDate, Location):
    curr_date = datetime.strptime(StartDate, '%Y-%m-%d')
    end_date = datetime.strptime(EndDate, '%Y-%m-%d')
    next_date = curr_date + timedelta(days=1)
    count = 1
    init_chunk = True
    while curr_date != end_date:
        print('Starting download {}'.format(count))
        crit = got.manager.TweetCriteria().setNear(Location).setWithin('20000mi').setSince(
            curr_date.strftime('%Y-%m-%d')).setUntil(next_date.strftime('%Y-%m-%d'))
        try:
            download = got.manager.TweetManager.getTweets(crit)
            downloadList = [[tweet.date, tweet.id, tweet.text, tweet.username, tweet.geo]
                            for tweet in download]

            temp = pd.DataFrame.from_records(
                downloadList, columns=["date", "id", "tweet", "user", "loc"])
            if init_chunk:
                temp.to_csv('./data.csv', index=False)
                init_chunk = False
            else:
                temp.to_csv('./data.csv', mode='a', index=False, header=False)
        except:
            print("Error date:", curr_date.strftime("%Y-%m-%d"))
            break
        finally:
            curr_date = curr_date + timedelta(days=1)
            next_date = next_date + timedelta(days=1)
            count = count + 1
            time.sleep(600)


if __name__ == "__main__":
    getAllTweets('2020-07-01', '2020-08-01', 'US')
