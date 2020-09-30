#!/bin/bash
service ssh restart
mongod --bind_ip_all &
./pollenisator.py &
./startWorker.sh &
myvar=`mongo pollenisator --quiet --eval "db.getCollectionNames()"`
while [[ $myvar != *"calendars"* ]]; do
    sleep 2
    myvar=`mongo pollenisator --quiet --eval "db.getCollectionNames()"`
done
ps -u | grep "celery -A" | awk 'NR>1 {print $2}' | xargs kill -9
./startWorker.sh
