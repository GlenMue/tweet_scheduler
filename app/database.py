from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Owner/Downloads/tweet-scheduler/tweet-scheduler/app/tweets.db'
db = SQLAlchemy(app)

class Tweet(db.Model):
    __tablename__ = 'tweets'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(280))
    time = db.Column(db.DateTime)
    done = db.Column(db.Boolean, default=False)
    row_index = db.Column(db.Integer)

def create_table():
    db.create_all()
