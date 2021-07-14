
# mckibben-snake

mckibben-snake is a Python library for working with the McKibben Snake v1.1.

## Installation

Coming soon

## Usage

#### mainKeboardControl.py

This script is used to control each solenoid valve on the McKibben Snake individually. To run:

```
$ python3 mainKeyboardControl.py
```
Wait until a new window appears. It will be a 100px by 100px black window. This is a window created by `pygame`. The keyboard control will properly function as long as the focus is on this black window. The controls are as follows:

- Q/A : Inflate/deflate actuator 1 (respectively)
- W/S : Inflate/deflate actuator 2 (respectively)
- E/D : Inflate/deflate actuator 3 (respectively)
- R/F : Inflate/deflate actuator 4 (respectively)
- P : End the script. This will automatically close the `pygame` window and end the script.

#### concurrentControl.py

This script will cyclically inflate the actuators. Currently it does so 4 times before attempting to fully deflate. To run:

```
$ python3 concurrentControl.py
```

#### deflateSnake.py

This script will fully deflate the actuators. Run this at the end of experiments to ensure that the actuators are at atmospheric pressure. To run:

```
$ python3 deflateSnake.py
```

#### solenoidControl.py

This script is currently undergoing an overhaul.

## Author
[Farhan Rozaidi](https://github.com/frozaidi)
