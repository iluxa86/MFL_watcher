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
