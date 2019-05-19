#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import urllib
import sys
import datetime
import traceback
import random
from time import sleep

import watcherconfig as cfg

class Config:
  def __init__(self):
    print "Config"

class TelegramBot:
  __api_url = cfg.telegram['api_url']
  __bot_token = cfg.telegram['token']
  __chat_name =  cfg.telegram['chatname']

  def send_message(self, message):
    encoded_message = urllib.quote_plus(message)
    url = self.__api_url % (self.__bot_token, self.__chat_name, encoded_message)

    try:
      requests.get(url)
      return True
    except:
      print "[TelegramBot] UNABLE TO SEND MESSAGE"
      print "[TelegramBot] " + sys.exc_info()[0]
      return False

class MFLWatcher:

  __login_url = cfg.mflwatcher['login']['url']
  __login = cfg.mflwatcher['login']['login']
  __password = cfg.mflwatcher['login']['password']
  __cookies = None

  __api_get_player = cfg.mflwatcher['api']['player']
  __api_get_draft = cfg.mflwatcher['api']['draft']
  __api_get_league = cfg.mflwatcher['api']['league']

  # MFL info cache
  __players_dict = dict()
  __franchises_dict = dict()
  __draft_dict = dict()
  __last_picks_dict = dict()

  __picks_file = cfg.mflwatcher['files']['picks']
  __log_filename = cfg.mflwatcher['files']['log']
  __log_file = None

  __adjectives = cfg.mflwatcher['draft_adjectives']
  __verbs = cfg.mflwatcher['draft_verbs']
  __div_map = cfg.mflwatcher['div_map']

  def __init__(self):
    self.__log_file = self.__open_log()
    self.__get_league()
    self.__get_all_players()
    self.__restore_last_picks()


  def __open_log(self):
    try:
      # Need to store last picks to file here
      return open(self.__log_filename,"a+")
    except:
      print "CANNOT OPEN LOG FILE"

  def __log(self, log_message):
    print "%s [%s] %s" % (str(datetime.datetime.now()), self.__class__, log_message)
    try:
      self.__log_file.write("%s [%s] %s\n" % (str(datetime.datetime.now()), self.__class__, log_message))
      self.__log_file.flush()
    except:
      print "CANNOT WRITE TO LOG FILE"
      self.__open_log()

  # NOT REALLY USED BUT CAN BE USEFUL FOR FUTURE
  def __log_in(self):
    url = self.__login_url % (self.__login, self.__password)
    resp = requests.get(url)

    if (resp.status_code == "200"):
      self.__cookies = resp.cookies
      return True
    else:
      self.__log("UNABLE TO LOGIN")
      return False

  def get_draft_update(self):

    try:
      resp = requests.get(self.__api_get_draft).json()
      json = resp['draftResults']['draftUnit']

      draft_updates = list()

      for div_draft in json:
        div_id = div_draft['unit']

        new_picks = self.__find_new_picks_for_div(div_id, div_draft)
        self.__log("NEW PICKS FOUND FOR " + div_id + " : " + str(len(new_picks)))

        for new_pick in new_picks:
          draft_updates.append(self.__convert_pick_to_message(new_pick, div_id))
          self.__log("FOUND NEW PICK FOR " + div_id + " : " + str(new_pick))

        if (div_id in self.__last_picks_dict):
          last_known_pick = self.__last_picks_dict[div_id]
        else:
          last_known_pick = None
        self.__log("LAST KNOWN PICK FOR " + div_id + " : " + str(last_known_pick))

      # Dump last picks into file
      self.__store_last_picks()

      return draft_updates

    except:
      self.__log("UNABLE TO FETCH DRAFT PAGE")
      self.__log(sys.exc_info()[0])
      traceback.print_exc(file=sys.stdout)
      return False

  def get_player_by_id(self, id):
    # Getting id from cache
    # TO DO: Fetch from API if cache is empty
    if (id in self.__players_dict):
      return self.__players_dict[id]

  def get_franchise_by_id(self, id):
    # Getting id from cache
    if (id in self.__franchises_dict):
      return self.__franchises_dict[id]

  def __store_last_picks(self):
    # Need to store last picks to file here
    f= open(self.__picks_file,"w+")

    for entry in self.__last_picks_dict:
      record = "%s %s" % (entry, self.__last_picks_dict[entry])
      f.write(record)
    f.close()

  def __restore_last_picks(self):
    # Need to store last picks to file here

    try:
      f= open(self.__picks_file,"r")

      for line in f:
        div = line.split()[0]
        pick = line.split()[1]

        self.__last_picks_dict[div] = pick
      f.close()
    except:
      self.__log("NO STORE FILE. NEW ONE WILL BE CREATED")


  def __convert_pick_to_message(self, pick, div_id):
    pick_id = str(pick[0])
    player = str(pick[1]['name'])
    pos = str(pick[1]['position'])
    team = str(pick[1]['team'])
    franchise = str(pick[2]['name'])
    comment = str(pick[3].encode('utf8')).replace('\n',' ')
    div_name = self.__div_map[div_id]
    adj = random.choice(self.__adjectives)
    verb = random.choice(self.__verbs)

    message = "Division %s update!\n" \
              "Under %s pick\nTeam \"%s\" %s " \
              "%s %s from %s - %s\n" \
              % (div_name, pick_id, franchise, verb, adj, pos, team, player)

    if comment != "":
      message = message + "Comment: " + comment

    return message

  def __get_all_players(self):
    try:
      url = self.__api_get_player % ""
      players_data = requests.get(url).json()['players']['player']

      for p in players_data:
        id = p['id']
        p_dict = dict()
        p_dict['name'] = p['name']
        p_dict['position'] = p['position']
        p_dict['team'] = p['team']
        self.__players_dict[id] = p_dict

      self.__log("PLAYERS FETCHED")
      return True
    except:
      self.__log("UNABLE TO FETCH PLAYERS")
      self.__log(sys.exc_info()[0])
      return False

  def __get_league(self):
    try:
      f_data = requests.get(self.__api_get_league).json()['league']['franchises']['franchise']

      for f in f_data:
        id = f['id']
        f_dict = dict()
        f_dict['name'] = f['name']
        f_dict['division'] = f['division']
        self.__franchises_dict[id] = f_dict

      self.__log("FRANCHISES FETCHED")
      return True
    except:
      self.__log("UNABLE TO FETCH FRANCHISES")
      self.__log(sys.exc_info()[0])
      return False

  def __find_new_picks_for_div(self, div_id, draft_unit_dict):
    picks = draft_unit_dict['draftPick']
    new_picks = list()

    last_known_pick_id = None
    passed_known_pick = False

    if (div_id in self.__last_picks_dict):
      last_known_pick_id = self.__last_picks_dict[div_id]
    else:
      # We do not have any picks stored
      passed_known_pick = True

    for pick in picks:
      player_id = pick['player']
      pick_id = pick['round'] + "." + pick['pick']

      # We reached picks that were not selected yet
      if (player_id == ""):
        return new_picks
      else:
        if (passed_known_pick):
          comment = pick['comments']
          player = self.get_player_by_id(player_id)
          franchise = self.get_franchise_by_id(pick['franchise'])
          new_pick = (pick_id, player, franchise, comment)
          new_picks.append(new_pick)
          self.__last_picks_dict[div_id] = pick_id
        else:
          if (pick_id == last_known_pick_id):
            passed_known_pick = True

    return new_picks


def main():
  bot = TelegramBot()
  watcher = MFLWatcher()

  while True:
    updates = watcher.get_draft_update()

    for update in updates:
      bot.send_message(update)
      print update
    sleep(60)

main()
