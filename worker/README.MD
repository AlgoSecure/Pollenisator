# Build docker
## Generic command
docker build -t pollenisator .
## Pull last version of repo (update pollenisator only)
docker build --build-arg CACHEBUST=$(date +%s) -t pollenisator . 
## Rebuild all tools (updated them)
docker build --no-cache -t pollenisator .

# Run worker (if it's for local to local add --net=host)

docker run -d pollenisator

or enter docker (if it's for local to local add --net=host)

docker run -ti pollenisator /bin/bash

# Stop docker

docker container ls
docker stop Xxxxxxx
