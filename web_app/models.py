
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import psycopg2

db = SQLAlchemy()

migrate = Migrate()

class User(db.Model):
    """Twitter users corresponding to Tweets in the Tweet table."""
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    newest_tweet_id = db.Column(db.BigInteger)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Tweet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.Unicode(300))  # Allowing for full + links
    embedding = db.Column(db.PickleType, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))

    def __repr__(self):
        return '<Tweet {}>'.format(self.text)
