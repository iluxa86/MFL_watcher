import requests
import sys
import traceback
import random
import watcherconfig as cfg
from logger import logger
from mflcache import mfl_cache

class draft_watcher:
  __api_get_draft = cfg.mflwatcher['api']['draft']

  # MFL info cache
  __mflcache = None
  __last_picks_dict = dict()

  __picks_file = cfg.mflwatcher['files']['picks']
  __log_file = None

  __adjectives = cfg.mflwatcher['draft_adjectives']
  __verbs = cfg.mflwatcher['draft_verbs']

  def __init__(self, mflcache = None):
    self.__log = logger(self.__class__)
    self.__log.log("STARTING MFL WATCHER")

    if (mflcache == None):
      self.__mflcache = mfl_cache()
    else:
      self.__mflcache = mflcache

    self.__restore_last_picks()

  def get_draft_update(self):

    draft_updates = list()
    try:
      resp = requests.get(self.__api_get_draft).json()
      json = resp['draftResults']['draftUnit']

      for div_draft in json:
        div_id = div_draft['unit']

        new_picks = self.__find_new_picks_for_div(div_id, div_draft)
        self.__log.log("NEW PICKS FOUND FOR " + div_id + " : " + str(len(new_picks)))

        for new_pick in new_picks:
          draft_updates.append(self.__convert_pick_to_message(new_pick, div_id))
          self.__log.log("FOUND NEW PICK FOR " + div_id + " : " + str(new_pick))

        # This section just needed for logging
        if (div_id in self.__last_picks_dict):
          last_known_pick = self.__last_picks_dict[div_id]
        else:
          last_known_pick = None
        self.__log.log("LAST KNOWN PICK FOR " + div_id + " : " + str(last_known_pick))

      # Dump last picks into file
      self.__store_last_picks()

    except:
      self.__log.log("UNABLE TO FETCH DRAFT PICKS")
      self.__log.log(sys.exc_info()[0])
      self.__log.log(traceback.format_exc())

    return draft_updates

  def __store_last_picks(self):
    # Need to store last picks to file here
    f= open(self.__picks_file,"w+")

    for entry in self.__last_picks_dict:
      record = "%s %s\n" % (entry, self.__last_picks_dict[entry])
      f.write(record)
    f.close()

  def __restore_last_picks(self):
    try:
      f= open(self.__picks_file,"r")

      for line in f:
        div = line.split()[0]
        pick = line.split()[1]

        self.__last_picks_dict[div] = pick
      f.close()
    except:
      self.__log.log("NO PICKS STORE FILE. STOPPING")
      self.__log.log(sys.exc_info()[0])
      self.__log.log(traceback.format_exc())
      raise Exception("CANNOT LOAD PICKS FILE")

  def __convert_pick_to_message(self, pick, div_id):

    message = ""
    pick_id = str(pick[0])

    franchise = str(pick[2]['name'])
    comment = str(pick[3].encode('utf8')).replace('\n',' ')
    div_name = self.__mflcache.get_divname_by_id(div_id)

    # If None - no pick was made
    if pick[1] != None:
      player = str(pick[1]['name'])
      pos = str(pick[1]['position'])
      team = str(pick[1]['team'])
      adj = random.choice(self.__adjectives)
      verb = random.choice(self.__verbs)

      message = "Division %s update!\n" \
                "Under %s pick\nTeam \"%s\" %s " \
                "%s %s from %s - %s\n" \
                % (div_name, pick_id, franchise, verb, adj, pos, team, player)
    else:
      message = "Division %s update!\n" \
                "(%s) No pick was made by team \"%s\"\n" \
                % (div_name, pick_id, franchise)

    if comment != "":
      message = message + "Comment: " + comment

    return message

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
          player = self.__mflcache.get_player_by_id(player_id)
          franchise = self.__mflcache.get_franchise_by_id(pick['franchise'])
          new_pick = (pick_id, player, franchise, comment)
          new_picks.append(new_pick)
          self.__last_picks_dict[div_id] = pick_id
        else:
          if (pick_id == last_known_pick_id):
            passed_known_pick = True

    return new_picks
