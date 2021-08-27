import tweepy
import cred
import textblob

auth = tweepy.AppAuthHandler(cred.API_KEY,cred.API_SECRET)
api = tweepy.API(auth)
for tweet in tweepy.Cursor(api.search, q='linux').items(100):
    print(tweet)