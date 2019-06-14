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


System begins in Kinect camera to get RGB information of image. Through the open source called OpenPose, we can generate skelon of body and keypoints of two hands. Then the computer outputs these information to ARC and doing SVM algorithm to verify each instrument with many different sounds. After getting the result of verification and sounds, we output the data to HoloLens to have a real stage to perform every instuments. The main flow is following:


![Flow](images/Flow.JPG)

* Kinect for Xbox 360 (Kinect) camera 

  Kinect is created by MicroSoft and it has three lens. We use kinect to get real-time RGB information for each image. Before we driver kinect, we use Open Natural Interface(OpenNI) library to achieve our target.

* OpenPose

* USB-FTDI Driver
* Support vector machines(SVM)
* ARC
* WIFI – TCP/IP 
* HoloLens

## Hardware Setup

## Software Setup

## Architecture

## User Manual


https://www.ftdichip.com/Support/Documents/DataSheets/ICs/DS_FT2232H.pdf







