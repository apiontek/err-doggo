# Doggo

This is a plugin for [Errbot](http://errbot.io/) that fetches random dog images from the [dog.ceo API$

Users can optionally specify a breed, and, also optionally, a sub-breed:

## 
- `!doggo` Fetches a random dog image
- `!doggo <breed>` fetches a random dog image of `<breed>` specified
- `!doggo <breed> <sub-breed>` fetches a random dog image of `<breed>` & `<sub-breed>` specified
- `!listbreeds` DMs the user the available breeds for use in the random image retriever
- `!listsubbreeds <breed>` DMs the user the available sub-breeds for a given `<breed>`
- `!listallbreeds` DMs the user the list of all available breeds & sub-breeds
- `!reloadbreeds` Admin-only; forces reload of the breeds currently available
- `!reloadsubbreeds <breed>` Admin-only; forces reload of sub-breed for the given `<breed>`

