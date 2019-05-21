import secretconfig as secret

year = '2019'
league_id = secret.league_id
update_period_sec = 60
tradewatcher_enabled = True
draftwatcher_enabled = True
daemon = True

# Telegram integration settings
telegram = {
  'chatname' : secret.telegram_chat,
  'token' : secret.telegram_token,
  'api_url' : 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s'
}

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
    'login' : secret.mfl_login,
    'password' : secret.mfl_pwd
  },

  'files' : {
    'log' : 'log/mflwatcher.log',
    'picks' : 'var/picks.txt',
    'trade' : 'var/trade.txt'
  },

  'draft_adjectives': ('young','active','energetic','muscular','powerful','strong','vigorous','dynamic','tremendous',
  'superior', 'brilliant', 'talented', 'gifted', 'magnificent', 'natural', 'prominent', 'superb', 'dominant',
  'outstanding', 'virtious', 'vivacious', 'spirited', 'all-round', 'promising', 'competent', 'temperamental',
  'valiant', 'modest', 'skilled', 'remarkable'),

  'draft_verbs' : ('picks', 'selects', 'steals', 'chooses'),

  'div_map' : secret.div_names_map
}

