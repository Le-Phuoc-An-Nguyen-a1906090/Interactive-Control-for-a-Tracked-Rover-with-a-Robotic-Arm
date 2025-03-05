#The code was originally made by Caleb Rodger and modified by Le Phuoc An Nguyen, James, Abby, Kimmy
#first install the python3 onto the computer
#make sure to choose add python.exe to PATH 
#in customise installation, make sure to choose everything

# IMPORT THESE LIBRARIES
# ----------------------

import serial # pip install pyserial
import roslibpy # pip install roslibpy
import numpy as np # pip install numpy

# ADJUST THESE VALUES AS NEEDED
# -----------------------------
# Control Computer IP:
robot_ip = '192.168.0.101' #the lattepanda

# Arduino Serial Port

serial_port = 'COM7' #The arduino

client = roslibpy.Ros(host=robot_ip, port=9090)
client.run()

talker = roslibpy.Topic(client, '/set_arm_joint_angles', 'aubo_interface_msgs/msg/ArmJoints')

talker2 = roslibpy.Topic(client, '/cmd_vel', 'geometry_msgs/Twist')


def readserial(comport, baudrate):

    ser = serial.Serial(comport, baudrate, timeout=0.1)

    while True:
        data = ser.readline().decode().strip().split(',')
        if data:
            try:
                if client.is_connected:
                    print(data)
                    talker.publish(roslibpy.Message({
                        # 'linear': {
                        # 'x': float(data[0])*(0.4/90),
                        # 'y': 0,
                        # 'z': 0
                        # },
                        # 'angular': {
                        # 'x': 0,
                        # 'y': 0,
                        # 'z': -np.sign(float(data[0]))*float(data[1])*(0.4/90)
                        # }
                        'joint0': float(data[0]),
                        'joint1': float(data[1]),
                        'joint2': float(data[2]),
                        'joint3': float(data[3]),
                        'joint4': float(data[4]),
                        'joint5': float(data[5]),
                    }))
                    talker2.publish(roslibpy.Message({
                        'linear': {
                    #
                        'x': -float(data[8])*(1/2),
                        'y': 0,
                        'z': 0
                        },
                        'angular': {
                        'x': 0,
                        'y': 0,
                        'z': -float(data[7])*(1/2)
                        }
                    }))
            except:
                print('err')

                   


if __name__ == '__main__':
    #define the asynchronous communication speed
    readserial(serial_port, 115200)
