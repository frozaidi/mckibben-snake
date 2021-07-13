#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import math


class SolenoidControl:
    def __init__(self, actuator1, actuator2, actuator3, actuator4, dutyCycle,
                 timePeriod, maxTime):
        GPIO.setmode(GPIO.BOARD)
        self.dutyCycle = dutyCycle
        self.timePeriod = timePeriod
        self.maxTime = maxTime
        self.timeOn = self.timePeriod*self.dutyCycle
        self.timeOff = self.timePeriod*(1.0-self.dutyCycle)
        self.numCycles = int(math.ceil(self.maxTime/self.timeOn))

    def solenoidSetup(self, actuatorNum):
        GPIO.setup(actuatorNum[0], GPIO.OUT)
        GPIO.setup(actuatorNum[1], GPIO.OUT)
        GPIO.output(actuatorNum[0], GPIO.HIGH)
        GPIO.output(actuatorNum[1], GPIO.HIGH)

    def solenoidInflate(self, actuatorNum):
        print("Inflating")
        print(actuatorNum[0])
        for i in range(self.numCycles):
            GPIO.output(actuatorNum[0], GPIO.LOW)
            time.sleep(self.timeOn)
            GPIO.output(actuatorNum[0], GPIO.HIGH)
            time.sleep(self.timeOff)

    def solenoidDeflate(self, actuatorNum):
        print("Deflating")
        print(actuatorNum[1])
        # for i in range(self.numCycles):
        #     GPIO.output(actuatorNum[1], GPIO.LOW)
        #     time.sleep(self.timeOn)
        #     GPIO.output(actuatorNum[1], GPIO.HIGH)
        #     time.sleep(self.timeOff)
        GPIO.output(actuatorNum[1], GPIO.LOW)
        time.sleep(1.0)
        GPIO.output(actuatorNum[1], GPIO.HIGH)

    def allInflateDeflate(self, actuator1, actuator2, actuator3, actuator4):
        GPIO.output(actuator1[0], GPIO.LOW)
        GPIO.output(actuator2[0], GPIO.LOW)
        GPIO.output(actuator3[0], GPIO.LOW)
        GPIO.output(actuator4[0], GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(actuator1[0], GPIO.HIGH)
        GPIO.output(actuator2[0], GPIO.HIGH)
        GPIO.output(actuator3[0], GPIO.HIGH)
        GPIO.output(actuator4[0], GPIO.HIGH)
        GPIO.output(actuator1[1], GPIO.LOW)
        GPIO.output(actuator2[1], GPIO.LOW)
        GPIO.output(actuator3[1], GPIO.LOW)
        GPIO.output(actuator4[1], GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(actuator1[0], GPIO.HIGH)
        GPIO.output(actuator2[0], GPIO.HIGH)
        GPIO.output(actuator3[0], GPIO.HIGH)
        GPIO.output(actuator4[0], GPIO.HIGH)

    def concurrentInflation(self, actuator1, actuator2, actuator3, actuator4):
        GPIO.output(actuator1[0], GPIO.LOW)
        GPIO.output(actuator1[1], GPIO.HIGH)
        GPIO.output(actuator3[0], GPIO.HIGH)
        GPIO.output(actuator3[1], GPIO.LOW)
        time.sleep(0.25)
        GPIO.output(actuator2[0], GPIO.LOW)
        GPIO.output(actuator2[1], GPIO.HIGH)
        GPIO.output(actuator4[0], GPIO.HIGH)
        GPIO.output(actuator4[1], GPIO.LOW)
        time.sleep(0.25)
        GPIO.output(actuator3[0], GPIO.LOW)
        GPIO.output(actuator3[1], GPIO.HIGH)
        GPIO.output(actuator1[0], GPIO.HIGH)
        GPIO.output(actuator1[1], GPIO.LOW)
        time.sleep(0.25)
        GPIO.output(actuator4[0], GPIO.LOW)
        GPIO.output(actuator4[1], GPIO.HIGH)
        GPIO.output(actuator2[0], GPIO.HIGH)
        GPIO.output(actuator2[1], GPIO.LOW)
        time.sleep(0.25)

    def opposingInflation(self, actuator1, actuator2, actuator3, actuator4):
        GPIO.output(actuator1[0], GPIO.LOW)
        GPIO.output(actuator3[0], GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(actuator1[0], GPIO.HIGH)
        GPIO.output(actuator3[0], GPIO.HIGH)
        GPIO.output(actuator2[1], GPIO.LOW)
        GPIO.output(actuator4[1], GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(actuator2[0], GPIO.HIGH)
        GPIO.output(actuator4[0], GPIO.HIGH)


if __name__ == '__main__':
    # Initialize the actuator GPIO pins. Convention is first number is to
    # inflate the tube, and second number is to deflate the tube.
    # Wire with relay module and solenoids accordingly.
    actuator1 = (37, 38)
    actuator2 = (35, 36)
    actuator3 = (31, 32)
    actuator4 = (23, 24)
    # Set up PWM control
    dutyCycle = 1.0
    timePeriod = 0.1
    maxTime = 0.5
    solenoidController = SolenoidControl(actuator1, actuator2, actuator3,
                                         actuator4, dutyCycle, timePeriod,
                                         maxTime)

    solenoidController.solenoidSetup(actuator1)
    solenoidController.solenoidSetup(actuator2)
    solenoidController.solenoidSetup(actuator3)
    solenoidController.solenoidSetup(actuator4)

    solenoidController.concurrentInflation(actuator1, actuator2, actuator3,
                                           actuator4)
    solenoidController.concurrentInflation(actuator1, actuator2, actuator3,
                                           actuator4)
    solenoidController.concurrentInflation(actuator1, actuator2, actuator3,
                                           actuator4)
    solenoidController.concurrentInflation(actuator1, actuator2, actuator3,
                                           actuator4)
    # solenoidController.solenoidInflate(actuator2)
    # solenoidController.solenoidDeflate(actuator2)
    #
    # solenoidController.solenoidInflate(actuator3)
    # solenoidController.solenoidDeflate(actuator3)
    #
    # solenoidController.solenoidInflate(actuator4)
    solenoidController.solenoidDeflate(actuator1)
    solenoidController.solenoidDeflate(actuator2)
    solenoidController.solenoidDeflate(actuator3)
    solenoidController.solenoidDeflate(actuator4)

    GPIO.cleanup()
