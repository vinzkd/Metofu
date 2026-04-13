#!/bin/bash

ros2 run teleop_twist_joy teleop_node --ros-args --params-file ~/ros/teleop_node.yaml &
ros2 run joy joy_node --ros-args -p deadzone:=0.15 -p coalesce_interval_ms:=1000 &
wait
