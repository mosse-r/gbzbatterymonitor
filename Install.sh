#!/bin/bash

cd ~
sudo apt-get install libpng12-dev -y
sudo apt-get install python-gpiozero -y
sudo apt-get install python-serial -y
sudo git clone https://github.com/AndrewFromMelbourne/raspidmx.git
cd raspidmx
sudo make
cd ~
sudo git clone https://github.com/HoolyHoo/gbzbatterymonitor.git
cd gbzbatterymonitor
sudo chmod 755 HHMonitorStart.sh
sudo sed -i '/\"exit 0\"/!s/exit 0/\/home\/pi\/gbzbatterymonitor\/HHMonitorStart.sh \&\nexit 0/g' /etc/rc.local
