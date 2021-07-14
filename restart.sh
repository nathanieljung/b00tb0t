#!/bin/sh
cd ~/b00tb0t
pkill -f start.py
nohup python3 start.py &
