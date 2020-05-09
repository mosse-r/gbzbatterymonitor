#!/usr/bin/env python2.7

"""
Date:  10/08/17
Author:  HoolyHoo
Version:  2.1
Name:  Combo Shortcut Script - Utility for the MintyPi project.
Description:  Monitors USB gamepad to adjust volume with icons, battery monitor, wifi and bluetooth toggle, and performs safe shutdown.
Usage:  Mode + Y = Toggle Wifi with Icon
        Mode + B = Toggle BT with Icon
        Mode + A = Toggle Battery
        Mode + X = Initiate Safe Shutdown
        Mode + Dpad Right = Volume Up with Icon
        Mode + Dpad Left  = Volume Down with Icon
        Mode + Dpad Up    = Dimming Up
        Mode + Dpad Down  = Dimming Down
        Mode + Right Shoulder = Display Cheat
"""

from inputs import get_gamepad
from Button import Button
from subprocess import check_call
import os
import time

functionBtn = Button('BTN_WEST')
volumeUpBtn = Button('BTN_SELECT')
volumeDownBtn = Button('BTN_START')
shutdownBtn = Button('BTN_NORTH')
monitorBtn = Button('BTN_EAST')
wifiBtn = Button('BTN_C')
bluetoothBtn = Button('BTN_SOUTH')
cheatBtn = Button('BTN_TL2')
volume = 60
wifiStatus = 1
bluetoothStatus = 1
toggleFile = "/home/pi/gbzbatterymonitor/Toggle.txt"
batteryMonitorPath = "/home/pi/gbzbatterymonitor/HHBatteryMonitor.py"
pngviewBinary = "/home/pi/gbzbatterymonitor/bin/pngview-transient"
iconPath = "/home/pi/gbzbatterymonitor/icons"
state = 1


def volumeDown():
    global volume
    volume = max(0, volume - 10)
    os.system("amixer sset -q 'PCM' " + str(volume) + "%")
    showVolumeIcon()


def volumeUp():
    global volume
    volume = min(100, volume + 10)
    os.system("amixer sset -q 'PCM' " + str(volume) + "%")
    showVolumeIcon()


def wifiToggle():
    global wifiStatus
    killPngview()
    if wifiStatus == 0:
        os.system("sudo rfkill block wifi")
        os.system(pngviewBinary + " -b 0 -l 999999 -t 2000 " + iconPath + "/wifiOff.png &")
        wifiStatus = 1
    else:
        os.system("sudo rfkill unblock wifi")
        os.system(pngviewBinary + " -b 0 -l 999999 -t 2000 " + iconPath + "/wifiOn.png &")
        wifiStatus = 0


def bluetoothToggle():
    global bluetoothStatus
    delay = 2000
    killPngview()
    if bluetoothStatus == 0:
        os.system("sudo rfkill block bluetooth")
        os.system("{pngviewBinary} -b 0 -l 999999 -t {delay} {iconPath}/bluetoothOff.png &".format(
            pngviewBinary=pngviewBinary, delay=delay, iconPath=iconPath)
        )
        bluetoothStatus = 1
    else:
        os.system("sudo rfkill unblock bluetooth")
        os.system("{pngviewBinary} -b 0 -l 999999 -t {delay} {iconPath}/bluetoothOn.png &".format(
            pngviewBinary=pngviewBinary, delay=delay, iconPath=iconPath)
        )
        bluetoothStatus = 0


def shutdown():
    for i in range(0, 3):
        os.system(pngviewBinary + " -b 0 -l 999999 " + iconPath + "/shutdown.png &")
        time.sleep(1)
        killPngview()
        time.sleep(.5)
    check_call(['sudo', 'poweroff'])


def toggleState():
    global state
    if state == 1:
        os.system('sudo pkill -f "python {battery_monitor_script}"'.format(battery_monitor_script=batteryMonitorPath))
        state = 0
        with open(toggleFile, 'w') as f:
            f.write('0')
        time.sleep(2)
        os.system("python {battery_monitor_script} &".format(battery_monitor_script=batteryMonitorPath))
        time.sleep(1)
    else:
        os.system('sudo pkill -f "python {battery_monitor_script}"'.format(battery_monitor_script=batteryMonitorPath))
        state = 1
        with open(toggleFile, 'w') as f:
            f.write('1')
        time.sleep(2)
        os.system("python {battery_monitor_script} &".format(battery_monitor_script=batteryMonitorPath))
        time.sleep(1)


def showVolumeIcon():
    global volume
    killPngview()
    os.system(pngviewBinary + " -b 0 -l 999999 -t 1000 " + iconPath + "/Volume" + str(volume) + ".png &")

    if volumeUpBtn.is_pressed():
        volume = min(100, volume + 10)
    elif volumeDownBtn.is_pressed():
        volume = max(0, volume - 10)

    os.system("amixer sset -q 'PCM' " + str(volume) + "%")


def showCheat():
    os.system(pngviewBinary + " -b 0 -l 999999 -t 5000 " + iconPath + "/cheat.png &")


def killPngview():
    os.system("sudo killall -q -15 pngview-transient")


def initSetup():
    global state
    # Initial File Setup
    try:
        with open(toggleFile, 'r') as f:
            output = f.read()
    except IOError:
        with open(toggleFile, 'w') as f:
            f.write('1')
        output = '1'
    state = int(output)

    os.system("amixer sset -q 'PCM' " + str(volume) + "%")
    os.system("sudo rfkill block wifi")
    os.system("sudo rfkill block bluetooth")


def check_function():
    if functionBtn.is_pressed():
        if volumeUpBtn.is_pressed():
            volumeUp()
        elif volumeDownBtn.is_pressed():
            volumeDown()
        elif shutdownBtn.is_pressed():
            shutdown()
        elif monitorBtn.is_pressed():
            toggleState()
        elif wifiBtn.is_pressed():
            wifiToggle()
        elif bluetoothBtn.is_pressed():
            bluetoothToggle()
        elif cheatBtn.is_pressed():
            showCheat()


def main():

    initSetup()

    while True:
        events = get_gamepad()
        for event in events:
            if event.ev_type == 'Key':
                Button.state[event.code] = bool(event.state)
                check_function()


main()
