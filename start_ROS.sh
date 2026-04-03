#!/bin/bash

docker start metofu_brain && docker exec -it -u ubuntu metofu_brain /bin/bash -c "source /opt/ros/kilted/setup.bash && /home/ubuntu/Metofu/start_controller.sh"
