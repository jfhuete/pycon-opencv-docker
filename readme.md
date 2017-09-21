# Prerrequisites

* Is needed to be installed Docker in your system
* It necesary that your computer has webcam

# If you are developer and you want to improve the app

## Instance the docker image:

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

## Restart the container

To restart the container you have to run this command:

```
docker start -ai pycon-opencv
```

## If you want console

Execute in other terminal:

```
docker exec -it -u root pycon-opencv /bin/bash
```

## Quit

To quit container, you have to push q key in any camera windows

# If you only want a preview

## Instance the docker image:

To instance the jfhuete/pycon-opencv image you have run:

```
docker run -it \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e DISPLAY=unix$DISPLAY \
  --device /dev/video0 \
  --name pycon-opencv jfhuete/pycon-opencv
```

## Restart the container

If you want to restart te execution:

```
docker start -ai pycon-opencv
```

## Quit

To quit container, you have to push q key in any camera windows
