#!/usr/bin/python
# -*- coding: utf-8 -*-
## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2019 Intel Corporation. All Rights Reserved.

#####################################################
##           librealsense T265 example             ##
#####################################################


import argparse
from pythonosc import udp_client

# First import the library
import pyrealsense2 as rs
import math as m

from pathlib import Path

file = open(Path(__file__).with_name('User_Setting.cfg'))
all_lines = file.readlines()
#-------------------------------------------------------------------------------------#
UDP_IP = str(all_lines[3].strip())
UDP_PORT = int(all_lines[4].strip())

#UDP_IP = "127.0.0.1"
#UDP_PORT = 54321

#-------------------------------------------------------------------------------------#

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=UDP_IP,
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=UDP_PORT,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

#-------------------------------------------------------------------------------------#


# Declare RealSense pipeline, encapsulating the actual device and sensors
pipe = rs.pipeline()

# Build config object and request pose data
cfg = rs.config()
cfg.enable_stream(rs.stream.pose)

# Start streaming with requested config
pipe.start(cfg)

try:
    while True:
        # Wait for the next set of frames from the camera
        frames = pipe.wait_for_frames()

        # Fetch pose frame
        pose = frames.get_pose_frame()
        if pose:
            # Print some of the pose data to the terminal
            data = pose.get_pose_data()

            # Euler angles from pose quaternion
            # See also https://github.com/IntelRealSense/librealsense/issues/5178#issuecomment-549795232
            # and https://github.com/IntelRealSense/librealsense/issues/5178#issuecomment-550217609


            px = data.translation.x
            py = data.translation.y
            pz = data.translation.z
            
            qw = data.rotation.w
            qx = data.rotation.x
            qy = data.rotation.y
            qz = data.rotation.z

            data = [px,py,pz,qw,qx,qy,qz]
            client.send_message("/UE4_OSC", data)
            
            '''
            client.send_message("/POS_X", px)
            client.send_message("/POS_Y", py)
            client.send_message("/POS_Z", pz)

            client.send_message("/QUAT_W", qw)
            client.send_message("/QUAT_X", qx)
            client.send_message("/QUAT_Y", qy)
            client.send_message("/QUAT_Z", qz)
            '''

            print("Position: Pos_X: {0:.7f}, Pos_Y: {1:.7f}, Pos_Z: {2:.7f}".format(px, py, pz))
            print("Quaternion: QW: {0:.7f}, QX: {1:.7f}, QY: {2:.7f}, QZ: {3:.7f}".format(qw, qx, qy, qz))
            print("")
            print("")

finally:
    pipe.stop()