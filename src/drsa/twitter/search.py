import tweepy
from .config import get_config, get_auth, get_api, color, save_or_discard
import json
import logging
from dateutil.parser import parse as parse_date
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Twitter Search')

def search(query, output):
    api = get_api()
    for i in tweepy.Cursor(api.search, q=query).items():
        d = i._json
        save_or_discard(d, output)
