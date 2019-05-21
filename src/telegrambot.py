import watcherconfig as cfg
import requests
import urllib
import sys
from logger import logger
import traceback

class telegram_bot():
  __log = None
  __api_url = cfg.telegram['api_url']
  __bot_token = cfg.telegram['token']
  __chat_name =  cfg.telegram['chatname']

  def __init__(self):
    self.__log = logger(self.__class__)

  def send_message(self, message):
    encoded_message = urllib.quote_plus(message)
    url = self.__api_url % (self.__bot_token, self.__chat_name, encoded_message)

    try:
      requests.get(url)
      return True
    except:
      self.__log.log("UNABLE TO SEND MESSAGE")
      self.__log.log(sys.exc_info()[0])
      self.__log.log(traceback.format_exc())
      return False

  def send_messages(self, messages):
    for message in messages:
      self.send_message(message)
