#!/bin/bash
ssl=false
if [ "$1" ]; then
	ssl=true
fi

if [ "$ssl" == true ]
then
	echo "Launching mongod with ssl"
	mongod --dbpath=/var/lib/mongodb --sslMode requireSSL --sslPEMKeyFile ./ssl/server.pem --sslCAFile ./ssl/ca.pem -f /etc/mongod.conf
else
	echo "Launching mongod without ssl"
	mongod --dbpath=/var/lib/mongodb -f /etc/mongod.conf
fi

