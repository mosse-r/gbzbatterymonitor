# HoolyHoo-GBZBattery-Monitor

This battery monitoring solution is for Helder's AIO board. The script and hex should display on screen battery monitoring with a low battery warning video and critical battery level video along with an automated shutdown that would cancel if you plug in the zero to power. Also added an option to install a extra button that will be monitored and when pressed and held, will initialize a graceful shutdown at any time so you don't have to go through emulation station menu to shutdown. A good placement is in the original GB charging hole. That button is optional however and not needed if you don't want it.  I tested this with the Adafruit Powerboost 1000c but should work also with the Banggood power supply.

# Installation

### Hardware Needed

One 10K resistor and DPDT switch.  The original GB switch will work also with the Powerboost 1000C but not with the Banggood power supply.  Also one momemtary tact switch which is optional.
### Wiring Schematic PowerBoost 1000C Edition
![](https://github.com/HoolyHoo/gbzbatterymonitor/blob/master/Wiring/Schematic.png)

### Wiring Schematic Banggood Power Supply Edition
![](https://github.com/HoolyHoo/gbzbatterymonitor/blob/master/Wiring/SchematicBG.png)
### Hex File Install

Reprogram Helder's board with new hex file.

Grab the hex from the hex directory:
https://github.com/HoolyHoo/gbzbatterymonitor/tree/master/Hex

Go to Helder's link for help on programming.
http://www.sudomod.com/forum/viewtopic.php?f=25&t=1228

### Software Install

You can do this part in one of two ways, Automated or Manual.  You decide.

#### Automated Software Install

Go to raspberry command prompt or SSH.
Make sure you are in the home directory by typing ```cd ~ ``` and then type:
```
wget https://raw.githubusercontent.com/HoolyHoo/gbzbatterymonitor/master/Install.sh
```
Then type:
```
sudo chmod 755 Install.sh
```
And finally type:
```
./Install.sh
```
Finally reboot to have it all start on boot with:
```
sudo reboot
```

#### Manual Software Install
And the longer way if you want to do it manually step by step.
Go to raspberry command prompt or SSH.  Make sure you are in the home directory and type:
```
cd ~
```
Type:
```
sudo apt-get install libpng12-dev
```
Type:
```
sudo apt-get install python-gpiozero
```
Type:
```
sudo apt-get install python-serial
```
Clone and install my github and scripts:
```
sudo git clone https://github.com/HoolyHoo/gbzbatterymonitor.git
```
Change file permission:
```
sudo chmod 755 /home/pi/gbzbatterymonitor/HHMonitorStart.sh
```
Change file permission:
```
sudo chmod 755 /home/pi/gbzbatterymonitor/Pngview/pngview
```
Install in rc.local to start scripts on startup:
```
sudo nano /etc/rc.local
```
Add this before last line that reads exit 0:
```
/home/pi/gbzbatterymonitor/HHMonitorStart.sh &
```
Reboot:
```
sudo reboot
```

### Optional

Voltage from the battery is compared to the output voltage from the Powerboost or Banggood power supply.  This voltage may vary on your setup.  The default ouput measurement used is 5.1V.  If you want your battery reading to be more accurate measure with a reliable multimeter between ground and 5V on Helder's board.  Use that reading and change the variable VCC in the python script named "HHBatteryMonitor.py".

### Credits

www.sudomod.com

https://github.com/AndrewFromMelbourne/raspidmx/

https://github.com/joachimvenaas/gbzbatterymonitor
