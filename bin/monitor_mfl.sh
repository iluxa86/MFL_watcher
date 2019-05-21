#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1
cd ..

# Checks .email file for address to send alerts to
email=$(cat ./.email)

alert_file="var/alert.triggered"
status_cmd="bin/status.sh"
log_file="log/mflwatcher.log"

if [[ $($status_cmd | grep -c "RUNNING") -ne 1 ]]
then
        if [ ! -e $alert_file ]
        then
                tail -50 $log_file | mail -s "ALERT! MFL WATCHER IS DOWN" $email
                mkdir -p var
                touch $alert_file
        fi
else
	if [ -e $alert_file ]
	then
		echo "EVERYTHING IS FINE" | mail -s "MFL WATCHER IS BACK TO NORMAL" $email
		rm -f $alert_file
	fi
fi
