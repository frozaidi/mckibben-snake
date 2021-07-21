#!/usr/bin/env python3

from solenoidControl import SolenoidControl
import inquirer

if __name__ == '__main__':
    actuator1 = (37, 38)
    actuator2 = (35, 36)
    actuator3 = (31, 32)
    actuator4 = (23, 24)
    actuatorArray = (actuator1, actuator2, actuator3, actuator4)
    inflationTime = float(input("Enter inflation time: "))
    numCycles = int(input("Enter number of cycles: "))

    sc = SolenoidControl(actuatorArray, inflationTime, numCycles)

    question = [
        inquirer.List('control',
                      message="Select control scheme:",
                      choices=['Concurrent', 'Sequential', 'Singular',
                               'Opposing', 'All', 'Reversed Concurrent'],
                      ),
    ]

    controlScheme = inquirer.prompt(question)

    if controlScheme['control'] == 'Concurrent':
        sc.concurrentInflation(actuatorArray)
    elif controlScheme['control'] == 'Sequential':
        sc.sequentialInflation(actuatorArray)
    elif controlScheme['control'] == 'Singular':
        sc.singularInflation(actuatorArray)
    elif controlScheme['control'] == 'Opposing':
        sc.opposingInflation(actuatorArray)
    elif controlScheme['control'] == 'All':
        sc.allInflateDeflate(actuatorArray)
    elif controlScheme['control'] == 'Reversed Concurrent':
        sc.revConcurrentInflation(actuatorArray)
    else:
        print('Undefined control scheme')
        pass

    sc.solenoidCleanup(actuatorArray)
