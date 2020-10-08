# Scraping Macro User Tweets

![TwitterLogo](https://articles-images.sftcdn.net/wp-content/uploads/sites/3/2017/05/twitter-logo-small-fade-1920.png)

## Introduction

### What is a macro user?

A macro user in the case of this project is defined as any user that has greater than 100,000 followers but less than 1,000,000 users.

### Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

1. Clone the repository.
2. From the root directory of the cloned repository you can install all dependencies required by running the following command,

```
pip install -r requirements.txt
```

3. Add in your twitter api credentials into config.py. Details on how to do this is detailed later in this repository. Also add config.py to .gitignore before commiting to github to protect your credentials.
4. You can now run the scraper as follows,

```
python main.py
```

This will scrape all the tweets by macro users from the US from the 1st of July to the 31st of July.

### Editable Parameters

You can change the scraping parameters in main.py by editing the following function,

```python
def getAllTweets():
    '''
    Setting the tweet scraping criteria and starting the getOldTweets3 scraping api.
    '''
    tweetCriteria = got.manager.TweetCriteria().setNear('US').setSince('2020-07-01').setUntil('2020-08-01').setWithin('5000mi')

    tweets = got.manager.TweetManager.getTweets(tweetCriteria,receiveBuffer=setTimeOut,bufferLength=10000)
```

```
setNear - Location of the tweets
setSince - Date from which to scrape
setUntil - Date to which to scrape
setWithin - Set a range around the location as buffer
bufferLength - Chunks in which to scrape tweets at a time. The callback function is called everytime after 10,000 tweets are scraped.
```

---

## Background

### What is an API ?

API stands for application programming interface. In basic terms, APIs just allows application to communicate with another.
API allows us to get data from outside sources.

1. We can send an API a request detailing the information we want.
2. APIs allows our sites to alter data on other applications, too. For instance, you’ve probably seen “Share on Facebook” or “Share on Twitter” buttons on miscellaneous websites. When/if you click one of these buttons, the site you’re visiting can communicate with your Facebook or Twitter account, and alter its data by adding new status or tweet.

### So how to get THe API for twitter ? <br />

<b>step 1:</b> Go to the twitter's developer website,
[Twitter Developer site](https://developer.twitter.com/content/developer-twitter/en.html)<br />
<b>step 2:</b> Sign in to the account and go to the apps menu.<br />
<b>step 3:</b> Select create an app and complete the instructions on screen.<br />
<b>step 4:</b> After completing the entire procedure, go to app details and view the keys and token tab.<br />
<b>step 5:</b> Copy the following into the program config.py<br />
<t>Consumer API key ===> twitter_creds['Consumer_key']</t><br />
Consumer API secret key ===> twitter_creds['Consumer_secret']<br />
Access token ===> twitter_creds['Access_token']<br />
Access token secret ===> twitter_creds['Access_key']<br />

---

_References: https://towardsdatascience.com/how-to-scrape-tweets-from-twitter-59287e20f0f1_
