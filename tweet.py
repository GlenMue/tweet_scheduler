from os import environ
from datetime import datetime, timedelta, timezone
from tweepy import Client
import time
from dotenv import load_dotenv
load_dotenv()
import logging
import sqlite3
import json

logging.basicConfig(level= logging.INFO)
logger = logging.getLogger(__name__)

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_KEY_SECRET = environ['CONSUMER_KEY_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
BEARER_TOKEN = environ['BEARER_TOKEN']

client = Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_KEY_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

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

def read_tweets_from_db(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Assuming your table name is 'tweets'
        cursor.execute("SELECT * FROM tweets")
        rows = cursor.fetchall()

        tweet_records = []
        for row in rows:
            tweet_dict = {
                'id': row[0],
                'message': row[1],
                'time': row[2],
                'done': row[3],
                'row_index': row[4],
            }
            tweet_records.append(tweet_dict)

        return tweet_records

    except sqlite3.Error as e:
        print(f"Error reading data from the database: {e}")
        return None
    finally:
        conn.close()

tweet_records= read_tweets_from_db('app/tweets.db')
print(tweet_records)

INTERVAL = int(environ['INTERVAL'])
DEBUG = environ['DEBUG'] == '1'

def main():
    while True:
        # tweet_records = worksheet.get_all_records()
        current_time = datetime.now()
        logger.info(f' {len(tweet_records)} tweets found at {current_time.time()}')
        # empty space
        print("")

        for index, tweet in enumerate(tweet_records):
            msg = tweet['message']
            time_str = tweet['time']
            done = tweet['done']
            date_time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

            if not done:
                now_time_in_wat = datetime.now()

                print(f'date_time_obj: {date_time_obj}')
                print(f'now_time_in_wat: {now_time_in_wat}')

                if date_time_obj < now_time_in_wat:
                    logger.info('this should be tweeted')
                    try:
                        # api.update_status(msg)
                        client.create_tweet(text= msg)
                        logger.info(f'tweeted {msg}')
                        # worksheet.update_cell(index, 3, 1)
                        tweet['done'] = True  # Mark the tweet as done
                        # modify the database
                        conn = sqlite3.connect('app/tweets.db')
                        cursor = conn.cursor()
                        cursor.execute("UPDATE tweets SET done = ? WHERE row_index = ?", (1, index))
                        conn.commit()

                    except Exception as e:
                        logger.warning(f'exception during tweet! {e}')
        print("")
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()