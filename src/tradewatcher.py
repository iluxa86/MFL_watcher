#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import sys
import traceback
import re
import watcherconfig as cfg
from logger import logger
from mflcache import mfl_cache

class trade_watcher:
  __api_get_trade = cfg.mflwatcher['api']['trade']

  # MFL info cache
  __mflcache = None
  __last_trade_ts = 0

  __trade_file = cfg.mflwatcher['files']['trade']
  __log_file = None

  __adjectives = cfg.mflwatcher['draft_adjectives']
  __verbs = cfg.mflwatcher['draft_verbs']

  def __init__(self, mflcache = None):
    self.__log = logger(self.__class__)
    self.__log.log("STARTING TRADE WATCHER")

    if (mflcache == None):
      self.__mflcache = mfl_cache()
    else:
      self.__mflcache = mflcache

    self.__restore_last_trade()

  def get_trade_update(self):

    trade_updates = list()
    try:
      resp = requests.get(self.__api_get_trade).json()
      json = resp['transactions']['transaction']
      new_last_trade_ts = self.__last_trade_ts

      for t in json:
        ts = t['timestamp']

        if ts > self.__last_trade_ts:
          trade_updates.append(self.__convert_transaction_to_message(t))

          # noting the latest trade ts
          if ts > new_last_trade_ts: new_last_trade_ts = ts

          self.__log.log("FOUND NEW TRADE (new ts: %s): %s" % (new_last_trade_ts,t))

        else:
          self.__log.log("SKIPPING TRADE: %s" % t)
          break

      # Dump last trade ts into file
      self.__last_trade_ts = new_last_trade_ts
      self.__store_last_trade()

    except:
      self.__log.log("UNABLE TO FETCH TRADES")
      self.__log.log(sys.exc_info()[0])
      self.__log.log(traceback.format_exc())

    return trade_updates

  def __store_last_trade(self):
    # Need to store last trade to file here
    f= open(self.__trade_file,"w+")
    f.write(str( self.__last_trade_ts))
    f.close()

  def __restore_last_trade(self):
    try:
      f= open(self.__trade_file,"r")
      for line in f:
        if (re.match("\d+",line)):
          self.__last_trade_ts = line
      f.close()
    except:
      self.__log.log("NO TRADES STORE FILE. STOPPING")
      self.__log.log(sys.exc_info()[0])
      self.__log.log(traceback.format_exc())
      raise Exception("CANNOT LOAD TRADES FILE: " + self.__trade_file)


  def __convert_transaction_to_message(self, transaction):

    f1 = self.__mflcache.get_franchise_by_id(transaction['franchise'])
    a1 = self.__parse_trade_assets(transaction['franchise1_gave_up'])

    f2 = self.__mflcache.get_franchise_by_id(transaction['franchise2'])
    a2 = self.__parse_trade_assets(transaction['franchise2_gave_up'])

    div_id = "DIVISION" + f1['division']
    div_name = self.__mflcache.get_divname_by_id(div_id)

    message = "Trade Alert for %s division!\n" % (div_name) + \
              "Franchise %s gave up:\n%s\n\nFranchise %s gave up:\n%s\n\n#trade" % (f1['name'], a1, f2['name'], a2)

    return message

  def __parse_trade_assets(self, trade_asset_string):
    assets = trade_asset_string.split(",")
    parsed_assets = list()
    for a in assets:
      if (a != ""):
        parts = a.split("_")
        type = parts[0]

        if (type == "DP"):
          round = int(parts[1]) + 1
          pick = int(parts[2]) + 1
          parsed_assets.append("Current year draft pick - %s.%02d" % (round, pick))
          continue

        if (type == "FP"):
          round = parts[3]
          year = parts[2]
          f_id = parts[1]
          franchise = self.__mflcache.get_franchise_by_id(f_id)['name']
          parsed_assets.append("%s year %s round draft pick from %s" % (year, round, franchise))
          continue

        if (type == "BB"):
          amount = parts[1]
          parsed_assets.append("$%s in blind bidding" % amount)
          continue

        # Matching for player_id
        if (re.match("\d+",type)):
          traded_player = self.__mflcache.get_player_by_id(type)
          if traded_player != None:
            parsed_assets.append("%s %s [%s]" % (traded_player['position'],traded_player['name'],traded_player['team']))
            continue

        parsed_assets.append("Unknown asset type: %s" % (a))

    return '\n'.join(parsed_assets)