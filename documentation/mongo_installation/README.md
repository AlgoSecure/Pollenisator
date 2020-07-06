
## Requirements ##

## Install Backbone database: Mongo


### 1. Install mongo 3.6+: 
On Ubuntu 14.04 or 16.04 refer to that link: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

On Ubuntu 15.04 (replace all 3.0 occurence with 3.6): https://medium.com/@paulrohan/how-to-install-mongodb-on-ubuntu-15-04-and-15-10-9301e53a0d94

Any other, please refer to that link. https://docs.mongodb.com/manual/installation/ 

If you installed it correctly, you can run these without error result must be 3.6 or higher, and service running

`$ mongo --version`

`$ sudo service mongod start`

`$ sudo service mongod status`

`$ sudo service mongod stop`

###  2. Add an Administrative User for mongo
Start mongo client

`mongo`

And type this:

`use admin`

Then create your user replacing admin and password with the user/password of your choice.

`db.createUser({user:"admin", pwd:"password", roles:[{role:"root", db:"admin"}]});`

Then exit

`exit`


Open the MongoDB configuration file using sudo (sudo vi mongodb.conf).

`$ sudo nano /etc/mongod.conf`

In the #security section, we'll remove the hash in front of security to enable the stanza. Then we'll add the authorization setting. When we're done, the lines should look like the excerpt below:

`security:`

`  authorization: "enabled"`

Then exit and restart service:

`sudo systemctl restart mongod`

`sudo systemctl status mongod`

If we see Active: active (running) in the output and it ends with something like the text below, we can be sure the restart command was successful:

try connect to the user you created replacing AdminSammy with your admin username, enter password when prompted
mongo -u admin -p --authenticationDatabase admin


### 3. Use ssl with mongo (recommended if mongo is exposed on a public ip) 

 if not done yet, clone Pollenisator to the directory of you choice (~ in our case)

`$ cd ~ && $ git clone https://github.com/AlgoSecure/Pollenisator.git && cd Pollenisator/ssl`

Generate the certificates with your server's domain

`$ ./initServerSSL.sh <domain>`

And Duplicate the CA.pem and client.pem file on each of the clients Pollenisator/ssl/ folder

For example, I will do this using scp from the client machine Pollenisator/ssl/ folder and copy the CA.pem and client.pem from my server which has the ip 10.0.0.127 and a user named alogsecure.

`$ scp algosecure@10.0.0.127:~/Pollenisator/ssl/client.pem .`

`$ scp algosecure@10.0.0.127:~/Pollenisator/ssl/ca.pem .`

After generating the .pem files, now you can run mongod with the custom script startServices.sh

`$ cd ..`

`$ sudo service mongod stop`

`$ ./startServices.sh`


### 4. Open mongo to you other ips

All slaves and the master have to connect to the same mongo database.

On the server where mongodb is installed, enter:

`$ sudo service mongod stop`

`$ ifconfig`

And write down the IPs to which it will possible to connect.

Edit the mongo configuration file on the server where mongodb is installed :

`$ sudo nano /etc/mongod.conf`

Search for "bindIp"
`# network interfaces`
`net:`
`  port: 27017`
`  bindIp: 127.0.0.1`

bindIp authorize the mongodb server to accept.  127.0.0.1 is default so only your machine can connect to it right now.

Add the IPs you wrote down earlier separated by commas.

`  bindIp: 127.0.0.1, XXX.XXX.XXX.XXX, YYY.YYY.YYY.YYY`

Then save and exit.

Now your server should be open to all the computers that can talk to your bindIps.
** If one of your bindIp is open on the internet ** make sure to filter by IP if possible. 


### 5. (Recommended) Restrain mongo access to your know IPs

If you already have a firewall, add some basic constraints to filter by ip. 

IF NOT, follow this section to install persistence iptables (basic firewall rules) on your local server

First, install iptables-persistent. Keep the already-existing rules if you are asked.

`$ apt-get install iptables-persistent`

Then edit the rules:

`$ sudo nano /etc/iptables/rules.v4`

Search for

`*filter`

And add these two lines below for each ip to allow:

`-A INPUT -s <the allowed ip>/32 -p tcp --dport 27017 -m state --state NEW, ESTABLISHED -j ACCEPT`

`-A OUTPUT -d <the allowed ip>/32 -p tcp --sport 27017 -m state --state ESTABLISHED -j ACCEPT`

And Then these two lines below to disallow every other connection on this port:

`-A INPUT -p tcp --dport 27017 -m state --state NEW, ESTABLISHED -j DROP`

`-A OUTPUT -p tcp --sport 27017 -m state --state ESTABLISHED -j DROP`

Save and exit.

Finally, reload the rules and restart mongo

`$ sudo service iptables-persistent reload`

or depending on the version

`$ sudo service netfilters-persistent reload`


`$ sudo service mongod start`