#!/bin/bash

# Run as ROOT!

echo "root:orange123" | chpasswd
echo "ubuntu:orange123" | chpasswd

usermod -aG dialout ubuntu

apt update && 
apt install python3-pip -y &&
