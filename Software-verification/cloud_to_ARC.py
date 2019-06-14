# import sys
# sys.path.append("D:/openpose-master/openpose-master/build/examples/tutorial_api_python/")
from openni import openni2
import numpy as np
import sys
import cv2
import os
from sys import platform
import ftdi_pybind
import socket
import struct
import time
# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../python/openpose/Release');
        os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('../../python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

openni2.initialize()

dev = openni2.Device.open_any()
print('opening kinect', dev.get_device_info())

depth_stream = dev.create_depth_stream()
color_stream = dev.create_color_stream()
depth_stream.start()
color_stream.start()

params = dict()
params["model_folder"] = "../../../models/"
params["hand"] = True
params["disable_multi_thread"] = True
params["number_people_max"] = 1
params["hand_detector"] = 0
params["body"] = 1

all_data = np.zeros(shape=(200, 20))
all_data_target = np.zeros(shape=(200, 20))
data = np.zeros(shape=(200, 20))
data_target = np.zeros(shape=(1, 200))
sample_data = np.zeros(shape=(6, 10))

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()
datum = op.Datum()

ftdi_pybind.init()
ftdi_pybind.send_data("vlsi", 4)
count = 0


# ----------------------------socket server-----------------------------------
bind_ip = "192.168.0.132"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

server.listen(5)
print("[*] Listening on %s:%d" % (bind_ip, bind_port))

test_wifi = int('0000_0000_0000_0000_0000_0000_0000_0000', 2)

# while True:
client, addr = server.accept()
print("[*] Acepted connection from: %s:%d" % (addr[0], addr[1]))

    # -----------------------camera-------------------------------

while True:
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


    datum.cvInputData = cframe_data
    datum.handRectangles = handRectangles
    # Process and display image
    opWrapper.emplaceAndPop([datum])
    output_img = datum.cvOutputData
    cv2.imshow("OpenPose 1.4.0 - Tutorial Python API", output_img)
    key = cv2.waitKey(1)

    if datum.handKeypoints[1].shape == ():
        print("Cannot find people")
    elif datum.poseKeypoints[0][0][0] == 0 and datum.poseKeypoints[0][0][1] == 0 and datum.poseKeypoints[0][0][2] == 0:
        print("Cannot find body")
    elif datum.handKeypoints[0][0][0][0] == 0 and datum.handKeypoints[0][0][0][1] == 0 and datum.handKeypoints[0][0][0][2] == 0:
        print("Cannot find left hand")
    elif datum.handKeypoints[1][0][0][0] == 0 and datum.handKeypoints[1][0][0][1] == 0 and datum.handKeypoints[1][0][0][2] == 0:
        print("Cannot find right hand")
    else:
        output_data_list = [0 for n in range(44)]
        body_center_x = int(datum.poseKeypoints[0][1][0])
        body_center_y = int(datum.poseKeypoints[0][1][1])
        output_data_list[0] = body_center_x // 256
        output_data_list[1] = body_center_x % 256
        output_data_list[2] = body_center_y // 256
        output_data_list[3] = body_center_y % 256

        for i in range(1, 6):
            x = int(datum.handKeypoints[0][0][4 * i][0])
            y = int(datum.handKeypoints[0][0][4 * i][1])
            output_data_list[i * 4] = x // 256
            output_data_list[i * 4 + 1] = x % 256
            output_data_list[i * 4 + 2] = y // 256
            output_data_list[i * 4 + 3] = y % 256
        for i in range(1, 6):
            x = int(datum.handKeypoints[1][0][4 * i][0])
            y = int(datum.handKeypoints[1][0][4 * i][1])
            output_data_list[i * 4 + 20] = x // 256
            output_data_list[i * 4 + 21] = x % 256
            output_data_list[i * 4 + 22] = y // 256
            output_data_list[i * 4 + 23] = y % 256

            # ftdi_pybind.init()
            # ftdi_pybind.send_data("vlsi", 4)
            # time.sleep(0.5)
        # print('1231234564865646463566815616848135')
        count = count + 1
        print(count)
        ftdi_pybind.send_data("vlsi", 4)
        ftdi_pybind.send_point_data(ftdi_pybind.list_foo(output_data_list))
        ftdi_pybind.send_data("OK", 2)

        # read data from ARC
        result = ftdi_pybind.read_data()
        result2 = result & 0xffffffff
        print("result:", result2)

        # write data to HoloLens
        packed_int = struct.pack("I", result2)  # i = int, I = unsigned int
        client.send(packed_int)
        print("send success")

# close app
color_stream.stop()
dev.close()
