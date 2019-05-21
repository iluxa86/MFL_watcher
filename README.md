Monitors your MFL league and sends update to Telegram channel
Supported updates:
- draft events
- trade events

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

```

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
