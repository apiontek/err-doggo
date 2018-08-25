
import logging
import json

from errbot import botcmd, BotPlugin
import requests


class Doggo(BotPlugin):
    """Get random dog image URLs"""

    BASE_URL = 'https://dog.ceo/api'

    breeds = []

    @botcmd(split_args_with=' ')
    def doggo(self, msg, args):
        """
           Retrieve a random dog image, optionally specifying a breed
        """
        url = '{}/breeds/image/random'.format(self.BASE_URL)

        if len(args) > 0 and args[0]:
            breed = args[0]
            if not self.breeds:
                self.reloadbreeds(msg, args)
            if breed in self.breeds:
                url = '{}/breed/{}/images/random'.format(self.BASE_URL, breed)
            else:
                return 'Breed not found: {}. List breeds with !listbreeds'.format(breed)

        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.debug(e)
            return 'Unable to return a dog image'

        return resp.json()['message']


    @botcmd
    def listbreeds(self, msg, args):
        """
           List available breeds for use in the random image retriever
        """
        if not self.breeds:
            self.reloadbreeds(msg, args)
            if not self.breeds:
                return 'Unable to load breeds list'

        # Send the output to the user to prevent spamming the channel
        direct_to_user = self.build_identifier(str(msg.frm.nick))

        for breed in sorted(self.breeds):
            self.send(direct_to_user, breed)


    @botcmd(admin_only=True)
    def reloadbreeds(self, msg, args):
        """
           Reloads the list of breeds currently available
        """
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
