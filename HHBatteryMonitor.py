#!/usr/bin/python
import time
import os
import signal
import serial
from subprocess import check_output


# Config
warning = 0
status = 0
port = 0
debug = 0
iconState = ""
toggleFile = "/home/pi/gbzbatterymonitor/Toggle.txt"
PNGVIEWPATH = "/home/pi/gbzbatterymonitor/raspidmx/pngview"
ICONPATH = "/home/pi/gbzbatterymonitor/icons"
CLIPS = 1
REFRESH_RATE = 1
VCC = 5.1
VOLT100 = 4.2
VOLT75 = 3.99
VOLT50 = 3.79
VOLT25 = 3.59
VOLT0 = 3.38


def changeicon(percent):
    global iconState
    if iconState != percent:
        iconState = percent
        i = 0
        killid = 0
        os.system(PNGVIEWPATH + "/pngview -b 0 -l 3000" + percent + " -x 650 -y 0 " + ICONPATH + "/battery" + percent + ".png &")
        out = check_output("ps aux | grep pngview | awk '{ print $2 }'", shell=True)
        nums = out.split('\n')
        for num in nums:
            i += 1
            if i == 1:
                killid = num
                os.system("sudo kill " + killid)


def endProcess(signalnum=None, handler=None):
    os.system("sudo killall pngview")
    exit(0)


def readSerial():
    ser.write('1')
    time.sleep(.3)
    x = (ser.readline())
    return x


def convertVoltage():
    global VCC
    sensorValue = readSerial()
    voltage = float(sensorValue) * (VCC / 1023.0)
    return voltage


# Initial Setup

signal.signal(signal.SIGTERM, endProcess)
signal.signal(signal.SIGINT, endProcess)


# Check Serial Port Availability

while port == 0:
    for x in range(0, 3):
        try:
            ser = serial.Serial('/dev/ttyACM' + str(x), 115200)
        except serial.SerialException:
            if debug == 1:
                print('Serial Port ACM' + str(x) + ' Not Found')
            time.sleep(1)
        else:
            port = 1
            break

# Begin Battery Monitoring

os.system(PNGVIEWPATH + "/pngview -b 0 -l 299999 -x 650 -y 0 " + ICONPATH + "/blank.png &")

try:
    with open(toggleFile, 'r') as f:
        output = f.read()
except IOError:
    with open(toggleFile, 'w') as f:
        f.write('1')
    output = '1'
state = int(output)

while True:
    try:
        ret1 = convertVoltage()
        time.sleep(.2)
        ret2 = convertVoltage()
        time.sleep(.2)
        ret3 = convertVoltage()
        ret = (ret1 + ret2 + ret3) / 3
        if debug == 1:
            print(ret)
        if ret < VOLT0:
            if status != 0:
                changeicon("0")
                if CLIPS == 1:
                    os.system("/usr/bin/omxplayer --no-osd --layer 999999  " + ICONPATH + "/lowbattshutdown.mp4 --alpha 160;")
                    voltcheck = convertVoltage()
                    if voltcheck <= VOLT0:
                        os.system("sudo shutdown -h now")
                    else:
                        warning = 0
            status = 0
        elif ret < VOLT25:
            if status != 25:
                changeicon("25")
                if warning != 1:
                    if CLIPS == 1:
                        os.system("/usr/bin/omxplayer --no-osd --layer 999999  " + ICONPATH + "/lowbattalert.mp4 --alpha 160")
                    warning = 1
            status = 25
        elif ret < VOLT50:
            if status != 50 and state == 1:
                changeicon("50")
            status = 50
        elif ret < VOLT75:
            if status != 75 and state == 1:
                changeicon("75")
            status = 75
        else:
            if status != 100 and state == 1:
                changeicon("100")
            status = 100

        time.sleep(REFRESH_RATE)
    except serial.SerialException:
        port = 0
        while port == 0:
            for x in range(0, 3):
                try:
                    ser = serial.Serial('/dev/ttyACM' + str(x), 115200)
                    port = 1
                except serial.SerialException:
                    if debug == 1:
                        print('Serial Port ACM' + str(x) + ' Not Found')
                    time.sleep(1)
                else:
                    port = 1
                    break
