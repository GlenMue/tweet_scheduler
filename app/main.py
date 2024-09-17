from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
from typing import Optional
from flask_sqlalchemy import SQLAlchemy
import os

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///C:/Users/Owner/Downloads/tweet-scheduler/tweet-scheduler/app/tweets.db'
# initialize the app with the extension
db.init_app(app)

class Tweet(db.Model):
    __tablename__ = 'tweets'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(280))
    time = db.Column(db.String)
    done = db.Column(db.Boolean, default=False)
    row_index = db.Column(db.Integer)

with app.app_context():
    # check if the database exists, if not, create it
    if not os.path.exists('app/tweets.db'):
        db.create_all()

# tweet_records = [
#     {
#         'message': "Hello, Twitter! This is my first scheduled tweet.",
#         'time': '2024-09-16 10:00:00',  # Replace with your desired timestamp
#         'done': False,
#     },
#     {
#         'message': "Another scheduled tweet coming up!",
#         'time': '2024-09-16 14:30:00',  # Replace with another timestamp
#         'done': False,
#     },
#     # Add more tweet records as needed
# ]

def get_date_time(date_time_str):
    date_time_obj = None
    error_code = None
    try: 
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        error_code = f'Error! {e}'

    if date_time_obj is not None:
        now_time_in_wat = datetime.now()

        if not date_time_obj > now_time_in_wat:
            error_code = 'error! time must be in the future'

    return date_time_obj, error_code

@app.route('/')
def tweet_list():
    # tweet_records = worksheet.get_all_records()
    tweets = []

    # for index, tweet in enumerate(tweet_records, start = 2):
    #     tweet = Tweet(**tweet, row_index = index)
    #     # tweets.append(tweet)

    # convert tweets in db to list and add the row_index
    for tweet in Tweet.query.all():
        tweets.append(tweet)
        tweet.row_index = tweets.index(tweet)+1

    # tweets.reverse()

    n_open_tweets = sum(1 for tweet in tweets if not tweet.done)
    return render_template('base.html', tweets = tweets, n_open_tweets = n_open_tweets)

@app.route('/tweet', methods = ['POST'])
def add_tweet():
    message  = request.form['message']
    if not message:
        return 'error! no message'
    
    time  = request.form['time']
    if not time:
        return 'error! no time'
    
    pw  = request.form['pw']
    if not pw or pw != '123450':
        return 'error! wrong password'
    
    if len(message) > 280:
        return 'error! message too long!'
    
    date_time_obj, error_code = get_date_time(time)
    if error_code is not None:
        return error_code
    
    # tweet = [str(date_time_obj), message, 0]

    # add tweet to db
    new_tweet = Tweet(message = message, time = date_time_obj, done = False)
    db.session.add(new_tweet)
    db.session.commit()

    # worksheet.append_row(tweet)
    return redirect('/')

@app.route('/delete/<int:row_index>')
def delete_tweet(row_index):
    # worksheet.delete_rows(row_index)

    # delete tweet from db
    tweet = Tweet.query.get(row_index)
    db.session.delete(tweet)
    db.session.commit()
    return redirect('/')
    

if __name__ == '__main__':
    app.run(debug=True)