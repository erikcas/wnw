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

def post_twitter(hashtag, counter, tabel):
    text = f'#{hashtag} fun facts\n\n \
        Aantal tweets: {counter}\n \
        Top 10 posters en grafische historie in de plaatjes hieronder\n\n \
        Volg ook @inter_crap voor breaking news!'

    media_ids = []
    png1 = f'{hashtag}_tweet_top10.png'
    png2 = f'{hashtag}_tweet_graph.png'
    if tabel == 'yes':
        filenames = [png1, png2]
    else:
        filenames = [png2]
    for filename in filenames:
        res = api.media_upload(filename)
        media_ids.append(res.media_id)

    api.update_status(status=text, media_ids=media_ids)
