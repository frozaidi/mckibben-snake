#!/usr/bin/env python3

import atexit
import RPi.GPIO as GPIO
import time
import numpy as np
from scipy import signal


class SnakeControl():
    def __init__(self, actuator_dict, inflation_time, on_multiplier,
                 off_multiplier, cycle_amount, time_shift, order):
        atexit.register(self.cleanup)
        GPIO.setmode(GPIO.BOARD)
        self.inflation_time = inflation_time
        self.on_multiplier = on_multiplier
        self.off_multiplier = off_multiplier
        self.cycle_amount = cycle_amount
        self.time_shift = self.inflation_time / time_shift
        self.actuator_dict = actuator_dict
        self.actuator_ord = self.actuation_order(order)
        self.solenoid_setup(self.actuator_ord)
        self.time_start = time.time()
        self.time_limit = (self.inflation_time *
                           (self.on_multiplier + self.off_multiplier) *
                           self.cycle_amount)

    def solenoid_setup(self, actuator_dict):
        for actuator in range(len(actuator_dict)):
            for valve in range(len(actuator_dict[actuator])):
                GPIO.setup(actuator_dict[actuator][valve], GPIO.OUT)
                GPIO.output(actuator_dict[actuator][valve], GPIO.HIGH)

    def cleanup(self):
        for actuator in range(len(self.actuator_ord)):
            GPIO.output(self.actuator_ord[actuator][1], GPIO.LOW)
        time.sleep(self.inflation_time*2)
        GPIO.cleanup()

    def actuation_order(self, order):
        actuator_ord = [self.actuator_dict[int(i)-1] for i in order]
        return actuator_ord

    def control_signal(self, t, act_mul):
        duty_cycle = self.on_multiplier / (self.on_multiplier +
                                           self.off_multiplier)
        control_signal = signal.square(
            2 * np.pi * ((1 / self.inflation_time) * duty_cycle * t -
                         self.time_shift * act_mul), duty_cycle) / 2 + 0.5
        return round(control_signal)

    def generate_actuator_signals(self):
        actuator_sig = []
        for actuator in range(len(self.actuator_ord)):
            current_time = time.time() - self.time_start
            actuator_sig.append(self.control_signal(current_time, actuator))
        return actuator_sig

    def activate_solenoids(self, actuator_sig):
        for act_num in range(len(actuator_sig)):
            if actuator_sig[act_num]:
                GPIO.output(self.actuator_ord[act_num][0], GPIO.LOW)
                GPIO.output(self.actuator_ord[act_num][1], GPIO.HIGH)
            else:
                GPIO.output(self.actuator_ord[act_num][0], GPIO.HIGH)
                GPIO.output(self.actuator_ord[act_num][1], GPIO.LOW)

    def snake_control(self):
        self.time_start = time.time()
        current_time = time.time() - self.time_start
        while current_time < self.time_limit:
            actuator_sig = self.generate_actuator_signals()
            self.activate_solenoids(actuator_sig)
            current_time = time.time() - self.time_start


if __name__ == '__main__':
    actuator1 = (37, 38)
    actuator2 = (35, 36)
    actuator3 = (31, 32)
    actuator4 = (23, 24)
    actuator_dict = (actuator1, actuator2, actuator3, actuator4)
    inflation_time = float(input("Enter inflation time: "))
    cycle_amount = int(input("Enter number of cycles: "))
    on_multiplier = int(input("Enter on multiplier: "))
    off_multiplier = int(input("Enter off multiplier: "))
    time_shift = int(input("Enter time shift (inflation_time/#): "))
    order = input("Enter order of actuation: ")

    sc = SnakeControl(actuator_dict, inflation_time, on_multiplier,
                      off_multiplier, cycle_amount, time_shift, order)
    sc.snake_control()
