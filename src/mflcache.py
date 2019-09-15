import watcherconfig as cfg
import requests
import sys
from logger import logger

class mfl_cache:
  __api_get_player = cfg.mflwatcher['api']['player']
  __api_get_league = cfg.mflwatcher['api']['league']

  # MFL info cache
  __players_dict = dict()
  __franchises_dict = dict()
  __div_map = cfg.mflwatcher['div_map']

  # Reference to logger file
  __log = None

  def __init__(self):
    self.__log = logger(self.__class__)
    self.__log.log("STARTING MFL CACHE")
    self.__get_league()
    self.__get_all_players()

  def get_player_by_id(self, id):
    # Getting id from cache
    # TO DO: Fetch from API if cache is empty
    if (id in self.__players_dict):
      return self.__players_dict[id]
    else:
      return None

  def get_franchise_by_id(self, id):
    # Getting id from cache
    if (id in self.__franchises_dict):
      return self.__franchises_dict[id]
    else:
      return None

  def get_divname_by_id(self, div_id):
    if (div_id in self.__div_map):
      return self.__div_map[div_id]
    else:
      return None

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

      self.__log.log("PLAYERS FETCHED")
      return True
    except:
      self.__log.log("UNABLE TO FETCH PLAYERS")
      self.__log.log(sys.exc_info()[0])
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

      self.__log.log("FRANCHISES FETCHED")
      return True
    except:
      self.__log.log("UNABLE TO FETCH FRANCHISES")
      self.__log.log(sys.exc_info()[0])
      return False
