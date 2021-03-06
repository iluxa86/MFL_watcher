#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1
cd ..

mkdir -p log
mkdir -p var

if [ -e ./var/mflwatcher.pid ]
then
  echo "ALREADY STARTED. PID: "$(cat ./var/mflwatcher.pid)
else
  python3 ./src/mflwatcher_starter.py
  sleep 3
  ./bin/status.sh
fi
