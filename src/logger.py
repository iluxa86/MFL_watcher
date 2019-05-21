import watcherconfig as cfg
import datetime
import os

class logger:
  __classname = None
  __log_filename = None

  # Referece to the open log file
  __log_file = None

  def __init__(self, classname):
    self.__classname = classname
    self.__log_filename = cfg.mflwatcher['files']['log']
    self.__log_file = self.__open_log()

  def __open_log(self):
      try:
        return open(self.__log_filename,"a+")
      except:
        print "CANNOT OPEN LOG FILE"

  def log(self, log_message):
    record =  "%s [%s] %s" % (str(datetime.datetime.now()), self.__classname, log_message)
    try:
      print record
      self.__log_file.write(record + "\n")
      self.__log_file.flush()
    except:
      print "Working dir: " + os.getcwd()
      print "CANNOT WRITE TO LOG FILE"
      self.__open_log()
