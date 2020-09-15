#!/usr/bin/python3
# -*- coding: utf-8 -*-

import watcherconfig as cfg
from telegrambot import TelegramBot
from mflcache import mfl_cache
from draftwatcher import draft_watcher
from tradewatcher import trade_watcher
from waiverwatcher import waiver_watcher
from weeksummarywatcher import weeksummary_watcher
from time import sleep
import daemon
import schedule
from daemon import pidfile

def mflwatcher():
  bot = TelegramBot()
  cache = mfl_cache()
  dw = draft_watcher(cache, search_images=cfg.draftwatcher_images_enabled)
  tw = trade_watcher(cache)
  ww = waiver_watcher(cache)
  weekly_summary = weeksummary_watcher(cache)

  def waiverupdates():
    for update in ww.get_waiver_updates():
      bot.send_message(update[0], update[1], GIF=True)
      sleep(10)

  # Scheduled events
  if cfg.waiverwatcher_enabled:
    cfg.waiverwatcher_schedule.do(waiverupdates())

  if cfg.weeksummarywatcher_enabled:
    cfg.weeksummarywatcher_schedule.do(lambda: bot.send_message(weekly_summary.get_week_summary()))

  # Permanently checking events
  while True:
    if cfg.draftwatcher_enabled:
      for update in  dw.get_draft_update():
        bot.send_message(update[0], binary_image=update[1])
        sleep(10)

    if cfg.tradewatcher_enabled:
      for update in tw.get_trade_update():
        bot.send_message(update[0], binary_image=update[1])
        sleep(10)

    schedule.run_pending()
    sleep(cfg.update_period_sec)

def mflwatcher_daemon():
  import os

  dir_path = os.getcwd()
  print ("Working dir: " + dir_path)
  with daemon.DaemonContext(
    working_directory=dir_path,
    pidfile=pidfile.TimeoutPIDLockFile(dir_path + "/var/mflwatcher.pid")
  ) as context:
    mflwatcher()

if __name__ == "__main__":

  if (cfg.daemon):
    mflwatcher_daemon()
  else:
    mflwatcher()
