import tweepy

# Get the twitter credentials from a (hidden) file
secrets = open(".logincas")
login = secrets.readlines()

# assign the values accordingly
# strip the linebreak from the values to prevent bad login errors
consumer_key = login[0].rstrip('\n')
consumer_secret = login[1].rstrip('\n')
access_token = login[2].rstrip('\n')
access_token_secret = login[3].rstrip('\n')

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)

# calling the api
api = tweepy.API(auth)

def post_twitter(hashtag, hashtag2, counter, counter2, datum):
    text = f'#{hashtag} vs #{hashtag2} fun facts!!\n\n \
    Datum sinds: {datum}\n\n  \
    Aantal tweets: #{hashtag} {counter}\n \
    Aantal tweets: #{hashtag2} {counter2}\n\n \
    Volg ook @inter_crap voor breaking news!'

    media_ids = []
    png1 = f'{hashtag}_vs_{hashtag2}_tweet_graph.png'
    filenames = [png1]
    for filename in filenames:
        res = api.media_upload(filename)
        media_ids.append(res.media_id)

    api.update_status(status=text, media_ids=media_ids)
    print(text)
