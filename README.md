Monitors your MFL league and sends update to Telegram channel
Requires config: watcherconfig.py in the form of:

-----------
#!/usr/bin/python
# -*- coding: utf-8 -*-

# Telegram integration settings
telegram = {
  'chatname' : '',
  'token' : '',
  'api_url' : ''
}

mflwatcher = {
  'api' : {
    'player' : "http://www62.myfantasyleague.com/2019/export?TYPE=players&DETAILS=&SINCE=&PLAYERS=%s&JSON=1",
    'draft' : "http://www62.myfantasyleague.com/2019/export?TYPE=draftResults&L=74575&JSON=1",
    'league' : "http://www62.myfantasyleague.com/2019/export?TYPE=league&L=74575&APIKEY=&JSON=1"
  },

  # NOT REALLY USED NOW
  'login' : {
    'url' : 'https://api.myfantasyleague.com/2019/login?USERNAME=%s&PASSWORD=%s&XML=1',
    'login' : '',
    'password' : ''
  },

  'files' : {
    'log' : 'draftwatcher.log',
    'picks' : 'picks.txt'
  },

  'draft_adjectives': ('young','active','energetic','muscular','powerful','strong','vigorous','dynamic','tremendous',
  'superior', 'brilliant', 'talented', 'gifted', 'magnificent', 'natural', 'prominent', 'superb'),

  'draft_verbs' : ('picks', 'selects', 'steals', 'chooses'),

  'div_map' : {
    "DIVISION00": "GREAT [#great]",
    "DIVISION01": "NEXT GEN [#nextgen]",
    "DIVISION02": "3RD & LONG [#3long]",
    "DIVISION03": "FOUR SEASONS [#4seasons]",
    "DIVISION04": "RUSSEL'5 [#russel5]",
    "DIVISION05": "LEG VI [#legVI]"
  }

}

----------
