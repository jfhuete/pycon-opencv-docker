# Prerrequisites

* Is needed to be installed Docker in your system
* It necessary that your computer has webcam

## Build Dockerfile

To build the dockerfile you have to run:

```
docker build -t jfhuete/pycon-opencv .
```

# Instance the docker image:

## If you are developer and you want to improve the app

To instance the jfhuete/pycon-opencv image you have run:

```
docker run -it \
  -v "$(pwd)"/app:/home/opencv/app \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e DISPLAY=unix$DISPLAY \
  --device /dev/video0 \
  --name pycon-opencv jfhuete/pycon-opencv
```

This command create a docker volume and bind it with the local workspace.

When you restart the container you can view the result of your changes.

### Run bash in container

Execute in other terminal while the docker is running:

```
docker exec -it -u root pycon-opencv /bin/bash
```

## If you only want a preview

To instance the jfhuete/pycon-opencv image you have run:

```
docker run -it \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e DISPLAY=unix$DISPLAY \
  --device /dev/video0 \
  --name pycon-opencv jfhuete/pycon-opencv
```

## Restart the container

To restart the container you have to run this command:

```
docker start -ai pycon-opencv
```

## Quit

To quit container, you have to push q key in any camera windows, or ctrl+c in
terminal
