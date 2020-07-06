# Build docker

docker build -t pollenisator .

# Run worker (if it's for local to local add --net=host)

docker run -d pollenisator

or enter docker (if it's for local to local add --net=host)

docker run -ti pollenisator /bin/bash

# Stop docker

docker container ls
docker stop Xxxxxxx
