from ConfigParser import ConfigParser
import os
import tweepy
import colored as clrd 
import json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('drsa-twitter')

def color(text, fg=None, bg=None, bold=False):
    res = text
    if fg:
        res = "%s%s" % (clrd.fg(fg), res)
    if bg:
        res = "%s%s" % (clrd.bg(fg), res)
    if bold:
        res = "%s%s" % (clrd.attr('bold'), res)
    if fg or bg or bold:
        res = "%s%s" % (res, clrd.attr('reset'))
    return res

def get_config():
    default_fname = os.environ.get('DRSA_TWITTER_CONFIG', 'config.cfg')

    fname = None
    config_paths = ['/etc/drsa-toolkit/twitter.cfg', default_fname]
    for i in config_paths:
        if os.path.exists(i):
            fname = i

    if fname is None:
        raise RuntimeError(
            "Unable to find config file in %s" % ', '.join(config_paths)
        )

    cp = ConfigParser()
    cp.readfp(open(fname))

    result = {
        'consumer-key': cp.get('drsa-twitter', 'consumer-key'),
        'consumer-secret': cp.get('drsa-twitter', 'consumer-secret'),
        'access-token-key': cp.get('drsa-twitter', 'token-key'),
        'access-token-secret': cp.get('drsa-twitter', 'token-secret'),
        'woeid': cp.get('drsa-twitter', 'woeid')
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


def save_or_discard(data, f):
    d = data
    with open(f, 'a') as output:
        timezone = d['user']['time_zone'] or ''
        if timezone.upper() in ['KUALA LUMPUR', '']:
            output.write(json.dumps(data) + '\n')
            logger.info('%s[%s %s]: @%s (%s) %s' % (
                color('STORED', 'green', bold=True),
                color(data['created_at'], 'blue'),
                color(timezone.upper(), 'yellow'),
                color(d['user']['screen_name'], bold=True),
                d['user']['name'],
                d['text'])
            )
        else:
            logger.info('%s[%s %s]: @%s (%s) %s' % (
                color('DISCARD', 'red', bold=True),
                color(data['created_at'], 'blue'),
                color(timezone.upper(), 'yellow'),
                color(d['user']['screen_name'], bold=True),
                d['user']['name'],
                d['text'])
            )
