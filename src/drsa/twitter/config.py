from ConfigParser import ConfigParser
import os
import tweepy

def get_config():
    fname = os.environ.get('DRSA_TWITTER_CONFIG', 'config.cfg')

    cp = ConfigParser()
    cp.readfp(open(fname))

    result = {
        'consumer-key': cp.get('drsa-twitter', 'consumer-key'),
        'consumer-secret': cp.get('drsa-twitter', 'consumer-secret'),
        'access-token-key': cp.get('drsa-twitter', 'token-key'),
        'access-token-secret': cp.get('drsa-twitter', 'token-secret'),
        'keyword-list': cp.get('drsa-twitter', 'keywords').split() + ['%23'],
        'languages': cp.get('drsa-twitter', 'languages').split()
    }

    return result

def get_auth():

    config = get_config()

    auth = tweepy.OAuthHandler(config['consumer-key'], config['consumer-secret']) #OAuth object
    auth.set_access_token(
        config['access-token-key'],
        config['access-token-secret']
    )

    return auth

def get_api():
    auth = get_auth()
    return tweepy.API(
            auth,
            retry_count=200,
            retry_delay=30,
            retry_errors=[404,403,502,503],
            timeout=20,
            wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True
    )
