import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy.streaming import StreamListener
import os
from ConfigParser import ConfigParser
import logging
from .config import get_config, get_auth
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Stream Listener')
import json

#Listener Class Override
class Listener(StreamListener):

    def on_data(self, data):

        while True:

            try:

                with open('raw_tweets.json', 'a') as saveFile:
                    # ignore anything posted outside of KL timezone
                    data = data.strip()
                    d = json.loads(data)
                    timezone = d['user']['time_zone'] or ''
                    if timezone.upper() == 'KUALA LUMPUR':
                        saveFile.write(data + '\n')
                        logger.info('@%s (%s) %s' % (
                            d['user']['screen_name'], d['user']['name'], 
                            d['text'])
                        )
#                    else:
                        #print "skipped %s ||| %s " % (timezone, d['text'])

                return True

            except BaseException, e:
                print 'failed ondata,', data
                time.sleep(5)
                pass

    def on_error(self, status):
        print status

def listen():
    config = get_config()
    start_time = time.time() #grabs the system time

    keyword_list = config['keyword-list']
    languages = config['languages']

    auth = OAuthHandler(config['consumer-key'], config['consumer-secret']) #OAuth object
    auth.set_access_token(
        config['access-token-key'], 
        config['access-token-secret']
    )

    auth = get_auth()

    api = API(auth)

    twitterStream = Stream(auth, Listener()) #initialize Stream object with a time out limit
    twitterStream.filter(track=keyword_list, languages=languages)  #call the filter method to run the Stream Object
