
import logging
import json

from errbot import botcmd, BotPlugin
import requests


class Dog(BotPlugin):
    """Get random dog image URLs"""

    BASE_URL = 'https://dog.ceo/api'

    breeds = None

    @botcmd(split_args_with=' ')
    def doggo(self, msg, args):
        url = None

        if len(args) > 0:
            breed = args[0]
            if not self.breeds:
                self.reload_breeds(self, msg, args)
            if breed in self.breeds:
                url = '{}/breed/{}/images/random'.format(self.BASE_URL, breed)

        if not url:
            url = '{}/breeds/image/random'.format(self.BASE_URL)

        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.debug(e)
            return 'Unable to return a dog image'

        return resp.json()['message']


    @botcmd
    def breeds(self, msg, args):
        if not self.breeds:
            self.reload_breeds(self, msg, args)
            if not self.breeds:
                return 'Unable to load breeds list'

        # Send the output to the user to prevent spamming the channel
        direct_to_user = self.build_identifier(str(mess.frm.nick))

        for breed in sorted(self.breeds):
            self.send(direct_to_user, breed)


    @botcmd(admin_only=True)
    def reload_breeds(self, msg, args):
        url = '{}/breeds/list'.format(self.BASE_URL)

        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.debug(e)
            return 'Unable to load breeds list'

        data = resp.json()['message']
        if not isinstance(data, list):
            return 'Unable to load breeds list'

        self.breeds = data
