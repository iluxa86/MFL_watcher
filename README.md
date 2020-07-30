Monitors your MFL league and sends update to Telegram channel
Supported updates:
- draft events
- trade events
- waiver events
- week summary

Requires config: secretconfig.py to be places in src folder:

```
# Your league id in MFL
league_id = 'XXXXX'

# Chat id in Telegram
telegram_chat = '@ChatName'

# Bot token id in telegram - https://core.telegram.org/bots
telegram_token = 'token'

# You mfl login/pwd - but not actually required now
# MFL provide a lot of info without authorization
mfl_login = ''
mfl_pwd = ''

# Map of your MFL division names from DIVISION0X to your custom name
div_names_map = {
  "DIVISION00": "GREAT DIV",
  "DIVISION01": "NOT GREAT DIV"
}

# List of divisions NOT to send updates to (filters out)
tradewatcher_filterout_divs = ['DIVISION00']

# Google Search API token to search for images
imageprovider_api_key = 'AIzaSyDK3Sj6HA-Ge0hcHPOnHGDDvay0mzuQNFQ'
imageprovider_search_engine = '011676440456467540673:msftrr8ivvq'
```

If you want to use image search configure search API as explained here:
https://pypi.org/project/Google-Images-Search/

Control scripts are in bin folder
```
# Starts script
./bin/start.sh

# checks status
./bin/status.sh

# stops scripts
./bin/stop.sh

# Logs are written to
./log/
```

If you are running watcher for the first time you need to create two files.
They are not created automatically as a protection mechanism.
```
mkdir -p var
touch var/picks.txt
touch var/trade.txt
```
These are the files where last processed trades and picks are stored.
If you start with empty files bot will read all avail to him trades and picks.

You also need to install python3 libs:
```
pip3 install -r requirements.txt
```

If you run it on Windows you also need to install
```
pip3 install windows-curses
```

If you are running in a docker:
```
docker build mfl-watcher -t mfl-watcher
```
