#!/bin/bash

kill $(cat ./mflwatcher.pid)
rm -f ./mflwatcher.pid
