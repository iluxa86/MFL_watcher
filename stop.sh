#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1

if [ -e ./mflwatcher.pid ]
then
  PID=$(cat ./mflwatcher.pid)
  kill $PID > /dev/null
  rm -f ./mflwatcher.pid

  ./status.sh
else
  echo "ALREADY STOPPED or PID file does not exist"
fi


