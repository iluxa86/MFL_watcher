import watcherconfig as cfg
import requests
from logger import logger
from time import sleep

class mfl_login:

  __login_url = cfg.mflwatcher['login']['url']
  __mfl_user = cfg.mflwatcher['login']['login']
  __mfl_pwd = cfg.mflwatcher['login']['password']
  __cookies = None

  # MFL info cache
  __players_dict = dict()
  __franchises_dict = dict()
  __div_map = cfg.mflwatcher['div_map']

  # Reference to logger file
  __log = None

  def __init__(self):
    self.__log = logger(self.__class__)
    self.__log.log("STARTING MFL CACHE")

  # NOT REALLY USED BUT CAN BE USEFUL FOR FUTURE
  def __login(self):
    url = self.__login_url % (self.__mfl_user, self.__mfl_pwd)
    resp = requests.get(url)

    if (resp.status_code == "200"):
      self.__cookies = resp.cookies
      return True
    else:
      self.__log.log("UNABLE TO LOGIN")
      return False

  def get_cookies(self):
    while (self.__cookies == None):
      self.__login()
      sleep(1)

    return self.__cookies

  def refresh_cookies(self):
    self.__login()
