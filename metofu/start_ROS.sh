#!/bin/bash

docker start metofu_brain &&
	docker exec -it -u ubuntu metofu_brain /bin/bash -c "
	source /opt/ros/kilted/setup.bash && \
	cd /home/ubuntu/Metofu/chatbot && \
	python3 subscriber.py & \

	source /opt/ros/kilted/setup.bash && \
	cd /home/ubuntu/Metofu/chatbot && \
	python3 publisher.py & \
	wait
	"
