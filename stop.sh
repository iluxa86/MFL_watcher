#!/bin/bash


if [ -e ./mflwatcher.pid ]
then
  PID=$(cat ./mflwatcher.pid)
  kill $PID > /dev/null
  rm -f ./mflwatcher.pid

  ./status.sh
else
  echo "ALREADY STOPPED or PID file does not exist"
fi


