#!/bin/bash

cd ~

# Install dependancies
sudo apt-get install libpng-dev python-gpiozero python-pkg-resources python3-pkg-resources python-serial -y

# Install gbzbatterymonitor
sudo git clone https://github.com/mosse-r/gbzbatterymonitor.git
sudo chmod 755 /home/pi/gbzbatterymonitor/HHMonitorStart.sh

# Install Pngview
sudo git clone https://github.com/AndrewFromMelbourne/raspidmx.git ~/gbzbatterymonitor/raspidmx
cd /home/pi/gbzbatterymonitor/raspidmx
sudo make -j
sudo mkdir /home/pi/gbzbatterymonitor/bin
sudo cp /home/pi/gbzbatterymonitor/raspidmx/pngview/pngview /home/pi/gbzbatterymonitor/bin/pngview
sudo ln -s /home/pi/gbzbatterymonitor/bin/pngview /home/pi/gbzbatterymonitor/bin/pngview-transient
sudo ln -s /home/pi/gbzbatterymonitor/bin/pngview /home/pi/gbzbatterymonitor/bin/pngview-bluetooth
sudo ln -s /home/pi/gbzbatterymonitor/bin/pngview /home/pi/gbzbatterymonitor/bin/pngview-wifi
sudo rm -rf /home/pi/gbzbatterymonitor/raspidmx

# Startup
if grep -Fxq "/home/pi/gbzbatterymonitor/HHMonitorStart.sh &"  /etc/rc.local
then
	echo "Already Installed"
else
	sudo sed -i '/\"exit 0\"/!s/exit 0/\/home\/pi\/gbzbatterymonitor\/HHMonitorStart.sh \&\nexit 0/g' /etc/rc.local
fi
