# Stick Hero 6

A Raspberry Pi and Python powered robot that plays <a href="https://apps.apple.com/us/app/stick-hero/id918338898">Stick Hero</a>, a mobile game. It was created by me and 4 of my classmates for one of our courses. We used the NumPy, Pillow, GPIOZero, and PiCamera libraries. 

![Demo](https://github.com/danwei002/Stick-Hero-6/blob/main/stickHeroDemo.gif)

A demo of the robot playing the game. 


## How It Works

![Labelled Picture](https://github.com/danwei002/Stick-Hero-6/blob/main/robotLabelled.png)

The robot consists of 4 main components, two hardware and two software. The hardware components are the motor and the camera. The software components are the image processing and the game logic calculation scripts. The camera, controlled by a Python script using the PiCamera library, takes a picture of the game running on the device below it at regular intervals. This raw image is sent to the image processing script as a Pillow Image object, which is converted into a NumPy array of RGB tuples. The image processor then crops the image down to only include the phone screen and finds the distance between the current and target platforms. 

Before and after image processing: 

<img src="https://github.com/danwei002/Stick-Hero-6/blob/main/image_processing/imgs/img8.jpg" width="480" height="270">
<img src="https://github.com/danwei002/Stick-Hero-6/blob/main/image_processing/old/test.png" width="170" height="270"> 

