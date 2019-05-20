#!/bin/bash

if [ -e ./mflwatcher.pid ]
then
  echo "ALREADY STARTED. PID: "$(cat ./mflwatcher.pid)
else
  python mflwatcher_starter.py
fi
