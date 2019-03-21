#!/usr/bin/env python 


import subprocess
import smbus
import time
# import RPi.GPIO as GPIO

##=====I2C Testing=====##
IMU_ADDRESS = 0x68
TEMP_ADDRESS = 0x48

IMU_WHO_I_AM = 0x75 #should return 0x73, default value of the register for MP-92/65
##=====================##

TIMEOUT = 60

def testIMU(bus):

	imu_who_i_am = bus.read_word_data(IMU_ADDRESS, IMU_WHO_I_AM)
	beginTime = time.time()
	
	while imu_who_i_am != 115: #115 = 0x73
		imu_who_i_am = bus.read_word_data(IMU_ADDRESS, IMU_WHO_I_AM)
		if (time.time() - beginTime) > TIMEOUT:
			return 0
			
	return 1
	
		
def testTEMP(bus):

	temp = bus.read_word_data(TEMP_ADDRESS, 0x03) & 0xFFFF
	temp = ((temp << 8) & 0xFF00) + (temp >> 8) 
	temp = (temp / 32.0) /8.0
	beginTime = time.time()
	
	while temp != 80.0:
		temp = bus.read_word_data(TEMP_ADDRESS, 0x03) & 0xFFFF
		temp = ((temp << 8) & 0xFF00) + (temp >> 8) 
		temp = (temp / 32.0) /8.0
		if (time.time() - beginTime) > TIMEOUT:
			return 0
			
	return 1
	

def run_command(command):

	output = subprocess.getstatusoutput(command)
	return output
	

def testUSB():

	command = "sudo blkid | grep -c /dev/sd"
	usbDetected = int(run_command(command)[-1])
	beginTime = time.time()

	while usbDetected != 3 :
		usbDetected = int(run_command(command)[-1])
		if (time.time() - beginTime) > TIMEOUT:
			return 0

	return 1
	
	
bus = smbus.SMBus(1)

if(testUSB()==1):
	print("USB OK")
else:
	print("USB NOT OK")
	
	
if(testIMU(bus)==1):
	print("IMU OK")
else:
	print("IMU NOT OK")
	
if(testTEMP(bus)==1):
	print("TEMP OK")
else:
	print("TEMP NOT OK")
