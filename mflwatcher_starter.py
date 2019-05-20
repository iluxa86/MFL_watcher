#!/usr/bin/python
# -*- coding: utf-8 -*-

import watcherconfig as cfg
from telegrambot import telegram_bot
from mflcache import mfl_cache
from draftwatcher import draft_watcher
from tradewatcher import trade_watcher
from time import sleep

def main():
  bot = telegram_bot()
  cache = mfl_cache()
  dw = draft_watcher(cache)
  tw = trade_watcher(cache)

  while True:
    updates = dw.get_draft_update()
    for update in updates:
      bot.send_message(update)

    updates = tw.get_trade_update()
    for update in updates:
      bot.send_message(update)

    sleep(cfg.update_period_sec)
main()
