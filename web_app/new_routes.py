

from flask import Blueprint, jsonify, request, render_template, flash
from sklearn.linear_model import LogisticRegression
import numpy as np
from os import getenv
from web_app.models import User, Tweet, db
from web_app.twitter_service import twitter_api_client
from web_app.twitter_service import basilica_connection
from web_app.predict import predict_user
from web_app.twitter_service import twitter_api_client, add_or_update_user, update_all_users
from pickle import dumps, loads
import pdb
import psycopg2
from dotenv import load_dotenv

#from web_app.classifier import load_model
load_dotenv()
new_routes = Blueprint("new_routes", __name__)

client = twitter_api_client()
basilica_client = basilica_connection()
#classifier_model = load_model()

@new_routes.route("/")
def index():
    return render_template("homepage.html")

@new_routes.route('/user', methods=['POST'])
@new_routes.route('/user/<name>', methods=['GET'])
def user(name=None, message=''):
    name = name or request.values['user_name']
    try:
        if request.method == 'POST':
            add_or_update_user(name)
            message = "User {} successfully added!".format(name)
        tweets = User.query.filter(User.name == name).one().tweets
    except Exception as e:
        message = "Error adding {}: {}".format(name, e)
        tweets = []
    return render_template('user.html', title=name, tweets=tweets, message=message)

@new_routes.route("/predict", methods=["POST"])
def predict(message = ''):
    user1, user2 = sorted([request.values['user1'], request.values['user2']])
    prediction = predict_user(user1, user2, request.values['tweet_text'])
    message = '"{} is more likely to mentioned in his tweets by {} than {}'.format(
        request.values['tweet_text'], user1 if prediction else user2, user2 if prediction else user1) 
    return render_template('prediction.html', title='Prediction', message=message)

@new_routes.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    return render_template('homepage.html', title='Reset database!')

@new_routes.route('/update')
def update():
    update_all_users()
    return render_template('homepage.html', users=User.query.all(), title='Cache cleared and all Tweets updated!')




