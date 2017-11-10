import logging
from os import environ
from os.path import (
    join,
    dirname,
    exists as path_exists
)

from dotenv import load_dotenv

logging.basicConfig(filename='py_digest.log', level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = dirname(__file__)
dotenv_path = join(BASE_DIR, '.env')
if not path_exists(dotenv_path):
    raise FileNotFoundError

load_dotenv(dotenv_path)

TWITTER_CONSUMER_KEY = environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = environ.get('TWITTER_ACCESS_TOKEN_SECRET')

TWITTER_POST_COUNT = environ.get('TWITTER_POST_COUNT')

PYDIGEST_USER_NAME = 'pydigest'
SLACK_CHANNEL_NAME = 'py-digest'

SLACK_CLIENT_ID = environ.get('SLACK_CLIENT_ID')
SLACK_CLIENT_TOKEN = environ.get('SLACK_CLIENT_TOKEN')
SLACK_OAUTH_ACCESS_TOKEN = environ.get('SLACK_OAUTH_ACCESS_TOKEN')
SLACK_BOT_TOKEN = environ.get('SLACK_BOT_TOKEN')
