# New Vision World
  Welcome to New Vision World! 
  :smile:
  
  We are ready to show you how New Vision World works. 

  
Contents
--------
- [Introduction](#Introduction)
    - [Architecture](#Architecture)
- [Hardware Setup](#Hardware-Setup)
- [Software Setup](#Software-Setup)
- [User Manual](#User-Manual)
    - [Required hardware](#Required-hardware)
    - [Required software](#Required-software)

## Introduction

  Due to the development of science and technology, people's concept of musical instruments of various forms has gradually changed. The somatosensory technology combined with character motion sensing and hand gesture recognition is the trend in the future. Therefore, it is thought to apply finger recognition to virtual playing instruments. This work combines the possibilities of technology and music multimedia.

### Architecture

  System begins in Kinect camera to get RGB information of image. Through the open source called OpenPose, we can generate skeleton of body and keypoints of two hands. Then the computer outputs these information to ARC and doing SVM algorithm to verify each instrument with many different sounds. After getting the result of verification and sounds, we output the data to HoloLens to have a real stage to perform every instuments. The main flow is following:
  
![Flow](images/Flow.JPG)
<div align="center"><img width="300" height="300" src="images/ARC_demo.gif"></div>
  
## Hardware Setup

* Kinect for Xbox 360 (Kinect) camera 

    Kinect is created by Microsoft and it has three lens. We use kinect to get real-time RGB information for each image. Before we driver kinect, we use the library called Open Natural Interface(OpenNI) to finish driving.

* ARC

  [See toolchain for much more detail.](https://github.com/foss-for-synopsys-dwc-arc-processors)
  
  
  1. Start the ARC to transfer or read data.
  
      ![ARC_start](images/ARC_start.jpg)
  
  2. Sure to connect correctly and start to recieve data.
  
      ![ARC_result0](images/ARC_result0.png)
  
      ![ARC_result1](images/ARC_result1.jpg)
  
* USB-FTDI module

  It needs to transfer data between the computer and ARC through USB. We choose FT2232HL chip to transfer. [See the document we use.](https://www.intra2net.com/en/developer/libftdi/download.php)
  
  ![ARC_USB](images/ARC_USB.png)
    

* WIFI – TCP/IP 

  The WIFI module we used is ESP8266. ARC is the srver and HoloLens is the client. When HoloLens connect to ARC, ARC will transfer 32-bits data contiuously to HoloLens. The flow is following:

  ![WIFI](images/WIFI.png)    

* HoloLens

  Microsoft HoloLens is an Augmented Reality (AR) device developed by Microsoft. It is part of the Windows Mixed Reality AR Platform incorporated with Windows 10 OS. Similar to other OHMDs (optical head-mounted displays), HoloLens is a see-through display worn over your eyes. Unlike the Oculus Rift and other VR Devices, the eye-piece component of HoloLens is transparent and the headset requires neither PC nor smartphone. It is able to project high-definition (HD) virtual content or holograms over real world objects. 

  ![HoloLens](images/HoloLens.jpg)
  
## Software Setup

* ARC GNU Toolchain

* OpenPose

    [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) represents the first real-time multi-person system to jointly detect human body, hand, facial, and foot keypoints (in total 135 keypoints) on single images. It has been widely used in many applications. Here, in order to verify different instruments, we gonna use body and hands information to do SVM training and testing.  
    The skeleton of body and keypoints of hands are following:
   
   ![OpenPose_skeleton](images/OpenPose_skeleton.png)

* Support vector machines(SVM)

  SVM is a discriminative classifier formally defined by a separating hyperplane. In other words, given labeled training data (supervised learning), the algorithm outputs an optimal hyperplane which categorizes new examples. In two dimentional space this hyperplane is a line dividing a plane in two parts where in each class lay in either side. We train model with 200 data per class. 
 
## User Manual

### Required hardware
* ARC IoT Development Kit (IoTDK) 
* ESP8266 Wi-Fi module
* FTDI FT2232 USB to UART module
* Camera (Kinect or any other webcam)
* HoloLens

### Required software
* ARC GNU Toolchain
* OPENNI (for kinect camera here)
* OpenPose (please click [here](https://github.com/CMU-Perceptual-Computing-Lab/openpose) for much more detail requirements), and check GPU performance [here](https://docs.google.com/spreadsheets/d/1-DynFGvoScvfWDA1P4jDInCkbD4lg0IKOYbXgEq0sK0/edit#gid=0). We use GTX 1080 in this project.
* [LIBSVM](https://www.csie.ntu.edu.tw/~cjlin/libsvm/) (a library for Support Vector Machines) 



