#!/bin/bash

DATE=$(date +"%Y-%m-%dT%H:%M:%S")

fswebcam -r 1280x720 /home/pi/git/github/motion_triggered_cam/docs/images/$DATE.jpg