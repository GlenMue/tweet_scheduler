from os import environ
from datetime import datetime, timedelta
import gspread
import tweepy
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

auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit= True)


gc = gspread.service_account(filename = 'tweetsheet.json')

sh = gc.open_by_key('195i34hteWh_n6jT8m6VvPmS59W7XDhe3HtBq65e9pTM')
worksheet = sh.sheet1

INTERVAL = int(environ['INTERVAL'])
DEBUG = environ['DEBUG'] == '1'

def main():
    while True:
        tweet_records = worksheet.get_all_records()
        current_time = datetime.utcnow() + timedelta(hours = 1)
        logger.info(f'{len(tweet_records)} tweets found at {current_time.time()}')

        for index, tweet in enumerate(tweet_records, start = 2):
            msg = tweet['message']
            time_str = tweet['time']
            done = tweet['done']
            date_time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

            if not done:
                now_time_in_wat = datetime.utcnow() + timedelta(hours = 1)
                if date_time_obj < now_time_in_wat:
                    logger.info('this should be tweeted')
                    try:
                        api.update_status(msg)
                        worksheet.update_cell(index, 3, 1)
                    except Exception as e:
                        logger.warning(f'exception during tweet! {e}')

        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()