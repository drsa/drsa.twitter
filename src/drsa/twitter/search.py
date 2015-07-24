import tweepy
from .config import get_config, get_auth, get_api, color
import json
import logging
from dateutil.parser import parse as parse_date
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Twitter Search')

def search(query, output):
    api = get_api()
    for i in tweepy.Cursor(api.search, q=query).items():
        with open(output, 'a') as f:
            d = i._json
            logger.info('[%s] %s (%s) : %s' % (
                color(parse_date(d['created_at']).isoformat(), 'blue'),
                color('@' + d['user']['screen_name'], 'yellow', bold=True),
                color(d['user']['name'], bold=True),
                d['text']
            ))
            f.write(json.dumps(i._json) + '\n')
