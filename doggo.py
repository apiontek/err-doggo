import logging
import requests
import json
from errbot import botcmd, BotPlugin


class Doggo(BotPlugin):
    """Fetch random dog image URLs"""

    BASE_URL = 'https://dog.ceo/api'

    breeds = {}

    @botcmd(split_args_with=' ')
    def doggo(self, msg, args):
        """
           Fetches a random dog image, optionally of given <breed>, or of given <breed> <sub-breed>
        """
        url = '{}/breeds/image/random'.format(self.BASE_URL)

        if len(args) > 0 and args[0]:
            breed = args[0]
            if not self.breeds:
                args.append('calledbyfunction')
                self.reloadbreeds(msg, args)
            if breed in self.breeds.keys():
                url = '{}/breed/{}/images/random'.format(self.BASE_URL, breed)
            else:
                return 'Breed not found: {}. List breeds with !listbreeds'.format(breed)

        # But what if user passed us a sub-breed?
        if len(args) > 1 and args[1]:
            subbreed = args[1]
            if len(self.breeds[breed]) == 0:
                if 'calledbyfunction' not in args:
                    args.append('calledbyfunction')
                self.reloadsubbreeds(msg, args)
                if len(self.breeds[breed]) == 0:
                    return 'No sub-breeds available for {}, so we cannot use {}.'.format(breed, subbreed)
            if subbreed in self.breeds[breed]:
                url = '{}/breed/{}/{}/images/random'.format(self.BASE_URL, breed, subbreed)
            else:
                return 'Sub-breed of {} not found: {}. List sub-breeds with !listsubbreeds'.format(breed, subbreed)

        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.debug(e)
            return 'Unable to return a dog image'

        return resp.json()['message']

    @botcmd(split_args_with=' ')
    def listbreeds(self, msg, args):
        """
           DMs the user the breeds available for use in the random image fetcher
        """
        if not self.breeds:
            args.append('calledbyfunction')
            self.reloadbreeds(msg, args)
            if not self.breeds:
                return 'Unable to load breeds list'

        # Send the output to the user to prevent spamming the channel
        direct_to_user = self.build_identifier(str(msg.frm))

        for breed in sorted(self.breeds.keys()):
            self.send(direct_to_user, breed)

    @botcmd(admin_only=True,split_args_with=' ')
    def reloadbreeds(self, msg, args):
        """
           Admin-only; forces reload of the breeds currently available
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

        for breed in data:
            self.breeds[breed] = []

        if 'calledbyfunction' not in args:
            # Tell user command was successful
            direct_to_user = self.build_identifier(str(msg.frm))
            self.send(direct_to_user, "Breed list successfully loaded")

    @botcmd(split_args_with=' ')
    def listsubbreeds(self, msg, args):
        """
           DMs the user the sub-breeds available for a given `<breed>`
        """
        if len(args) > 0 and args[0]:
            breed = args[0]
            if not self.breeds:
                args.append('calledbyfunction')
                self.reloadbreeds(msg, args)
                if not self.breeds:
                    return 'Unable to load sub-breeds list'
            if breed not in self.breeds.keys():
                return 'Breed not found: {}. List breeds with !listbreeds'.format(breed)
        else:
            return 'Please tell me the breed for which you want sub-breeds, like: *!listsubbreeds terrier*'

        # Send the output to the user to prevent spamming the channel
        direct_to_user = self.build_identifier(str(msg.frm))

        if len(self.breeds[breed]) == 0:
            args.append('calledbyfunction')
            self.reloadsubbreeds(msg, args)
            if len(self.breeds[breed]) == 0:
                return 'No sub-breeds available for {}.'.format(breed)

        for subbreed in sorted(self.breeds[breed]):
            self.send(direct_to_user, subbreed)

    @botcmd(admin_only=True, split_args_with=' ')
    def reloadsubbreeds(self, msg, args):
        """
           Admin-only; forces reload of the sub-breeds available for the given <breed>
        """
        if len(args) > 0 and args[0]:
            breed = args[0]
            if not self.breeds:
                self.reloadbreeds(msg, args)
                if not self.breeds:
                    return 'Unable to load breeds list'
            if breed in self.breeds.keys():
                url = '{}/breed/{}/list'.format(self.BASE_URL, breed)
            else:
                return 'Breed not found: {}. List breeds with !listbreeds'.format(breed)
        else:
            return 'Please tell me the breed for which you want sub-breeds, like: *!reloadsubbreeds terrier*'
        
        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.debug(e)
            return 'Unable to load sub-breeds list'

        data = resp.json()['message']
        if not isinstance(data, list):
            return 'Unable to load sub-breeds list'
        
        self.breeds[breed] = data
        if 'calledbyfunction' not in args:
            # Tell user command was successful
            direct_to_user = self.build_identifier(str(msg.frm))
            self.send(direct_to_user, "Sub-breed list successfully loaded")

    @botcmd(split_args_with=' ')
    def listallbreeds(self, msg, args):
        """
           DMs the user the list of all breeds & sub-breeds available for use in the random image fetcher
        """
        if not self.breeds:
            args.append('calledbyfunction')
            self.reloadbreeds(msg, args)
            if not self.breeds:
                return 'Unable to load breeds list'

        direct_to_user = self.build_identifier(str(msg.frm))

        for breed in self.breeds:
            if len(self.breeds[breed]) == 0:
                args[0] = breed
                args[1] = 'calledbyfunction'
                self.reloadsubbreeds(msg, args)
                if len(self.breeds[breed]) == 0:
                    self.send(direct_to_user, breed)
                else:
                    for subbreed in self.breeds[breed]:
                        self.send(direct_to_user, breed + " " + subbreed)
