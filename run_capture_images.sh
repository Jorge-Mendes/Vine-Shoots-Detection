#!/bin/sh

cd /home/pi/Desktop/Vine-Shoots-Detection
python capture_images.py

# Add the following line to crontab:
# @reboot sh /home/pi/Desktop/Vine-Shoots-Detection/run_capture_images.sh