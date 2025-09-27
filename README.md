# PiDisposableCamera
I shoved a raspberry pi and a camera module into the shell of a disposable camera

HardWare:
- Raspberry Pi Zero 2W
- Arducam 12mp Camera Module 3
- PiSugar S battery module

Software:
- Pi OS Lite 32bit
- Picamera2

Setup
============
- Install PiOS Lite to SD Card
- ssh into Pi
- Install PiCamera2 using <sudo apt install -y python3-picamera2 --no-install-recommends>
- clone repo and run python class

Classes
============
Wifi-cam.py:
- creates a simple HTTP server to view a camera preview

Flask_cam.py:
- creates a lightweight flask app to view preview and take an image
