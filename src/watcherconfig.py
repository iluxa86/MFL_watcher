import secretconfig as secret
import schedule
year = '2019'
league_id = secret.league_id
update_period_sec = 60
tradewatcher_enabled = True
draftwatcher_enabled = False
waiverwatcher_enabled = True
daemon = True

# Telegram integration settings
telegram = {
  'chatname' : secret.telegram_chat,
  'token' : secret.telegram_token,
  'api_url' : 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s'
}

# Waiverwatcher schedule
# Runs only according to this schedule
waiverwatcher_schedule = schedule.every().wednesday.at("02:10")

mflwatcher = {
  'api' : {
    'player' : "http://www62.myfantasyleague.com/" + year + "/export?TYPE=players&DETAILS=&SINCE=&PLAYERS=%s&JSON=1",
    'draft' : "http://www62.myfantasyleague.com/%s/export?TYPE=draftResults&L=%s&JSON=1" % (year, league_id),
    'league' : "http://www62.myfantasyleague.com/%s/export?TYPE=league&L=%s&APIKEY=&JSON=1" % (year, league_id),
    'trade' : "http://www62.myfantasyleague.com/%s/export?TYPE=transactions&L=%s&APIKEY=&W=&TRANS_TYPE=TRADE&FRANCHISE=&DAYS=1&COUNT=&JSON=1" % (year, league_id),
    'waiver' : "http://www62.myfantasyleague.com/%s/export?TYPE=transactions&L=%s&APIKEY=&W=&TRANS_TYPE=BBID_WAIVER&FRANCHISE=&DAYS=6&COUNT=&JSON=1" % (year, league_id)
  },

  # NOT REALLY USED NOW
  'login' : {
    'url' : 'https://api.myfantasyleague.com/' + year + '/login?USERNAME=%s&PASSWORD=%s&XML=1',
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

  'div_map' : secret.div_names_map,

  # Filter out trades from these divs:
  'tradewatcher_filter' : secret.tradewatcher_filterout_divs
}

