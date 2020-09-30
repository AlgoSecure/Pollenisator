# Build docker

## Generic command
docker build -t allinone-pollenisator .

## Rebuild all tools (update them)
docker build --no-cache -t allinone-pollenisator .

# Run worker (if it's for local to local add --net=host)

```
sudo apt-get install x11-xserver-utils
xhost +local:docker
```

```docker run --env="DISPLAY" -v `pwd`/results:/etc/Pollenisator/files/results --volume="$HOME/.Xauthority:/root/.Xauthority:rw" -v /tmp/.X11-unix/X0:/tmp/.X11-unix/X0 -d allinone-pollenisator```

or enter docker

```docker run --env="DISPLAY" -v `pwd`/results:/etc/Pollenisator/files/results --volume="$HOME/.Xauthority:/root/.Xauthority:rw" -v /tmp/.X11-unix/X0:/tmp/.X11-unix/X0 -ti allinone-pollenisator /bin/bash```

and run
./start.sh

# Stop docker

```
docker ps
docker stop Xxxxxxx
```
