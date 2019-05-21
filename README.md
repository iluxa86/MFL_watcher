Monitors your MFL league and sends update to Telegram channel
Supported updates:
- draft events
- trade events

Requires config: watcherconfig.py in the form of:

```
year = '2019'
league_id = '74575'
update_period_sec = 60
tradewatcher_enabled = True
draftwatcher_enabled = True
daemon = True

# Telegram integration settings
telegram = {
  'chatname' : '@<Telegram_name>',
  'token' : '<bot_token>',
  'api_url' : 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s'
}

# DONT NEED TO TOUCH THESE
mflwatcher = {
  'api' : {
    'player' : "http://www62.myfantasyleague.com/" + year + "/export?TYPE=players&DETAILS=&SINCE=&PLAYERS=%s&JSON=1",
    'draft' : "http://www62.myfantasyleague.com/%s/export?TYPE=draftResults&L=%s&JSON=1" % (year, league_id),
    'league' : "http://www62.myfantasyleague.com/%s/export?TYPE=league&L=%s&APIKEY=&JSON=1" % (year, league_id),
    'trade' : "http://www62.myfantasyleague.com/%s/export?TYPE=transactions&L=%s&APIKEY=&W=&TRANS_TYPE=TRADE&FRANCHISE=&DAYS=1&COUNT=&JSON=1" % (year, league_id)
  },

  # NOT REALLY USED NOW
  'login' : {
    'url' : 'https://api.myfantasyleague.com/2019/login?USERNAME=%s&PASSWORD=%s&XML=1',
    'login' : '',
    'password' : ''
  },

  'files' : {
    'log' : 'draftwatcher.log',
    'picks' : 'picks.txt',
    'trade' : 'trade.txt'
  },

  'draft_adjectives': ('young','active','energetic','muscular','powerful','strong','vigorous','dynamic','tremendous',
  'superior', 'brilliant', 'talented', 'gifted', 'magnificent', 'natural', 'prominent', 'superb', 'dominant',
  'outstanding', 'virtious', 'vivacious', 'spirited', 'all-round', 'promising', 'competent', 'temperamental',
  'valiant', 'modest', 'skilled', 'remarkable'),

  'draft_verbs' : ('picks', 'selects', 'steals', 'chooses'),

  # NEED TO UPDATE ALIASES FOR YOU DIVISIONS
  'div_map' : {
    "DIVISION00": "GREAT [#great]",
    "DIVISION01": "NEXT GEN [#nextgen]",
    "DIVISION02": "3RD & LONG [#3long]",
    "DIVISION03": "FOUR SEASONS [#4seasons]",
    "DIVISION04": "RUSSEL'5 [#russel5]",
    "DIVISION05": "LEG VI [#legVI]"
  }
}
```
