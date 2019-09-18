#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import sys
import traceback
from collections import defaultdict
import watcherconfig as cfg
from logger import logger
from mflcache import mfl_cache

class waiver_watcher:
  __api_get_waiver = cfg.mflwatcher['api']['waiver']

  # MFL info cache
  __mflcache = None
  __log_file = None

  def __init__(self, mflcache = None):
    self.__log = logger(self.__class__)
    self.__log.log("STARTING WAIVER WATCHER")

    if (mflcache == None):
      self.__mflcache = mfl_cache()
    else:
      self.__mflcache = mflcache

  # Supposed to be run only once per week
  # Generates list of all waiver transactions for current week
  def get_waiver_updates(self):

    waivers_dict = defaultdict(lambda: list())

    try:
      resp = requests.get(self.__api_get_waiver).json()

      json = []
      if 'transaction' in resp['transactions']:
        json = resp['transactions']['transaction']

        # Corner case with only one trade
        # MFL reports object not as list then
        if isinstance(json, dict):
          json = [json]
      else:
        # No new trades found
        self.__log.log("NO WAIVER TRANSACTION GOT FROM API")

      for t in json:
        waiver_transaction = self.__convert_transaction_to_message(t)
        waivers_dict[waiver_transaction[0]].append(waiver_transaction[1])

    except:
      self.__log.log("UNABLE TO FETCH WAIVERS")
      self.__log.log(sys.exc_info()[0])
      self.__log.log(traceback.format_exc())

    updates_list = list()
    updates_list.append("WAIVER RESULTS for this week\n#waiver")
    for div in waivers_dict.keys():
      division_update = []
      division_update.append("Division: %s:" % div)
      for update in waivers_dict[div]:
        division_update.append(update)
      updates_list.append('\n'.join(division_update))

    self.__log.log("WAIVER RESULTS ARE:\n%s" % '\n'.join(updates_list))
    return updates_list

  # Returns None if update should not exist
  def __convert_transaction_to_message(self, transaction):

    f = self.__mflcache.get_franchise_by_id(transaction['franchise'])
    div_id = "DIVISION" + f['division']
    div_name = self.__mflcache.get_divname_by_id(div_id)

    if (not div_name):
      div_name = div_id

    waiver_message = self.__parse_waiver_transaction(transaction['transaction'])

    return (div_name, "Franchise %s %s" % (f['name'], waiver_message))

  def __parse_waiver_transaction(self, waiver_string):
    waiver_info = waiver_string.replace(",","").split("|")
    picked = self.__mflcache.get_player_by_id(waiver_info[0])
    bid = waiver_info[1]

    message = "picked %s %s [%s] for %s" % (picked['name'], picked['position'], picked['team'], bid)

    dropped_id = waiver_info[2]
    if (dropped_id):
      dropped = self.__mflcache.get_player_by_id(dropped_id)
      message = "%s and dropped %s %s [%s]" % (message, dropped['name'], dropped['position'], dropped['team'])

    return message
