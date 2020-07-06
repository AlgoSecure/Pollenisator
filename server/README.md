Build docker
docker build --build-arg SSHPASSWORD=pollenisator123 -t pollenisatorserver . --no-cache

Run docker, port can be changed to whatever you want, just change the config file of workers and clients
docker run -p 22:22 -p 27017:27017 -d pollenisatorserver

for example, run on port 22222
docker run -p 22222:22 -p 27017:27017 -d pollenisatorserver
and change config/client.cfg as well as worker/config/client.cfg 
sftp_port:22222
