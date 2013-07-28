from flask import Blueprint
from models import Session, Tweet
from flask.ext.login import login_required
from flask.ext.security.core import current_user
from models import OAuthTokens
import json
import tweepy

tweet_renderer = Blueprint('tweets', __name__)

@tweet_renderer.route('/tweets')
@login_required
def get_tweet():
    tweet = get_last_tweet(current_user.id)

    return json.dumps({'type' : 'text',
            'color' : '000000',
            'channel' : 'Twitter',
            'title' : tweet.author.name,
            'text' : tweet.text,
            'image' : tweet.user.profile_image_url,
            'meta' : {
                'text' : 'Twitter!',
                'image' : tweet.user.profile_image_url
            },
        })

def get_last_tweet(user_id):
    oauth_token = Session().query(OAuthTokens).filter_by(user_id=user_id).one()
    api = setup_api(oauth_token)
    return api.user_timeline(count = 1)[0]

def setup_api(oauth_token):
    config = json.load(open('config.json'))
    consumer_key = str(config["TwitterReader"]["CONSUMER_KEY"])
    consumer_secret = str(config["TwitterReader"]["CONSUMER_SECRET"])
    key = oauth_token.twitter_key
    secret = oauth_token.twitter_secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    return tweepy.API(auth)

def get_image(tweet):
    media = tweet.entities.get('media')
    if media is not None:
        return media[0]['expanded_url']


