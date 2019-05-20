#!/usr/bin/python
# -*- coding: utf-8 -*-

import watcherconfig as cfg
from telegrambot import telegram_bot
from mflcache import mfl_cache
from draftwatcher import draft_watcher
from tradewatcher import trade_watcher
from time import sleep
import daemon
from daemon import pidfile

def mflwatcher():
  bot = telegram_bot()
  cache = mfl_cache()
  dw = draft_watcher(cache)
  tw = trade_watcher(cache)

  while True:
    if (cfg.draftwatcher_enabled):
      updates = dw.get_draft_update()
      for update in updates:
        bot.send_message(update)

    if (cfg.tradewatcher_enabled):
      updates = tw.get_trade_update()
      for update in updates:
        bot.send_message(update)

    sleep(cfg.update_period_sec)

def mflwatcher_daemon():
  import os

  dir_path = os.getcwd()
  print "Working dir: " + dir_path
  with daemon.DaemonContext(
    working_directory=dir_path,
    pidfile=pidfile.TimeoutPIDLockFile(dir_path + "/mflwatcher.pid")
  ) as context:
    mflwatcher()

if __name__ == "__main__":

  if (cfg.daemon):
    mflwatcher_daemon()
  else:
    mflwatcher()
