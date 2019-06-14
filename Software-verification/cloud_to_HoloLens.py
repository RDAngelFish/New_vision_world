# import sys
# sys.path.append("D:/openpose-master/openpose-master/build/examples/tutorial_api_python/")
from openni import openni2
import numpy as np
import sys
import cv2
import os
from sys import platform
import ftd2xx as ftd
import socket
# import threading
import struct
import time
import math

# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../python/openpose/Release');
        os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' + dir_path + '/../../bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('../../python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print(
        'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

openni2.initialize()

dev = openni2.Device.open_any()
print('opening kinect', dev.get_device_info())

depth_stream = dev.create_depth_stream()
color_stream = dev.create_color_stream()
depth_stream.start()
color_stream.start()

dmap_count = 0

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "../../../models/"
params["hand"] = True
# params["face"] = True
# "It would slightly reduce the frame rate in order to highly reduce the lag. Mainly useful for 1)
# Cases where it is needed a low latency (e.g., webcam in real-time scenarios with low-range GPU devices);
# and 2) Debugging OpenPose when it is crashing to locate the error."
params["disable_multi_thread"] = True
# keep single person
params["number_people_max"] = 1
# params["fps_max"] = -1
params["hand_detector"] = 0
# params["hand_scale_number"] = 1
# params["hand_scale_range"] = 0.4
params["body"] = 1

all_data = np.zeros(shape=(200, 20))
all_data_target = np.zeros(shape=(200, 20))
data = np.zeros(shape=(200, 20))
data_target = np.zeros(shape=(1, 200))
sample_data = np.zeros(shape=(6, 10))

# piano: 0 / drum: 1 / BA: 2
target = 0

count = 0
count_sample = 0
counter = 0

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()
datum = op.Datum()

# ---------------------------------- SVM----------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

iris = load_iris()
print(iris.DESCR)
X_d = iris.data
X = np.loadtxt('output/data/final_1.txt')
Y = np.loadtxt('output/data/final_target.txt')

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=87)
# plt.scatter(x_train[:, 0], x_train[:, 1], c=y_train)
# plt.show()

from sklearn.svm import SVC

clf = SVC()
clf.fit(x_train, y_train)
# ---------------------------------- SVM----------------------------------------


# ----------------------------socket server-----------------------------------
bind_ip = "192.168.0.132"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

server.listen(5)
print("[*] Listening on %s:%d" % (bind_ip, bind_port))

test_wifi = int('0000_0000_0000_0000_0000_0000_0000_0000', 2)

while True:
    client, addr = server.accept()
    print("[*] Acepted connection from: %s:%d" % (addr[0], addr[1]))

    # -----------------------camera-------------------------------

    while True:
        # depth map
        frame = depth_stream.read_frame()
        dframe_data = np.array(frame.get_buffer_as_triplet()).reshape([480, 640, 2])
        dpt = np.asarray(dframe_data[:, :, 0], dtype='float32')
        # rgb map
        cframe = color_stream.read_frame()
        cframe_data = np.array(cframe.get_buffer_as_triplet()).reshape([480, 640, 3])
        cframe_data = cv2.cvtColor(cframe_data, cv2.COLOR_BGR2RGB)

        # read hand rectangle locations
        handRectangles = [
            # Left/Right hands person 0
            [
                op.Rectangle(320.035889, 377.675049, 69.300949, 69.300949),
                op.Rectangle(0., 0., 0., 0.),
            ],
            # Left/Right hands person 1
            [
                op.Rectangle(80.155792, 407.673492, 80.812706, 80.812706),
                op.Rectangle(46.449715, 404.559753, 98.898178, 98.898178),
            ],
            # Left/Right hands person 2
            [
                op.Rectangle(185.692673, 303.112244, 157.587555, 157.587555),
                op.Rectangle(88.984360, 268.866547, 117.818230, 117.818230),
            ]
        ]

        # Create new datum
        # cv2.imshow("input", cframe_data)

        # Face landmark
        #  import dlib
        #  detector = dlib.get_frontal_face_detector()  # 使用dlib庫提供的人臉提取器
        #  predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  # 構建特徵提取器
        #  img_gray = cv2.cvtColor(cframe_data, cv2.COLOR_RGB2GRAY)
        #  rects = detector(img_gray, 0)
        #  if len(rects) == 0:
        #      print('cannot detect landmark')
        #  else:
        #      for i in range(len(rects)):
        #          landmarks = np.matrix([[p.x, p.y] for p in predictor(cframe_data, rects[i]).parts()])  # 人臉關鍵點識別
        #          for idx, point in enumerate(landmarks):
        #              pos = (point[0, 0], point[0, 1])
        #              cv2.circle(cframe_data, pos, 1, color=(0, 0, 255), thickness=-1)
        # # cv2.imshow("img", cframe_data)

        datum.cvInputData = cframe_data
        datum.handRectangles = handRectangles
        # Process and display image
        opWrapper.emplaceAndPop([datum])
        output_img = datum.cvOutputData
        # draw line
        vertical_line_color_320 = (0, 255, 0)
        cv2.line(output_img, (320, 0), (320, 640), vertical_line_color_320, 1)
        horizontal_line_color_355 = (0, 0, 255)
        cv2.line(output_img, (0, 355), (640, 355), horizontal_line_color_355, 1)
        horizontal_line_color_400 = (255, 0, 0)
        cv2.line(output_img, (0, 400), (640, 400), horizontal_line_color_400, 1)
        cv2.imshow("OpenPose 1.4.0 - Tutorial Python API", output_img)
        key = cv2.waitKey(1)
        # -------------------------------------------------- SVM verify --------------------------------------------------------
        if datum.handKeypoints[1].shape == ():
            print("Cannot find people")
        elif datum.poseKeypoints[0][0][0] == 0 and datum.poseKeypoints[0][0][1] == 0 and datum.poseKeypoints[0][0][
            2] == 0:
            print("Cannot find body")
        elif datum.handKeypoints[0][0][0][0] == 0 and datum.handKeypoints[0][0][0][1] == 0 and \
                datum.handKeypoints[0][0][0][2] == 0:
            print("Cannot find left hand")
        elif datum.handKeypoints[1][0][0][0] == 0 and datum.handKeypoints[1][0][0][1] == 0 and \
                datum.handKeypoints[1][0][0][2] == 0:
            print("Cannot find right hand")
        else:
            body_center_xy = (datum.poseKeypoints[0][1][:2]) / 100
            test_tmp = ((datum.handKeypoints[0][0][4][:2]) / 100) - body_center_xy
            for i in range(2, 6):
                xy = ((datum.handKeypoints[0][0][4 * i][:2]) / 100) - body_center_xy
                test_tmp = np.concatenate((test_tmp, xy), axis=0)
            for i in range(1, 6):
                xy = ((datum.handKeypoints[1][0][4 * i][:2]) / 100) - body_center_xy
                test_tmp = np.concatenate((test_tmp, xy), axis=0)
            test = np.zeros(shape=(1, 20))
            for i in range(0, 20):
                test[0][i] = test_tmp[i]
            predict = clf.predict(test)

            right_hand_finger_x = []
            right_hand_finger_y = []
            left_hand_finger_x = []
            left_hand_finger_y = []
            ten_fingers_y = []
            if predict == 0:
                print(
                    "````````````````````````````````````````````````````````````````````It's the piano!!!``````````````````````````````````````````````````")
                for i in range(5, 0, -1):
                    right_hand_finger_x.append(np.ceil(datum.handKeypoints[1][0][4 * i][0]))
                    right_hand_finger_y.append(np.ceil(datum.handKeypoints[1][0][4 * i][1]))
                for i in range(1, 6):
                    left_hand_finger_x.append(np.ceil(datum.handKeypoints[0][0][4 * i][0]))
                    left_hand_finger_y.append(np.ceil(datum.handKeypoints[0][0][4 * i][1]))
                # [R20 R16 R12 R8 R4 L4 L8 L12 L16 L20]
                ten_fingers_x = right_hand_finger_x + left_hand_finger_x
                ten_fingers_y = right_hand_finger_y + left_hand_finger_y
                piano_num_tmp = [0 for n in range(35)]
                for i in range(0, len(ten_fingers_y)):
                    if ten_fingers_y[i] > 355:
                        number = int((ten_fingers_x[i] - (320 - 14 * 19)) // 19 + 1)
                        # print(str(number))
                        piano_num_tmp[number - 1] = 1
                # print(str(final_num))
                instrument_bit = [1, 0, 0, 0]
                piano_num = piano_num_tmp[:28]
                piano_bit_tmp = instrument_bit + piano_num[::-1]
                piano_bit = ("".join('%s' % i for i in piano_bit_tmp))
                piano_int = int(piano_bit, 2)
                test_wifi = piano_int
                packed_int = struct.pack("I", test_wifi)  # i = int, I = unsigned int
                client.send(packed_int)
                print("send success", test_wifi)
                print(str(piano_int))
            elif predict == 1:
                print(
                    "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!It's the drum!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                right_hand_4_x = np.ceil(datum.handKeypoints[1][0][4][0])
                right_hand_4_y = np.ceil(datum.handKeypoints[1][0][4][1])
                left_hand_4_x = np.ceil(datum.handKeypoints[0][0][4][0])
                left_hand_4_y = np.ceil(datum.handKeypoints[0][0][4][1])
                # distance =math.sqrt((right_hand_4_x - left_hand_4_x)**2 + (right_hand_4_y - left_hand_4_y)**2)
                distance_x = left_hand_4_x - right_hand_4_x
                # distance_x_center = distance_x / 2
                # distance = abs(distance_x - distance_x_center)
                # distance = right_hand_4_x - 320
                drum_num = [0 for n in range(28)]
                instrument_bit = [0, 1, 0, 0]
                # right - real: left hand
                y_level = 300
                if right_hand_4_y > y_level and left_hand_4_y < y_level:
                    print("!!!!!!!!!!!!!!!!!!right!!!!!!!!!!!!!!!!!!!!!!!!!")
                    if right_hand_4_x > 270 and right_hand_4_x < 320:
                        print("inner")
                        # 0100
                        drum_num[25] = 1
                        drum_bit_tmp = instrument_bit + drum_num
                        drum_bit = ("".join('%s' % i for i in drum_bit_tmp))
                        drum_int = int(drum_bit, 2)
                        test_wifi = drum_int
                        packed_int = struct.pack("I", test_wifi)  # i = int, I = unsigned int
                        client.send(packed_int)
                        print("send success", test_wifi)
                        print(str(drum_int))

                    elif right_hand_4_x > 220 and right_hand_4_x <= 270:
                        print("outside")
                        # 1000
                        drum_num[24] = 1
                        drum_bit_tmp = instrument_bit + drum_num
                        drum_bit = ("".join('%s' % i for i in drum_bit_tmp))
                        drum_int = int(drum_bit, 2)
                        test_wifi = drum_int
                        packed_int = struct.pack("I", test_wifi)  # i = int, I = unsigned int
                        client.send(packed_int)
                        print("send success", test_wifi)
                        print(str(drum_int))

                    else:
                        print("no")

                # left
                if right_hand_4_y < y_level and left_hand_4_y > y_level:
                    print("!!!!!!!!!!!!!!!!!!left!!!!!!!!!!!!!!!!!!!!!!!!!")
                    if left_hand_4_x > 320 and left_hand_4_x < 370:
                        print("inner")
                        # 0010
                        drum_num[26] = 1
                        drum_bit_tmp = instrument_bit + drum_num
                        drum_bit = ("".join('%s' % i for i in drum_bit_tmp))
                        drum_int = int(drum_bit, 2)
                        test_wifi = drum_int
                        packed_int = struct.pack("I", test_wifi)  # i = int, I = unsigned int
                        client.send(packed_int)
                        print("send success", test_wifi)
                        print(str(drum_int))

                    elif left_hand_4_x > 370 and left_hand_4_x <= 420:
                        print("outside")
                        # 0001
                        drum_num[27] = 1
                        drum_bit_tmp = instrument_bit + drum_num
                        drum_bit = ("".join('%s' % i for i in drum_bit_tmp))
                        drum_int = int(drum_bit, 2)
                        test_wifi = drum_int
                        packed_int = struct.pack("I", test_wifi)  # i = int, I = unsigned int
                        client.send(packed_int)
                        print("send success", test_wifi)
                        print(str(drum_int))

                    else:
                        print("no")
                # both hand
                if right_hand_4_y > y_level and left_hand_4_y > y_level:
                    print("!!!!!!!!!!!!!!!!!!both!!!!!!!!!!!!!!!!!!!!!!!!!")
                    if distance_x <= 100:
                        print("inner")
                        # 0110
                        drum_num[25] = 1
                        drum_num[26] = 1
                        drum_bit_tmp = instrument_bit + drum_num
                        drum_bit = ("".join('%s' % i for i in drum_bit_tmp))
                        drum_int = int(drum_bit, 2)
                        test_wifi = drum_int
                        packed_int = struct.pack("I", test_wifi)  # i = int, I = unsigned int
                        client.send(packed_int)
                        print("send success", test_wifi)
                        print(str(drum_int))

                    elif distance_x > 100 and distance_x <= 200:
                        print("outside")
                        # 1001
                        drum_num[24] = 1
                        drum_num[27] = 1
                        drum_bit_tmp = instrument_bit + drum_num
                        drum_bit = ("".join('%s' % i for i in drum_bit_tmp))
                        drum_int = int(drum_bit, 2)
                        test_wifi = drum_int
                        packed_int = struct.pack("I", test_wifi)  # i = int, I = unsigned int
                        client.send(packed_int)
                        print("send success", test_wifi)
                        print(str(drum_int))

                    else:
                        print("no")
            else:
                print("It's the BA!!!")
                right_hand_4_x = np.ceil(datum.handKeypoints[1][0][4][0])
                right_hand_4_y = np.ceil(datum.handKeypoints[1][0][4][1])
                left_hand_4_x = np.ceil(datum.handKeypoints[0][0][4][0])
                left_hand_4_y = np.ceil(datum.handKeypoints[0][0][4][1])
                distance_x = left_hand_4_x - right_hand_4_x
                distance_y = left_hand_4_y - right_hand_4_y
                ba_num = [0 for n in range(28)]
                instrument_bit = [0, 0, 1, 0]
                if distance_y <= 5 and distance_x <= 30:
                    print("~~~~~~~~~~~~~~kuon~~~~~~~~~~~~")
                    # 01
                    ba_num[27] = 1
                    ba_bit_tmp = instrument_bit + ba_num
                    ba_bit = ("".join('%s' % i for i in ba_bit_tmp))
                    ba_int = int(ba_bit, 2)
                    test_wifi = ba_int
                    packed_int = struct.pack("I", test_wifi)  # i = int, I = unsigned int
                    client.send(packed_int)
                    print("send success", test_wifi)
                    print(str(ba_int))
                elif left_hand_4_y > right_hand_4_y and distance_y > 20 and distance_x <= 30:
                    print(" DOWN sound!!!!!!!!!!!!!!!!!!")
                    # 100
                    ba_num[26] = 1
                    ba_bit_tmp = instrument_bit + ba_num
                    ba_bit = ("".join('%s' % i for i in ba_bit_tmp))
                    ba_int = int(ba_bit, 2)
                    test_wifi = ba_int
                    packed_int = struct.pack("I", test_wifi)  # i = int, I = unsigned int
                    client.send(packed_int)
                    print("send success", test_wifi)
                    print(str(ba_int))
                # elif left_hand_4_y < right_hand_4_y and distance_y > 20 and distance_x <= 30:
                #     print(" UP sound!!!!!!!!!!!!!!!!!!")
                else:
                    qcencqie = 0
        # if predict == 0:
        #     i = int('0100_0000_0000_0000_0000_0000_0000_0000', 2)
        # i = int('0100_0000_0000_0000_0000_0000_0000_0000', 2)
        # while True:
        #     try:
        #         packed_int = struct.pack("I", test_wifi)  # i = int, I = unsigned int
        #         client.send(packed_int)
        #         print("send success", i)
        #         test_wifi = test_wifi + 1
        #         time.sleep(2)
        #     except:
        #         print("break")
        #         break



        # -------------------------------------------------- SVM verify --------------------------------------------------------
        # -------------------------------------------------- write output ------------------------------------------------------
        #     if datum.handKeypoints[1].shape == ():
        #         print("Cannot find people")
        #     elif datum.poseKeypoints[0][0][0] == 0 and datum.poseKeypoints[0][0][1] == 0 and datum.poseKeypoints[0][0][2] == 0:
        #         print("Cannot find body")
        #     elif datum.handKeypoints[0][0][0][0] == 0 and datum.handKeypoints[0][0][0][1] == 0 and datum.handKeypoints[0][0][0][2] == 0:
        #         print("Cannot find left hand")
        #     elif datum.handKeypoints[1][0][0][0] == 0 and datum.handKeypoints[1][0][0][1] == 0 and datum.handKeypoints[1][0][0][2] == 0:
        #         print("Cannot find right hand")
        #     else:
        #         # print("Right hand (piano_data): \n" + str(datum.handKeypoints[1]))
        #         body_center_xy = (np.ceil(datum.poseKeypoints[0][1][:2]))/100
        #         data_tmp = ((np.ceil(datum.handKeypoints[0][0][4][:2]))/100) - body_center_xy
        #         for i in range(2, 6):
        #             xy = ((np.ceil(datum.handKeypoints[0][0][4*i][:2]))/100) - body_center_xy
        #             data_tmp = np.concatenate((data_tmp, xy), axis=0)
        #         for i in range(1, 6):
        #             xy = ((np.ceil(datum.handKeypoints[1][0][4*i][:2]))/100) - body_center_xy
        #             data_tmp = np.concatenate((data_tmp, xy), axis=0)
        #         data[counter] = data_tmp
        #         data_target[0][counter] = target
        #         print(counter + 1)
        #         counter = counter + 1
        #         print("OK")
        #
        #         if counter == 200:
        #             np.savetxt('output/data/p_data.txt', data, fmt='%.2f')
        #             np.savetxt('output/data/p_data_target.txt', data_target, fmt='%d')
        #             print('save data')
        #             depth_stream.stop()
        #             color_stream.stop()
        #             dev.close()
        # -------------------------------------------------- write output ------------------------------------------------------

        ###################################### function ###################################
        # press Q to show keypointsz
        if int(key) == 113:
            print("Body keypoints: \n" + str(datum.poseKeypoints))
            print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
            print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))
            print("OK")

        # Press A to dump pic
        if int(key) == 97:
            cv2.imwrite('output/depth/' + str(dmap_count) + '.png', dpt)
            cv2.imwrite('output/rgb/' + str(dmap_count) + '_ori.png', cframe_data)
            cv2.imwrite('output/rgb/' + str(dmap_count) + '_openpose.png', datum.cvOutputData)
            fp = open('output/obj/' + '/test' + str(dmap_count) + '.txt', 'w', encoding='UTF-8')
            print("Body keypoints: \n" + str(datum.poseKeypoints))
            print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
            print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))
            print("OK")
            dmap_count += 1
            # body
            for r in range(0, datum.poseKeypoints.shape[1]):
                if datum.poseKeypoints[0][r][0] != 0:
                    fp.write("v ")
                    fp.write(str(datum.poseKeypoints[0][r][0]))
                    fp.write(" ")
                    fp.write(str(datum.poseKeypoints[0][r][1]))
                    fp.write(" ")
                    fp.write(str(datum.poseKeypoints[0][r][2]))
                    fp.write("\n")
                else:
                    fp.write("v ")
                    fp.write(str(datum.poseKeypoints[0][r][0]))
                    fp.write(" ")
                    fp.write(str(datum.poseKeypoints[0][r][1]))
                    fp.write(" ")
                    fp.write(str(datum.poseKeypoints[0][r][2]))
                    fp.write("\n")
            # left hand
            for i in range(0, datum.handKeypoints[0].shape[1]):
                if datum.handKeypoints[0][0][i][0] != 0:
                    fp.write("v ")
                    fp.write(str(datum.handKeypoints[0][0][i][0]))
                    fp.write(" ")
                    fp.write(str(datum.handKeypoints[0][0][i][1]))
                    fp.write(" ")
                    fp.write(str(datum.handKeypoints[0][0][i][2]))
                    fp.write("\n")
                else:
                    fp.write("v ")
                    fp.write(str(datum.handKeypoints[0][0][i][0]))
                    fp.write(" ")
                    fp.write(str(datum.handKeypoints[0][0][i][1]))
                    fp.write(" ")
                    fp.write(str(datum.handKeypoints[0][0][i][2]))
                    fp.write("\n")

            # right hand
            for i in range(0, datum.handKeypoints[1].shape[1]):
                if datum.handKeypoints[1][0][i][0] != 0:
                    fp.write("v ")
                    fp.write(str(datum.handKeypoints[1][0][i][0]))
                    fp.write(" ")
                    fp.write(str(datum.handKeypoints[1][0][i][1]))
                    fp.write(" ")
                    fp.write(str(datum.handKeypoints[1][0][i][2]))
                    fp.write("\n")
                else:
                    fp.write("v ")
                    fp.write(str(datum.handKeypoints[1][0][i][0]))
                    fp.write(" ")
                    fp.write(str(datum.handKeypoints[1][0][i][1]))
                    fp.write(" ")
                    fp.write(str(datum.handKeypoints[1][0][i][2]))
                    fp.write("\n")
            fp.close()
            # # body
            # for r in range(0, datum.poseKeypoints.shape[1]):
            #     fp.write("v ")
            #     for s in range(0, 3):
            #         if s == 2:
            #             fp.write(str(datum.poseKeypoints[0][r][2]))
            #         else:
            #             fp.write(str(datum.poseKeypoints[0][r][s]))
            #             fp.write(" ")
            #     fp.write("\n")
            # # left hand
            # for i in range(0, datum.handKeypoints[0].shape[1]):
            #     fp.write("v ")
            #     for j in range(0, 3):
            #         if j == 2:
            #             fp.write(str(datum.handKeypoints[0][0][i][2]))
            #         else:
            #             fp.write(str(datum.handKeypoints[0][0][i][j]))
            #             fp.write(" ")
            #     fp.write("\n")
            # # right hand
            # for i in range(0, datum.handKeypoints[1].shape[1]):
            #     fp.write("v ")
            #     for j in range(0, 3):
            #         if j == 2:
            #             fp.write(str(datum.handKeypoints[1][0][i][2]))
            #         else:
            #             fp.write(str(datum.handKeypoints[1][0][i][j]))
            #             fp.write(" ")
            #     fp.write("\n")
            # fp.close()

        ##################################### Dump data ###################################
        # Press Z to dump piano_data => 0
        if int(key) == 122:
            if datum.handKeypoints[1][0][0][0] == 0 and datum.handKeypoints[1][0][0][1] == 0 and \
                    datum.handKeypoints[1][0][0][2] == 0:
                print('cannot find right hand')
            else:
                piano_data = (datum.handKeypoints[1][0][4][:2]) / 100
                print("Right hand (piano_data): \n" + str(datum.handKeypoints[1]))
                for i in range(2, 6):
                    xy = (datum.handKeypoints[1][0][i * 4][:2]) / 100
                    piano_data = np.concatenate((piano_data, xy), axis=0)
                all_data[count] = piano_data
                print(count + 1)
                count = count + 1

        # Press X to dump drum_data => 1
        if int(key) == 120:
            if datum.handKeypoints[1][0][0][0] == 0 and datum.handKeypoints[1][0][0][1] == 0 and \
                    datum.handKeypoints[1][0][0][2] == 0:
                print('cannot find right hand')
            else:
                drum_data = datum.handKeypoints[1][0][4][:2]
                print("Right hand (drum_data): \n" + str(datum.handKeypoints[1]))
                for i in range(2, 6):
                    xy = datum.handKeypoints[1][0][i + 1][:2]
                    drum_data = np.concatenate((drum_data, xy), axis=0)
                all_data[count] = drum_data
                print(count + 1)
                count = count + 1

        # Press C to dump flute_data => 2
        if int(key) == 99:
            if datum.handKeypoints[1][0][0][0] == 0 and datum.handKeypoints[1][0][0][1] == 0 and \
                    datum.handKeypoints[1][0][0][2] == 0:
                print('cannot find right hand')
            else:
                flute_data = datum.handKeypoints[1][0][4][:2]
                print("Right hand (flute_data): \n" + str(datum.handKeypoints[1]))
                for i in range(2, 6):
                    xy = datum.handKeypoints[1][0][4 * i][:2]
                    flute_data = np.concatenate((flute_data, xy), axis=0)
                all_data[count] = flute_data
                print(count + 1)
                count = count + 1

        # Press F to finish data
        if int(key) == 102:
            np.savetxt('output/data/data_trytrytrytry.txt', all_data, fmt='%.3f')
            print('save data')

        # Press R to reset data
        if int(key) == 114:
            all_data = np.zeros(shape=(150, 42))
            count = 0

        # Press D to sample
        if int(key) == 100:
            if datum.handKeypoints[1][0][0][0] == 0 and datum.handKeypoints[1][0][0][1] == 0 and \
                    datum.handKeypoints[1][0][0][2] == 0:
                print('cannot find right hand')
            else:
                sample = datum.handKeypoints[1][0][0][:2]
                print("Right hand (flute_data): \n" + str(datum.handKeypoints[1]))
                for i in range(0, datum.handKeypoints[1].shape[1] - 1):
                    xy = datum.handKeypoints[1][0][i + 1][:2]
                    sample = np.concatenate((sample, xy), axis=0)
                sample_data[count_sample] = sample
                print(count_sample + 1)
                count_sample = count_sample + 1

        # Press E to sample
        if int(key) == 101:
            np.savetxt('output/data/sample_try_different_pos.txt', sample_data, fmt='%.3f')
            print('save sample')

        # Press W to verify instrument
        if int(key) == 119:
            if datum.handKeypoints[1][0][0][0] == 0 and datum.handKeypoints[1][0][0][1] == 0 and \
                    datum.handKeypoints[1][0][0][2] == 0:
                print('cannot find right hand')
            else:
                test_tmp = (datum.handKeypoints[1][0][4][:2]) / 100
                for i in range(2, 6):
                    xy = (datum.handKeypoints[1][0][i * 4][:2]) / 100
                    test_tmp = np.concatenate((test_tmp, xy), axis=0)
                test = np.zeros(shape=(1, 10))
                for i in range(0, 10):
                    test[0][i] = test_tmp[i]
                predict = clf.predict(test)
                if predict == 0:
                    print("It's the piano!!!")
                elif predict == 1:
                    print("It's the drum!!!")
                else:
                    print("It's the flute!!!")

        # Press T to transfer data to usb
        if int(key) == 119:
            d = ftd.open(0)  # Open first FTDI device
            print(d.getDeviceInfo())

# close app

depth_stream.stop()
color_stream.stop()
dev.close()