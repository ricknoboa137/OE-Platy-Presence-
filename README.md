# OE-Platy-Presence
This repository contains the current development state of a Telepresence Toolkit for mobile robot platforms, developed by the Obuda University. 

## Receive stereo-video in MetaQuest_2 from a mobile robot platform.



1. Download the Unity Project from the link: 

https://drive.google.com/file/d/1Yay8N6dB6167HbH-BpTKxqf23NE7s6MG/view?usp=sharing

2. Connect Oculus MetaQuest 2 to the usb port and make sure you granted usb permissions in the device
3. start the Oculus desktop link
4.  Open the project using unity 2022.3.15
   ![image](https://github.com/ricknoboa137/OE-Platy-Presence-/assets/45580543/ee550470-26d7-4c92-b97b-0c5f5d42abb8)
5. In Unity go to: Files -> Build Settings -> RunDevice | and select the Oculus device
6. Make sure to select the scene to be rendered
7. In the Hierarchy field, select the element called MQTTreceiver (see previous image) and edit the field of the IP adress of the computer runing the MQTT broker, port by default is 1883.
8. The fields of Subscribe and Publish are the MQTT topics which we are using to recieve the image form the platform and send the controller's joystick state as well as the current position and rotation of the headset (modify the topic names acordingly if necesary)
9. Hit the "PLay" button tu run the scene

![image](https://github.com/ricknoboa137/OE-Platy-Presence-/assets/45580543/d7d954e2-9bfe-4b45-bce5-5118b5cf7062)


The project contains, between other elements, 2 RawImage elements used to display the stereo-images transmited from the robot platform. (RawImageRight / RawImageLeft as can be noticed in the Project architecture in the above image)

## Transmite Stereo-video from a Mobile Robot Platform

1. Mke sure the camera is connected to the platform
2. Dowload the folder PythonScripts from this repo (Make sure to edit the IP adress of the computer runing an MQTT Broker, port 1883)
3. Run the Script named "MQTTVideoStream.py"
   (This code uses OpenCV library to capture the frame from the USB camera, process the image, compress it using base 64 standar, and transmit it using MQTT)
   In this step we have the chance to aply image recognition models using OpenCV.
5. Note: you can reduce the image size to reduce latency. 
``` www
```
## Mirror headset position and rotation in the platform. 

1. The gimbal design can be found in the following link:

2. make sure the servomotors are connected to the digital pins 4 and 5 of the board Node MCU V3, equiped with a ESP12 wifi chip.
3. Download the Arduino code from this repo in the folder ArduinoSketch/nodeMCU
4. make sure to update the IP adress of the computer runing the MQTT Broker and subscribe to the Topic "test1" to receive information from the headset
5. Load the script to the board   
