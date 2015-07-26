import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy.streaming import StreamListener
import os
from ConfigParser import ConfigParser
import logging
from .config import get_config, get_auth, color, save_or_discard
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Stream Listener')
import json
import traceback

class FirehoseLimitExceeded(Exception):
    pass

#Listener Class Override
class Listener(StreamListener):

    def __init__(self, api, output_file):
        self.output_file = output_file
        self.api = api or API()

    def on_data(self, data):

        while True:

            try:
                data = data.strip()
                d = json.loads(data)
                if not d.get('user', None):
                    if d['limit']['track']:
                        raise FirehoseLimitExceeded()
                save_or_discard(d, self.output_file)
                return True

            except BaseException, e:
                if isinstance(e, FirehoseLimitExceeded):
                    raise e
                traceback.print_exc()
                logger.error('Failed on_data, ' + data)
                time.sleep(5)
                pass

    def on_error(self, status):
        logger.error(status)

def listen(keywords, output):
    config = get_config()
    start_time = time.time() #grabs the system time

    auth = get_auth()

    proxy = os.environ.get('https_proxy', None)
    api = API(auth, proxy=proxy)
    logger.info(
      "Listening for messages with keywords: %s from Kuala Lumpur timezone" % (
          ','.join(keywords)
    ))
    twitterStream = Stream(auth, Listener(api, output)) #initialize Stream object with a time out limit
    twitterStream.api = api
    while True:
        try:
            twitterStream.filter(track=keywords)  #call the filter method to run the Stream Object
        except FirehoseLimitExceeded, e:
            traceback.print_exc()
            logger.info("Firehose Limit Exceeded. Attempting to rebind")
            time.sleep(5)
