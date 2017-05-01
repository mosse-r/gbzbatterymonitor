#!/bin/bash

cd ~
sudo apt-get install libpng12-dev -y
sudo apt-get install python-gpiozero -y
sudo apt-get install python-pkg-resources python3-pkg-resources -y
sudo apt-get install python-serial -y
sudo git clone https://github.com/HoolyHoo/gbzbatterymonitor.git
sudo chmod 755 /home/pi/gbzbatterymonitor/HHMonitorStart.sh
sudo chmod 755 /home/pi/gbzbatterymonitor/Pngview/pngview
sudo sed -i '/\"exit 0\"/!s/exit 0/\/home\/pi\/gbzbatterymonitor\/HHMonitorStart.sh \&\nexit 0/g' /etc/rc.local
