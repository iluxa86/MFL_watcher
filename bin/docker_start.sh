#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1
cd ..

mkdir -p log
mkdir -p var

if [ -e storage/var ]
then
        rm -rf var
        ln -sf $(realpath storage/var) var
fi

if [ -e storage/log ]
then
        rm -rf log
        ln -sf $(realpath storage/log) log
fi

if [ -e storage/cfg ]
then
  for file in storage/cfg/*
  do
          ln -sf $(realpath $file) src/
  done
fi

rm -f var/mflwatcher.pid
python3 ./src/mflwatcher_starter.py
