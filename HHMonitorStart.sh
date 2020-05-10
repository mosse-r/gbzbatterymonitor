#!/usr/bin/env bash

python /home/pi/gbzbatterymonitor/GBZCombo.py &
sleep 20
python /home/pi/gbzbatterymonitor/HHBatteryMonitor.py &