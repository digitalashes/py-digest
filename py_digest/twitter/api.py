import asyncio
from json import load, dumps
from os.path import join as path_join
from urllib.parse import urlparse

import twitter
import uvloop
from aiohttp import ClientSession
from bs4 import BeautifulSoup

import settings

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

logger = settings.logger

FILE_PATH = path_join(settings.BASE_DIR, 'db.json')

api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                  consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                  access_token_key=settings.TWITTER_ACCESS_TOKEN,
                  access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)


def _get_from_file(key):
    try:
        with open(FILE_PATH, 'r') as file:
            try:
                data = load(file)
                return data.get(key, None)
            except Exception as e:
                logger.exception(e)
                return None
    except FileNotFoundError:
        return None


def get_last_post_id():
    return _get_from_file('last_post_id')


def get_user_id():
    user_id = _get_from_file('user_id')
    if user_id:
        return user_id
    user = api.GetUser(screen_name=settings.PYDIGEST_USER_NAME)
    return user.id


def update_last_post_id(last_post_id, user_id):
    with open(FILE_PATH, 'w+') as file:
        try:
            data = dumps({'last_post_id': last_post_id, 'user_id': user_id})
            file.write(data)
            return True
        except Exception as e:
            logger.exception(e)
            return False


async def fetch(semaphore, obj, session):
    async with semaphore:
        text = obj.text.split(':')[0]
        url = obj.urls[0]._json.get('expanded_url')
        url_parse_data = urlparse(url)
        if url_parse_data.hostname == 'pythondigest.ru' and 'issue' in url_parse_data.path:
            return f'{text}: {url}'
        async with session.get(url) as response:
            if response.status != 200:
                return None
            soup = BeautifulSoup(await response.text(), 'lxml')
            elem = soup.find('a', 'btn btn-primary btn-sm pull-left')
            if hasattr(elem, 'attrs'):
                link = elem.attrs.get('href')
                return f'{text}: {link}'
            return None


async def run(urls):
    tasks = []
    semaphore = asyncio.Semaphore(50)
    async with ClientSession() as session:
        for obj in urls:
            task = asyncio.ensure_future(fetch(semaphore, obj, session))
            tasks.append(task)
        return [item for item in await asyncio.gather(*tasks) if item]


def get_posts():
    last_post_id = get_last_post_id()
    user_id = get_user_id()
    results = api.GetUserTimeline(user_id=user_id, since_id=last_post_id, count=settings.TWITTER_POST_COUNT)
    if not results:
        return None
    update_last_post_id(results[0].id, user_id)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(results))
    try:
        posts = loop.run_until_complete(future)
        return posts
    except Exception as e:
        logger.exception(e)
    finally:
        loop.close()
