#!/usr/bin/env python3

import RPi.GPIO as GPIO
import keyModule as km
import atexit
import time


class KeyboardControl():
    def __init__(self, actuator_dict):
        atexit.register(self.cleanup)
        km.init()
        GPIO.setmode(GPIO.BOARD)
        self.actuator_dict = actuator_dict
        self.key_dict = {
            'q': actuator_dict[0][0],
            'w': actuator_dict[1][0],
            'e': actuator_dict[2][0],
            'r': actuator_dict[3][0],
            'a': actuator_dict[0][1],
            's': actuator_dict[1][1],
            'd': actuator_dict[2][1],
            'f': actuator_dict[3][1]
        }
        self.solenoid_setup(actuator_dict)

    def solenoid_setup(self, actuator_dict):
        for actuator in range(len(actuator_dict)):
            for valve in range(len(actuator_dict[actuator])):
                GPIO.setup(actuator_dict[actuator][valve], GPIO.OUT)
                GPIO.output(actuator_dict[actuator][valve], GPIO.HIGH)

    def cleanup(self):
        GPIO.cleanup()

    def generate_keys_pressed(self):
        key_pressed = []
        key_unpressed = []
        for key in self.key_dict.keys():
            if km.getKey(key):
                key_pressed.append(key)
            else:
                key_unpressed.append(key)
        return key_pressed, key_unpressed

    def activate_solenoids(self, key_pressed, key_unpressed):
        for key in key_pressed:
            GPIO.output(self.key_dict[key], GPIO.LOW)
        for key in key_unpressed:
            GPIO.output(self.key_dict[key], GPIO.HIGH)

    def key_control(self):
        key_pressed, key_unpressed = self.generate_keys_pressed()
        self.activate_solenoids(key_pressed, key_unpressed)


if __name__ == '__main__':

    GPIO.setmode(GPIO.BOARD)

    actuator1 = (37, 38)
    actuator2 = (35, 36)
    actuator3 = (31, 32)
    actuator4 = (23, 24)
    actuator_dict = (actuator1, actuator2, actuator3, actuator4)

    kc = KeyboardControl(actuator_dict)
    time_limit = 100.0
    time_start = time.time()
    current_time = time.time()-time_start
    while current_time < time_limit:
        kc.key_control()
        current_time = time.time()-time_start
