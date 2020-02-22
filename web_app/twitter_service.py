

from os import getenv
import os
from dotenv import load_dotenv
import tweepy
import basilica
from web_app.models import db, Tweet, User

load_dotenv()

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", default="OOPS")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", default="OOPS")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", default="OOPS")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", default="OOPS")
BASILICA_API_KEY = os.getenv("BASILICA_API_KEY", default="OOPS")

def twitter_api_client():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    print(type(auth))
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    client = tweepy.API(auth)
    print(client)
    return client

def basilica_connection():
    connection = basilica.Connection(BASILICA_API_KEY)
    print(connection)
    return connection


client = twitter_api_client()
basilica_client = basilica_connection()




 # add or update user function

def add_or_update_user(username):
    try:
        twitter_user = client.get_user(username)
        db_user = (User.query.get(twitter_user.id) or User(id=twitter_user.id, name=username))
        db.session.add(db_user)

        tweets = twitter_user.timeline(count=100, exclude_replies=True, include_rts=False, tweet_mode='extended', since_id=db_user.newest_tweet.id)

        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            embedding = basilica_client.embed_sentence(tweet.full_text, model='twittr')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300], embedding=embedding)
            db_user.tweets.append(db_tweet)
            db.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        db.session.commit()

# add a list of users

def add_users(users):
    for user in users:
        add_or_update(user)

#update all user tweets in user table

def update_all_users():
    for user in User.query.all():
        add_or_update_user(user.name)




