#!/bin/bash

ROS_IMAGE_NAME="metofu_brain"
CONTAINER_NAME="metofu_brain"

docker run -it \
	--name "$CONTAINER_NAME" \
	--device /dev/ttyACM0:/dev/ttyACM0 \
	--network host \
	-e DISPLAY="$DISPLAY" \
	-v /home/bmo/Metofu:/home/ubuntu/Metofu \
	"$ROS_IMAGE_NAME" \
	/bin/bash
