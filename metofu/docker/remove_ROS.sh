#!/bin/bash

NAME="metofu_brain"

docker stop $NAME && docker rm $NAME && docker rmi $NAME
