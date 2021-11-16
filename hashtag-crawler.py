#!/usr/local/bin/python3.9

import tweepy
import csv
import pandas as pd
import datetime
import time
import sys
from collections import Counter, defaultdict

# Get the twitter credentials from a (hidden) file
secrets = open(".login")
login = secrets.readlines()

# assign the values accordingly
# strip the linebreak from the values to prevent bad login errors
consumer_key = login[0].rstrip('\n')
consumer_secret = login[1].rstrip('\n')
access_token = login[2].rstrip('\n')
access_token_secret = login[3].rstrip('\n')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


def leaders(hashtag, sorttweets, top=50):
    counts = defaultdict(int)
    for x in sorttweets:
        counts[x] += 1
    filename = f'{hashtag}_tweet_top50.csv'
    stand = sorted(counts.items(), reverse=True, key=lambda tup: tup[1])[:top]
    pd.DataFrame(stand).to_csv(filename, header=['Tweep', 'Aantal'])
    return stand

def writetweets(hashtag, tweets):
    filename = f"{hashtag}_tweets.csv"
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(["screen_name", "id", "created_at", "trucated text"])
        writer.writerows(tweets)

def getweets(hashtag, datum):
    outputfile = f"{hashtag}_tweets.csv"
    sortoutput = f"{hashtag}_tweets_sorted.csv"
    csvFile = open(outputfile, 'a')
    csvWriter = csv.writer(csvFile)

    hashtweets = []
    sorttweets = []
    hashtwit =f'#{hashtag}'
    for tweet in tweepy.Cursor(api.search, q = hashtwit,
            since=datum,count=200).items():
        try:
            sorttweets.append(tweet.user.screen_name)
            hashtweets.append([tweet.user.screen_name, tweet.id_str, tweet.created_at, tweet.text.encode('utf-8'),])
        except tweepy.TweepError:
            print('Sleep for a while')
            time.sleep(60 * 15)
            continue

    writetweets(hashtag, hashtweets)
    print(sorttweets)
    testing = leaders(hashtag, sorttweets)
    print(testing)
    

try:
    hashtek = sys.argv[1]
    datum = sys.argv[2]
    getweets(hashtek, datum)
except IndexError:
    print('no hashtag given')
