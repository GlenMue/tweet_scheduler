from os import environ
from datetime import datetime, timedelta, timezone
import gspread
from tweepy import Client
import time
from dotenv import load_dotenv
load_dotenv()
import logging
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

tweet_records = [
    {
        'message': "Hello, Twitter! This is my first scheduled tweet.",
        'time': '2024-09-16 10:00:00',  # Replace with your desired timestamp
        'done': False,
    },
    {
        'message': "Another scheduled tweet coming up!",
        'time': '2024-09-16 14:30:00',  # Replace with another timestamp
        'done': False,
    },
    # Add more tweet records as needed
]

INTERVAL = int(environ['INTERVAL'])
DEBUG = environ['DEBUG'] == '1'

def main():
    while True:
        # tweet_records = worksheet.get_all_records()
        current_time = datetime.now(timezone.utc)
        logger.info(f' {len(tweet_records)} tweets found at {current_time.time()}')
        # empty space
        print("")

        for index, tweet in enumerate(tweet_records):
            msg = tweet['message']
            time_str = tweet['time']
            done = tweet['done']
            date_time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)

            if not done:
                now_time_in_wat = datetime.now(timezone.utc)

                if date_time_obj < now_time_in_wat:
                    logger.info('this should be tweeted')
                    try:
                        # api.update_status(msg)
                        client.create_tweet(text= msg)
                        logger.info(f'tweeted {msg}')
                        # worksheet.update_cell(index, 3, 1)
                        tweet['done'] = True  # Mark the tweet as done

                    except Exception as e:
                        logger.warning(f'exception during tweet! {e}')
        print("")
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()