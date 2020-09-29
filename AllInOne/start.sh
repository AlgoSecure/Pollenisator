#!/bin/bash
service ssh restart
mongod --bind_ip_all &
./pollenisator.py &
./startWorker.sh &
sleep 15
ps -u | grep "celery -A" | cut -d ' ' -f 9 | xargs kill -9
./startWorker.sh
