#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1

if [ -e ./mflwatcher.pid ]
then
  PID=$(cat ./mflwatcher.pid)
  if ps -p $PID > /dev/null
  then
    echo "$PID - RUNNING"
    exit 0
  else
    echo "$PID - STOPPED"
    exit 1
  fi
else
  echo "NO PID - STOPPED"
  exit 2
fi




