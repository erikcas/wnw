#!/usr/local/bin/python3.9

import tweepy
import csv
import pandas as pd
from datetime import datetime
import sys
from collections import defaultdict
from tag_hourly import tag_data, plot_data
from printer import print_table
from post import post_twitter

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
    filename = f'temp_{hashtag}_tweet_top50.csv'
    uploadfile = f'{hashtag}_tweet_top50.csv'
    stand = sorted(counts.items(), reverse=True, key=lambda tup: tup[1])[:top]
    pd.DataFrame(stand).to_csv(filename, header=['Tweep', 'Aantal'])
    # TODO: simplify this, remove initial row
    with open(filename, 'r') as r:
        reader = csv.reader(r)
        with open(uploadfile, 'w') as w:
            writer = csv.writer(w)
            for r in reader:
                writer.writerow((r[1], r[2]))

def writetweets(hashtag, tweets):
    filename = f"{hashtag}_tweets.csv"
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["screen_name", "id", "created_at", "trucated text"])
        writer.writerows(tweets)

def getweets(hashtag, datumi, tabel):
    hashtweets, sorttweets, datatweets = [], [], []
    twitter_datum = datetime.strptime(datum, '%d-%m-%Y').strftime('%Y-%m-%d')

    hashtwit =f'#{hashtag}'
    counter = 0
    for tweet in tweepy.Cursor(api.search, q = hashtwit,
            since=twitter_datum,count=200).items():
        try:
            # De gebruikers voor de tussenstand
            sorttweets.append(tweet.user.screen_name)
            # De tweettijden voor de leuke grafiekjes
            temptijd = tweet.created_at
            temptijd = temptijd.replace(minute=0, second=0)
            datatweets.append(temptijd)
            # De totaal info
            hashtweets.append([tweet.user.screen_name, tweet.id_str, tweet.created_at, tweet.text.encode('utf-8'),])
        except tweepy.TweepError:
            print('Sleep for a while')
            time.sleep(60 * 15)
            continue
        counter += 1

    writetweets(hashtag, hashtweets)
    tag_data(hashtag, datatweets)
    plot_data(hashtag, datatweets, datum)
    leaders(hashtag, sorttweets)
    if tabel == 'yes':
        print_table(hashtag, sorttweets)
    post_twitter(hashtag, counter, tabel, datum)
    

try:
    hashtek = sys.argv[1]
    datum = sys.argv[2]
    if sys.argv[3]:
        tabel = sys.argv[3]
    else:
        tabel = 'no'
    getweets(hashtek, datum, tabel)
except IndexError:
    print('no hashtag given')
