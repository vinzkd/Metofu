#!/bin/bash

# This script is designed to fix the LD_PRELOAD error when launching terminals
# or containers from Steam's Big Picture/Game Mode.

# 1. Unset environment variables injected by Steam that cause conflicts.
# This forces the session to use standard system libraries.
unset LD_PRELOAD
unset STEAM_RUNTIME

# 2. Launch the Distrobox container
# Note: Konsole (or your preferred terminal) will open, and then immediately
# execute the 'distrobox enter' command inside that Konsole window.
konsole -e "distrobox enter steamdeck_ros_client"
