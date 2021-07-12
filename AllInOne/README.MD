# Build docker

## Generic command
docker build -t allinone-pollenisator .

## Rebuild all tools (update them)
docker build --no-cache -t allinone-pollenisator .

# Run worker (if it's for local to local replace -p paramaters with --net=host)

```docker run -p 127.0.0.1:2222:22 -p 127.0.0.1:27017:27017 -d allinone-pollenisator```

or enter docker

```docker run -p 127.0.0.1:2222:22 -p 127.0.0.1:27017:27017 -ti allinone-pollenisator /bin/bash```

and run ./start.sh

# Stop docker

```
docker ps
docker stop Xxxxxxx
```
