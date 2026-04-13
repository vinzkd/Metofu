#!/bin/bash

ffmpeg -f v4l2 -framerate 30 -s 640x480 -i /dev/video0 \
  -c:v libx264 -preset ultrafast -tune zerolatency -b:v 800k \
  -f mpegts udp://192.168.1.187:2000
