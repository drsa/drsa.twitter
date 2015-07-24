import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy.streaming import StreamListener
import os
from ConfigParser import ConfigParser
import logging
from .config import get_config, get_auth, color
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Stream Listener')
import json
import traceback

#Listener Class Override
class Listener(StreamListener):

    def __init__(self, api, output_file):
        self.output_file = output_file
        self.api = api or API()

    def on_data(self, data):

        while True:

            try:

                with open(self.output_file, 'a') as saveFile:
                    # ignore anything posted outside of KL timezone
                    data = data.strip()
                    d = json.loads(data)
                    if not d.get('user', None):
                        if d['limit']['track']:
                            raise Exception('Exceeded firehose limit')
                    timezone = d['user']['time_zone'] or ''
                    if timezone.upper() == 'KUALA LUMPUR':
                        saveFile.write(data + '\n')
                        logger.info('%s[%s]: @%s (%s) %s' % (
                            color('STORED', 'green', bold=True),
                            color(timezone.upper(), 'yellow'),
                            color(d['user']['screen_name'], bold=True), 
                            d['user']['name'], 
                            d['text'])
                        )
                    else:
                        logger.info('%s[%s]: @%s (%s) %s' % (
                            color('DISCARD', 'red', bold=True),
                            color(timezone.upper(), 'yellow'),
                            color(d['user']['screen_name'], bold=True),
                            d['user']['name'],
                            d['text'])
                        )

                return True

            except BaseException, e:
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
    twitterStream.filter(track=keywords)  #call the filter method to run the Stream Object
