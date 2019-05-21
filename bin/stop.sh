#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1
cd ..

if [ -e ./var/mflwatcher.pid ]
then
  PID=$(cat ./var/mflwatcher.pid)
  kill $PID > /dev/null
  rm -f ./var/mflwatcher.pid

  ./bin/status.sh
else
  echo "ALREADY STOPPED or PID file does not exist"
fi


