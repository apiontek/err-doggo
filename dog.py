
import logging
import json

from errbot import botcmd, BotPlugin
import requests


class Dog(BotPlugin):
    """Get random dog image URLs"""

    BASE_URL = 'https://dog.ceo/api'

    @botcmd
    def doggo(self, msg, args):
        url = '{}/breeds/image/random'.format(self.BASE_URL)

        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.debug(e)
            return 'Unable to return a dog image'

        return resp.json()['message']
