#!/usr/bin/env python3

import RPi.GPIO as GPIO
import keyboard as kb

class endControl(Exception): pass

def solenoidSetup(actuatorArray):
    for actuator in range(4):
        for valve in range(2):
            GPIO.setup(actuatorArray[actuator][valve], GPIO.OUT)
            GPIO.output(actuatorArray[actuator][valve], GPIO.HIGH)

def main():
    if kb.is_pressed('q'):
        print("q")
        GPIO.output(actuatorArray[0][0], GPIO.LOW)
    elif kb.is_pressed('w'):
        print("w")
        GPIO.output(actuatorArray[1][0], GPIO.LOW)
    elif kb.is_pressed('e'):
        print("e")
        GPIO.output(actuatorArray[2][0], GPIO.LOW)
    elif kb.is_pressed('r'):
        print("r")
        GPIO.output(actuatorArray[3][0], GPIO.LOW)
    elif kb.is_pressed('a'):
        print("a")
        GPIO.output(actuatorArray[0][1], GPIO.LOW)
    elif kb.is_pressed('s'):
        print("s")
        GPIO.output(actuatorArray[1][1], GPIO.LOW)
    elif kb.is_pressed('d'):
        print("d")
        GPIO.output(actuatorArray[2][1], GPIO.LOW)
    elif kb.is_pressed('f'):
        print("f")
        GPIO.output(actuatorArray[3][1], GPIO.LOW)
    elif kb.is_pressed('p'):
        print("p")
        raise endControl
    else:
        # print("Nothing")
        for actuator in range(4):
            for valve in range(2):
                GPIO.output(actuatorArray[actuator][valve], GPIO.HIGH)

if __name__ == '__main__':

    GPIO.setmode(GPIO.BOARD)

    actuator1 = (37, 38)
    actuator2 = (35, 36)
    actuator3 = (31, 32)
    actuator4 = (23, 24)
    actuatorArray =(actuator1,actuator2,actuator3,actuator4)
    solenoidSetup(actuatorArray)
    try:
        while True:
            main()
    except endControl:
        pass
    GPIO.cleaup()
