from slackclient import SlackClient

import settings

slack_client = SlackClient(settings.SLACK_OAUTH_ACCESS_TOKEN)
slack_client_bot = SlackClient(settings.SLACK_BOT_TOKEN)

logger = settings.logger


def check_channel():
    response = slack_client.api_call('channels.list', exclude_archived=True)
    if 'ok' in response:
        channels = response.get('channels')
        slack_channel = [
            channel for channel in channels
            if channel.get('name').lower() == settings.SLACK_CHANNEL_NAME.lower()
        ]
        if slack_channel:
            return slack_channel[0]
        else:
            response = slack_client.api_call('channels.create', name=settings.SLACK_CHANNEL_NAME)
            if 'ok' in response:
                return response.get('channel')
    logger.error(response.get('error'))
    raise Exception(response.get('error'))


channel = check_channel()


def write_into_channel(post):
    slack_client_bot.api_call('chat.postMessage', channel=channel.get('id'), text=post)
