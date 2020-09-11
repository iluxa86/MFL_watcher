import secretconfig as secret
import schedule
year = '2020'
league_id = secret.league_id
update_period_sec = 60
tradewatcher_enabled = True
tradewatcher_images_enabled = True
draftwatcher_enabled = False
draftwatcher_images_enabled = True
waiverwatcher_enabled = True
weeksummarywatcher_enabled = True

# For docker it should be False
daemon = False

# Telegram integration settings
telegram = {
  'chatname': secret.telegram_chat,
  'token': secret.telegram_token
}

# Waiverwatcher schedule
# Runs only according to this schedule
waiverwatcher_schedule = schedule.every().wednesday.at("09:10")

# Weeksummarywatcher schedule
# Runs only according to this schedule
weeksummarywatcher_schedule = schedule.every().tuesday.at("20:00")

mflwatcher = {
  'api': {
    'player': "https://api.myfantasyleague.com/" + year + "/export?TYPE=players&DETAILS=&SINCE=&PLAYERS=%s&JSON=1",
    'draft': "http://www62.myfantasyleague.com/%s/export?TYPE=draftResults&L=%s&JSON=1" % (year, league_id),
    'league': "http://www62.myfantasyleague.com/%s/export?TYPE=league&L=%s&APIKEY=&JSON=1" % (year, league_id),
    'trade': "http://www62.myfantasyleague.com/%s/export?TYPE=transactions&L=%s&APIKEY=&W=&TRANS_TYPE=TRADE&FRANCHISE=&DAYS=1&COUNT=&JSON=1" % (year, league_id),
    'waiver': "http://www62.myfantasyleague.com/%s/export?TYPE=transactions&L=%s&APIKEY=&W=&TRANS_TYPE=BBID_WAIVER&FRANCHISE=&DAYS=6&COUNT=&JSON=1" % (year, league_id),
    'results': "http://www62.myfantasyleague.com/%s/export?TYPE=weeklyResults&L=%s&APIKEY=&JSON=1" % (year, league_id)
  },

  # NOT REALLY USED NOW
  'login': {
    'url': 'https://api.myfantasyleague.com/' + year + '/login?USERNAME=%s&PASSWORD=%s&XML=1',
    'login': secret.mfl_login,
    'password': secret.mfl_pwd
  },

  'files': {
    'log': 'log/mflwatcher.log',
    'picks': 'var/picks.txt',
    'trade': 'var/trade.txt'
  },

  'draft_adjectives': ('young','active','energetic','muscular','powerful','strong','vigorous','dynamic','tremendous',
  'superior', 'brilliant', 'talented', 'gifted', 'magnificent', 'natural', 'prominent', 'superb', 'dominant',
  'outstanding', 'virtious', 'vivacious', 'spirited', 'all-round', 'promising', 'competent', 'temperamental',
  'valiant', 'modest', 'skilled', 'remarkable'),

  'draft_verbs': ('picks', 'selects', 'steals', 'chooses'),

  'div_map': secret.div_names_map,
  'div_images': {
    "DIVISION00": "../images/DIV01.png",
    "DIVISION01": "../images/DIV02.png",
    "DIVISION02": "../images/DIV03.png",
    "DIVISION03": "../images/DIV04.png",
    "DIVISION04": "../images/DIV05.png",
    "DIVISION05": "../images/DIV06.png"
  },
  'image_font_file': '../images/BAUHS93.ttf',

  # Filter out trades from these divs:
  'tradewatcher_filter': secret.tradewatcher_filterout_divs,

  # Images search for draft watcher
  'imageprovider_api_key': secret.imageprovider_api_key,
  'imageprovider_search_engine': secret.imageprovider_search_engine
}

