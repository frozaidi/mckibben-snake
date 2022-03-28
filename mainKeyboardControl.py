#!/usr/bin/env python3

import RPi.GPIO as GPIO
import keyModule as km

km.init()


class endControl(Exception):
    pass


def solenoidSetup(actuatorArray):
    for actuator in range(4):
        for valve in range(2):
            GPIO.setup(actuatorArray[actuator][valve], GPIO.OUT)
            GPIO.output(actuatorArray[actuator][valve], GPIO.HIGH)


def main():
    if km.getKey('q'):
        GPIO.output(actuatorArray[0][0], GPIO.LOW)
    elif km.getKey('w'):
        GPIO.output(actuatorArray[1][0], GPIO.LOW)
    elif km.getKey('e'):
        GPIO.output(actuatorArray[2][0], GPIO.LOW)
    elif km.getKey('r'):
        GPIO.output(actuatorArray[3][0], GPIO.LOW)
    elif km.getKey('a'):
        GPIO.output(actuatorArray[0][1], GPIO.LOW)
    elif km.getKey('s'):
        GPIO.output(actuatorArray[1][1], GPIO.LOW)
    elif km.getKey('d'):
        GPIO.output(actuatorArray[2][1], GPIO.LOW)
    elif km.getKey('f'):
        GPIO.output(actuatorArray[3][1], GPIO.LOW)
    elif km.getKey('p'):
        raise endControl
    else:
        for actuator in range(4):
            for valve in range(2):
                GPIO.output(actuatorArray[actuator][valve], GPIO.HIGH)


if __name__ == '__main__':

    GPIO.setmode(GPIO.BOARD)

    actuator1 = (37, 38)
    actuator2 = (35, 36)
    actuator3 = (31, 32)
    actuator4 = (23, 24)
    actuatorArray = (actuator1, actuator2, actuator3, actuator4)
    solenoidSetup(actuatorArray)
    try:
        while True:
            main()
    except endControl:
        pass
    GPIO.cleanup()
