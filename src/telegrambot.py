import watcherconfig as cfg
import sys
from logger import logger
import traceback
import telegram
import telegram.error
import time

class TelegramBot():
    __log = None
    __bot_token = cfg.telegram['token']
    __chat_name = cfg.telegram['chatname']
    __bot = None

    def __init__(self):
        self.__log = logger(self.__class__)
        self.__bot = telegram.Bot(self.__bot_token)

    def send_message(self, message, binary_image=None, GIF=False):
        self.__log.log("SENDING MESSAGE WITH LENGTH: %s" % len(message))

        try:
            if binary_image:
                try:
                    # Sending image w caption
                    if len(message) > 1023:
                        # Splitting image and caption
                        if GIF:
                            self.__bot.send_animation(self.__chat_name, binary_image)
                        else:
                            self.__bot.send_photo(self.__chat_name, binary_image)
                        self.__bot.send_message(self.__chat_name, message, parse_mode=telegram.ParseMode.HTML)
                    else:
                        if GIF:
                            self.__bot.send_animation(self.__chat_name, binary_image, caption=message, parse_mode=telegram.ParseMode.HTML)
                        else:
                            self.__bot.send_photo(self.__chat_name, binary_image, caption=message, parse_mode=telegram.ParseMode.HTML)
                except telegram.NetworkError as e:
                    self.__log.log(e)
                    self.__log.log(sys.exc_info()[0])
                    self.__log.log(traceback.format_exc())
                    self.__log.log("UNABLE TO SEND MEDIA MESSAGE. TRYING TO SEND PLAIN TEXT")
                    self.__bot.send_message(self.__chat_name, message, parse_mode=telegram.ParseMode.HTML)
            else:
                # Sending text only
                self.__bot.send_message(self.__chat_name, message, parse_mode=telegram.ParseMode.HTML)
            return True
        except:
            self.__log.log("UNABLE TO SEND MESSAGE")
            self.__log.log(sys.exc_info()[0])
            self.__log.log(traceback.format_exc())
            return False

    def send_messages(self, messages):
        for message in messages:
            self.send_message(message)
            time.sleep(10)
