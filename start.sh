#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1

if [ -e ./mflwatcher.pid ]
then
  echo "ALREADY STARTED. PID: "$(cat ./mflwatcher.pid)
else
  python mflwatcher_starter.py
fi
