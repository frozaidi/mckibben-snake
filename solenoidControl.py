#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time


class SolenoidControl:
    def __init__(self, actuatorArray, inflationTime=0.5, numCycles=4):
        GPIO.setmode(GPIO.BOARD)
        self.inflationTime = inflationTime
        self.numCycles = numCycles
        self.solenoidSetup(actuatorArray)

    def solenoidSetup(self, actuatorArray):
        for actuator in range(len(actuatorArray)):
            for valve in range(len(actuatorArray[actuator])):
                GPIO.setup(actuatorArray[actuator][valve], GPIO.OUT)
                GPIO.output(actuatorArray[actuator][valve], GPIO.HIGH)

    def closeValves(self, actuatorArray):
        for actuator in range(len(actuatorArray)):
            for valve in range(len(actuatorArray[actuator])):
                GPIO.output(actuatorArray[actuator][valve], GPIO.HIGH)

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
        GPIO.output(actuatorNum[1], GPIO.LOW)
        time.sleep(1.0)
        GPIO.output(actuatorNum[1], GPIO.HIGH)

    def deflateSnake(self, actuatorArray, scale=1.0):
        print("Deflating snake")
        for actuator in range(len(actuatorArray)):
            GPIO.output(actuatorArray[actuator][1], GPIO.LOW)
        time.sleep(self.inflationTime*scale)
        for actuator in range(len(actuatorArray)):
            GPIO.output(actuatorArray[actuator][1], GPIO.HIGH)

    def inflateSnake(self, actuatorArray, scale=1.0):
        print("Inflating snake")
        for actuator in range(len(actuatorArray)):
            GPIO.output(actuatorArray[actuator][0], GPIO.LOW)
        time.sleep(self.inflationTime*scale)
        for actuator in range(len(actuatorArray)):
            GPIO.output(actuatorArray[actuator][0], GPIO.HIGH)

    def allInflateDeflate(self, actuatorArray):
        for cycle in range(self.numCycles):
            self.inflateSnake(actuatorArray)
            self.deflateSnake(actuatorArray)

    def concurrentInflation(self, actuatorArray):
        for cycle in range(self.numCycles):
            GPIO.output(actuatorArray[0][0], GPIO.LOW)
            GPIO.output(actuatorArray[0][1], GPIO.HIGH)
            GPIO.output(actuatorArray[2][0], GPIO.HIGH)
            GPIO.output(actuatorArray[2][1], GPIO.LOW)
            time.sleep(self.inflationTime/2.0)
            GPIO.output(actuatorArray[1][0], GPIO.LOW)
            GPIO.output(actuatorArray[1][1], GPIO.HIGH)
            GPIO.output(actuatorArray[3][0], GPIO.HIGH)
            GPIO.output(actuatorArray[3][1], GPIO.LOW)
            time.sleep(self.inflationTime/2.0)
            GPIO.output(actuatorArray[2][0], GPIO.LOW)
            GPIO.output(actuatorArray[2][1], GPIO.HIGH)
            GPIO.output(actuatorArray[0][0], GPIO.HIGH)
            GPIO.output(actuatorArray[0][1], GPIO.LOW)
            time.sleep(self.inflationTime/2.0)
            GPIO.output(actuatorArray[3][0], GPIO.LOW)
            GPIO.output(actuatorArray[3][1], GPIO.HIGH)
            GPIO.output(actuatorArray[1][0], GPIO.HIGH)
            GPIO.output(actuatorArray[1][1], GPIO.LOW)
            time.sleep(self.inflationTime/2.0)

    def opposingInflation(self, actuatorArray):
        for cycle in range(self.numCycles):
            GPIO.output(actuatorArray[0][0], GPIO.LOW)
            GPIO.output(actuatorArray[0][1], GPIO.HIGH)
            GPIO.output(actuatorArray[2][0], GPIO.LOW)
            GPIO.output(actuatorArray[2][1], GPIO.HIGH)
            GPIO.output(actuatorArray[1][0], GPIO.HIGH)
            GPIO.output(actuatorArray[1][1], GPIO.LOW)
            GPIO.output(actuatorArray[3][0], GPIO.HIGH)
            GPIO.output(actuatorArray[3][1], GPIO.LOW)
            time.sleep(self.inflationTime)
            GPIO.output(actuatorArray[0][0], GPIO.HIGH)
            GPIO.output(actuatorArray[0][1], GPIO.LOW)
            GPIO.output(actuatorArray[2][0], GPIO.HIGH)
            GPIO.output(actuatorArray[2][1], GPIO.LOW)
            GPIO.output(actuatorArray[1][0], GPIO.LOW)
            GPIO.output(actuatorArray[1][1], GPIO.HIGH)
            GPIO.output(actuatorArray[3][0], GPIO.LOW)
            GPIO.output(actuatorArray[3][1], GPIO.HIGH)
            time.sleep(self.inflationTime)

    def sequentialInflation(self, actuatorArray):
        for cycle in range(self.numCycles):
            for actuator in range(len(actuatorArray)):
                GPIO.output(actuatorArray[actuator][0], GPIO.LOW)
                GPIO.output(actuatorArray[actuator][1], GPIO.HIGH)
                for othActuator in range(len(actuatorArray)):
                    if othActuator != actuator:
                        GPIO.output(actuatorArray[othActuator][0], GPIO.HIGH)
                        GPIO.output(actuatorArray[othActuator][1], GPIO.LOW)
                time.sleep(self.inflationTime)

    def singularInflation(self, actuatorArray):
        for cycle in range(self.numCycles):
            for actuator in range(len(actuatorArray)):
                GPIO.output(actuatorArray[actuator][0], GPIO.LOW)
                GPIO.output(actuatorArray[actuator][1], GPIO.HIGH)
                for othActuator in range(len(actuatorArray)):
                    if othActuator != actuator:
                        GPIO.output(actuatorArray[othActuator][0], GPIO.HIGH)
                        GPIO.output(actuatorArray[othActuator][1], GPIO.LOW)
                time.sleep(self.inflationTime)
                GPIO.output(actuatorArray[actuator][0], GPIO.HIGH)
                GPIO.output(actuatorArray[actuator][1], GPIO.LOW)
                time.sleep(self.inflationTime)

    def solenoidCleanup(self, actuatorArray):
        self.closeValves(actuatorArray)
        self.deflateSnake(actuatorArray, 2)
        GPIO.cleanup()
