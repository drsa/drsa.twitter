import tweepy
from .config import get_config, get_auth, get_api
import json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Twitter Search')

def search():
    api = get_api()
    for i in tweepy.Cursor(api.search, q='najib').items():
        with open('output.jsonl', 'a') as f:
            d = i._json
            logger.info('@%s (%s) : %s' % (
                d['user']['screen_name'],
                d['user']['name'],
                d['text']
            ))
            f.write(json.dumps(i._json) + '\n')
