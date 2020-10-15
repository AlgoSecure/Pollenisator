# Build docker
## Generic command
docker build -t pollenisator .

## Rebuild all tools (updated them)
docker build --no-cache -t pollenisator .

# Run worker (if it's for local to local add --net=host)

docker run -v `pwd`/../:/home/Pollenisator/ -d pollenisator

or enter docker (if it's for local to local add --net=host)

docker run -v `pwd`/../:/home/Pollenisator/ -ti pollenisator /bin/bash

# Stop docker

docker container ls
docker stop Xxxxxxx
