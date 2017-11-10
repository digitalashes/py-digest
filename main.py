from py_digest.slack import write_into_channel
from py_digest.twitter import get_posts

if __name__ == '__main__':
    posts = get_posts()
    if posts:
        for post in reversed(posts):
            write_into_channel(post)
