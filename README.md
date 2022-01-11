# Simple-Quadruped-Robot
Code and CAD models for a Simple Quadruped Robot.

## Installing Circuitpython and Mu

The code is written on CircuitPython, which is a stripped down version of Python, made for low power microcontroller boards.
The steps to install CircuitPython on RP2040 boards, such as Raspberry Pi Pico can be found [here](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython).
The editor I used is called Mu, it is a pretty lightweight, simple enough editor thats works with microcontrollers. It can be installed from [here](https://codewith.mu/).

## Transferring Files to Pi Pico
Plug in the Pi Pico after installing Circuitpython, you will get access to a drive on the Pi Pico. Open the lib folder and paste these files and folders:

1. adafruit_bus_device
2. adafruit_register
3. adafruit_pca9685.mpy
4. CustomLib.py

The first three are from the libraries of CircuitPython. The ones on this repostiory works fine but your free to download the latest version of the CircuitPython and the updated libraries from their [official site](https://circuitpython.org/).

Now paste the code.py file into the root of the drive. Do not rename the files.

## CAD Models

I have also uploaded the CAD files for the robot, the same is also uploaded in the [hackster site] for the project.
