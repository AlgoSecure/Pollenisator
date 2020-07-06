#!/bin/bash
if [[ $1 == "" ]]
then
	echo "Usage: ./initServerSSL.sh <ip or domain of host>"
	exit 1
fi
domain=$1
openssl req -out ca.pem -new -x509 -days 3650 -subj "/C=AU/ST=NSW/O=Organisation/CN=root/emailAddress=user@domain.com" -passout pass:"password"
echo "42" > file.srl
openssl genrsa -out server.key 2048
openssl req -key server.key -new -out server.req -subj  "/C=AU/ST=NSW/O=Organisation/CN=$domain/emailAddress=user@domain.com"
openssl x509 -req -in server.req -CA ca.pem -CAkey privkey.pem -CAserial file.srl -out server.crt -days 3650 -passin pass:"password"
cat server.key server.crt > server.pem
openssl verify -CAfile ca.pem server.pem
echo "Do you want to create a client certificat ? (Y/n)"
read answer
if [[ $answer == "n" ]]
then
	exit 0
fi
openssl genrsa -out client.key 2048
openssl req -key client.key -new -out client.req -subj "/C=AU/ST=NSW/O=Organisation/CN=client1/emailAddress=user@domain.com"
openssl x509 -req -in client.req -CA ca.pem -CAkey privkey.pem -CAserial file.srl -out client.crt -days 3650 -passin pass:"password"
cat client.key client.crt > client.pem
openssl verify -CAfile ca.pem client.pem
