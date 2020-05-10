#!/usr/bin/env python2.7

from inputs import get_gamepad

def main():

    while True:
        events = get_gamepad()
        for event in events:
            if event.ev_type == 'Key' and event.state == 1:
		print(event.code)


main()
