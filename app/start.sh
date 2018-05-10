#!/bin/bash

PORT=5003
IP=0.0.0.0
FOREGROUND=false
FLASK_APP=run.py
export FLASK_APP

venv=../venv/bin/activate

display_usage() { 
	echo "Start flask instance."
	echo -e "\nUsage: ./start.sh [arguments] \n" 
	echo -e "\t-p <port> = start on a specific port (default = $PORT)"
	echo -e "\t-i <ip>   = listen on a specific IP address (default = 0.0.0.0)"
	echo -e "\t-d        = debug mode: run in foreground (default = background using screen)"
	echo -e "\t-h        = print this help message \n"
        exit 0
} 


options=':p:i:dh'
while getopts $options option
do
    case $option in
        p  )    PORT=$OPTARG;;
        i  )    IP=$OPTARG;;
        d  )    FOREGROUND=true; PINGTHIS_ENV=debug;;
        h  )    display_usage;;
    esac
done

shift $(($OPTIND - 1))


source $venv

if ($FOREGROUND); then 
	flask run --port $PORT --host $IP
else
	PINGTHIS_ENV=prod
	export PINGTHIS_ENV
	screen -d -m -S pingthis flask run --port $PORT --host $IP
fi
