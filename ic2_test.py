#!/usr/bin/python

import smbus
import time

bus = smbus.SMBus(1)	# 1 = /dev/i2c-1

IMU_ADDRESS = 0x68
TEMP_ADDRESS = 0x48

IMU_WHO_I_AM = 0x75 #should return 0x73, default value of the register for MP-92/65


i = 0

#read a value of temperature 
while i!=60:

	temp = bus.read_word_data(TEMP_ADDRESS, 0) & 0xFFFF
	temp = ((temp << 8) & 0xFF00) + (temp >> 8) 

	#print(temp)
	#print("{0:b}".format(temp))
	temp2 = (temp / 32.0) /8.0
	print "Temperature: %(temp2)f Celsius" % {"temp2": temp2}

	
	imu_who_i_am = bus.read_word_data(IMU_ADDRESS, IMU_WHO_I_AM)
	#print("{0:x}".format(imu_who_i_am))
	
	if imu_who_i_am == 115: #115 = 0x73
		print "Successful connection to imu"
	else:
		print "problems during imu connection"


	i = i + 1
	time.sleep(1)
