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
import schedule
import yaml
from logger import logger
from datetime import datetime

log = logger('mflwatcher_starter.py')

def mflwatcher():
    bot = TelegramBot()
    cache = mfl_cache()
    dw = draft_watcher(cache, search_images=cfg.draftwatcher_images_enabled)
    tw = trade_watcher(cache)
    ww = waiver_watcher(cache)
    weekly_summary = weeksummary_watcher(cache)
    schedule_dictionary = dict()

    if cfg.run_once:
        log.log("Configured to run only once")
        try:
            with open(cfg.scheduled_tasks_file, "r") as file:
                schedule_dictionary = yaml.full_load(file.read())
        except FileNotFoundError:
            log.log("Failed to open file: %s" % cfg.scheduled_tasks_file)

    def waiverupdates():
        updates = ww.get_waiver_updates()
        for update in updates:
            bot.send_message(update[0], binary_image=update[1], GIF=True)
            sleep(10)

    # Scheduled events
    if cfg.waiverwatcher_enabled:
        label = 'waiverwatcher_schedule'
        if cfg.run_once and label in schedule_dictionary.keys() and schedule_dictionary[label] < datetime.now():
            log.log("Running waiverwatcher_schedule once based on yaml schedule")
            waiverupdates()
        cfg.waiverwatcher_schedule.do(waiverupdates)
        schedule_dictionary[label] = cfg.waiverwatcher_schedule.next_run

    if cfg.weeksummarywatcher_enabled:
        label = 'weeksummarywatcher_schedule'
        if cfg.run_once and label in schedule_dictionary.keys() and schedule_dictionary[label] < datetime.now():
            bot.send_message(weekly_summary.get_week_summary())
            log.log("Running waiverwatcher_schedule once based on yaml schedule")
        cfg.weeksummarywatcher_schedule.do(lambda: bot.send_message(weekly_summary.get_week_summary()))
        schedule_dictionary[label] = cfg.weeksummarywatcher_schedule.next_run

    # Permanently checking events
    while True:
        if cfg.draftwatcher_enabled:
            for update in dw.get_draft_update():
                bot.send_message(update[0], binary_image=update[1])
                sleep(10)

        if cfg.tradewatcher_enabled:
            for update in tw.get_trade_update():
                bot.send_message(update[0], binary_image=update[1])
                sleep(10)

        if cfg.run_once:
            with open(cfg.scheduled_tasks_file, "w+") as file:
                file.write(yaml.dump(schedule_dictionary))
                break

        schedule.run_pending()
        sleep(cfg.update_period_sec)


def mflwatcher_daemon():
    import daemon
    from daemon import pidfile
    import os

    dir_path = os.getcwd()
    print("Working dir: " + dir_path)
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
