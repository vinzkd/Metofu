#!/bin/bash

echo "orange123" | sudo chown ubuntu:ubuntu /dev/ttyACM0

python3 /home/ubuntu/Metofu/metofu_controller.py
