#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import sys
import traceback
from collections import defaultdict
import watcherconfig as cfg
from logger import logger
from mflcache import mfl_cache

class weeksummary_watcher:
  __api_get_results = cfg.mflwatcher['api']['results']

  # MFL info cache
  __mflcache = None
  __log_file = None

  def __init__(self, mflcache = None):
    self.__log = logger(self.__class__)
    self.__log.log("STARTING WEEK SUMMARY WATCHER")

    if (mflcache == None):
      self.__mflcache = mfl_cache()
    else:
      self.__mflcache = mflcache

  # Supposed to be run only once per week
  # Generates summary for current week
  def get_week_summary(self):
    result = []

    highscorer = (0,0)
    lowscorer = (0,1000)

    looser = (0,0)
    lucker = (0,1000)

    rivalry = (0,0,0,0,1000)
    blowout = (0,0,0,0,0)

    performance = (0,0,0,0,0)
    boring = (0,0,0,0,1000)

    bestcoach = None
    worstcoach = None


    try:
      json = requests.get(self.__api_get_results).json()
      week = json['weeklyResults']['week']
      matchups = json['weeklyResults']['matchup']

      for m in matchups:
        f1 = m['franchise'][0]
        id1 = f1['id']
        result1 = True if f1['result'] == 'W' else False
        score1 = float(f1['score'])
        #optimal1 = float(f1['opt_pts'])

        f2 = m['franchise'][1]
        id2 = f2['id']
        result2 = True if f2['result'] == 'W' else False
        score2 = float(f2['score'])
        #optimal2 = float(f2['opt_pts'])

        score_diff = abs(round(score1 - score2, 2))
        score_sum = round(score1 + score2, 2)

        # 1. Highscorer
        if score1 > highscorer[1]: highscorer = (id1, score1)
        if score2 > highscorer[1]: highscorer = (id2, score2)

        # 2. Lowscorer
        if score1 < lowscorer[1]: lowscorer = (id1, score1)
        if score2 < lowscorer[1]: lowscorer = (id2, score2)

        # 3. Looser
        if not result1 and score1 > looser[1]: looser = (id1, score1)
        if not result2 and score2 > looser[1]: looser = (id2, score2)

        # 4. Lucker
        if result1 and score1 < lucker[1]: lucker = (id1, score1)
        if result2 and score2 < lucker[1]: lucker = (id2, score2)

        # 5. Rivalry
        if score_diff < rivalry[4]: rivalry = (id1, score1, id2, score2, score_diff)

        # 6. Blowout
        if score_diff > blowout[4]: blowout = (id1, score1, id2, score2, score_diff)

        # 7. Performance
        if score_sum > performance[4]: performance = (id1, score1, id2, score2, score_sum)

        # 7. Boring
        if score_sum < boring[4]: boring = (id1, score1, id2, score2, score_sum)

      # Converting results into summary
      result.append("Please find #summary for week %s\n" % week)
      result.append(self.__convert_message_1franchise(highscorer, 'HIGHSCORER'))
      result.append(self.__convert_message_1franchise(lowscorer, 'LOWSCORER'))
      result.append(self.__convert_message_1franchise(looser, 'LOOSER'))
      result.append(self.__convert_message_1franchise(lucker, 'LUCKER'))
      result.append(self.__convert_message_2franchises(rivalry, 'RIVALRY', 'Margin'))
      result.append(self.__convert_message_2franchises(blowout, 'BLOWOUT', 'Margin'))
      result.append(self.__convert_message_2franchises(performance, 'PERFORMANCE', 'Points Combined'))
      result.append(self.__convert_message_2franchises(boring, 'BOREDOM', 'Points Combined'))

      self.__log.log('WEEKLY SUMMARY CREATED:\n' + '\n'.join(result))
    except:
      self.__log.log("UNABLE TO FETCH WEEK RESULTS")
      self.__log.log(sys.exc_info()[0])
      self.__log.log(traceback.format_exc())

    return '\n'.join(result)

  def __convert_message_1franchise(self, info, label):
    f_info = self.__mflcache.get_franchise_by_id(info[0])
    divname = self.__mflcache.get_divname_by_id(f_info['division'])
    return '%s OF THE WEEK\n%s - %s\n%s\n' % (label, f_info['name'], info[1], divname)

  def __convert_message_2franchises(self, info, label1, label2):
    f_info = self.__mflcache.get_franchise_by_id(info[0])
    f2_info = self.__mflcache.get_franchise_by_id(info[2])
    divname = self.__mflcache.get_divname_by_id(f_info['division'])
    return '%s OF THE WEEK\n%s - %s\n%s - %s\n%s - %s\n%s\n' % \
           (label1, f_info['name'], info[1], f2_info['name'], info[3], label2, info[4], divname)
