# New Vision World
  Welcome to New Vision World! 
  
  We are ready to show you how New Vision World works.
  
Contents
--------
- [Introduction](#Introduction)
- [Hardware Setup](#Hardware-Setup)
- [Software Setup](#Software-Setup)
- [Architecture](#Architecture)
- [User Manual](#User-Manual)

## Introduction

  Due to the development of science and technology, people's concept of musical instruments of various forms has gradually changed. The somatosensory technology combined with character motion sensing and hand gesture recognition is the trend in the future. Therefore, it is thought to apply finger recognition to virtual playing instruments. This work combines the possibilities of technology and music multimedia.


  System begins in Kinect camera to get RGB information of image. Through the open source called OpenPose, we can generate skeleton of body and keypoints of two hands. Then the computer outputs these information to ARC and doing SVM algorithm to verify each instrument with many different sounds. After getting the result of verification and sounds, we output the data to HoloLens to have a real stage to perform every instuments. The main flow is following:


![Flow](images/Flow.JPG)

* Kinect for Xbox 360 (Kinect) camera 

    Kinect is created by Microsoft and it has three lens. We use kinect to get real-time RGB information for each image. Before we driver kinect, we use the library called Open Natural Interface(OpenNI) to finish driving.

* OpenPose

    OpenPose represents the first real-time multi-person system to jointly detect human body, hand, facial, and foot keypoints (in total 135 keypoints) on single images.It is authored by Gines Hidalgo, Zhe Cao, Tomas Simon, Shih-En Wei, Hanbyul Joo, and Yaser Sheikh. Currently, it is being maintained by Gines Hidalgo and Yaadhav Raaj. It has been widely used in many applications. Here, in order to verify different instruments, we gonna use these body and hands information to do SVM training and testing.  The skeleton of body and keypoints of hands are following:
   
   ![OpenPose_skeleton](images/OpenPose_skeleton.png)


* USB-FTDI Driver

  It needs to transfer data between the computer and ARC through USB. We choose FT2232HL chip to transfer. [See the document we use.]  (https://www.intra2net.com/en/developer/libftdi/download.php)
  
* Support vector machines(SVM)
* ARC
* WIFI – TCP/IP 
* HoloLens

## Hardware Setup

## Software Setup

## Architecture

## User Manual


https://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT2232H.pdf







