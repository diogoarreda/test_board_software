#!/usr/bin/env python 


import subprocess
import smbus
import time
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
gpio_list = [21,22,23,24]

GPIO.setup(gpio_list, GPIO.OUT)

##=====I2C Testing=====##
GYRO_ADDRESS = 0x68
ACCEL_ADDRESS = 0x18

TEMP_ADDRESS = 0x48

WHO_I_AM = 0x00


ACCEL_WHO_I_AM = 8990
GYRO_WHO_I_AM = 8719
##=====================##

TIMEOUT = 45

##Test starts with both of them connected##

#GPIO.output(23, GPIO.LOW) #green
#GPIO.output(24,GPIO.HIGH)
#GPIO.output(22, GPIO.LOW) #red
#GPIO.output(21,GPIO.HIGH)

def testAccel(bus):

	accel = bus.read_word_data(ACCEL_ADDRESS, WHO_I_AM)
		
	beginTime = time.time()
	
	while accel != ACCEL_WHO_I_AM: #115 = 0x73
		accel = bus.read_word_data(ACCEL_ADDRESS, WHO_I_AM)
		if (time.time() - beginTime) > TIMEOUT:
			return 0
			
	return 1


def testGyro(bus):

	gyro = bus.read_word_data(GYRO_ADDRESS, WHO_I_AM)
	
	beginTime = time.time()
	
	while gyro != GYRO_WHO_I_AM: #115 = 0x73
		gyro = bus.read_word_data(GYRO_ADDRESS, WHO_I_AM)
		if (time.time() - beginTime) > 5:
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
		if (time.time() - beginTime) > 5:
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

def red():
	GPIO.output(22, GPIO.LOW) #red
	GPIO.output(21,GPIO.HIGH)

	return

def red_off():
	GPIO.output(22, GPIO.LOW) #red_off
	GPIO.output(21,GPIO.LOW)

	return

def green_off():
	
	GPIO.output(23, GPIO.LOW) #green_off
	GPIO.output(24,GPIO.LOW)

	return
def green():
	
	GPIO.output(23, GPIO.LOW) #green
	GPIO.output(24,GPIO.HIGH)

	return

def blink_red():
	GPIO.output(22, GPIO.LOW)
	GPIO.output(21,GPIO.HIGH)
	sleep(1)
	GPIO.output(21,GPIO.LOW)
	sleep(1)

	return

def blink_green():
	GPIO.output(23, GPIO.LOW)
	GPIO.output(24,GPIO.HIGH)
	sleep(1)
	GPIO.output(24,GPIO.LOW)
	sleep(1)

	return

green()
red()
#--------------------- Evaluation ---------------------------	
bus = smbus.SMBus(1)


file  = open("/home/pi/result.txt", "w")
test = 0
t = 0
u = 0
te = 0
us = 0
g = 0

if(testUSB()==1):
	#print("USB OK")
	file.write("USB OK\n") 
	test = test + 1
	#GPIO.output(24,GPIO.HIGH)
else:
	#print("USB NOT OK")
	file.write("USB NOT OK\n") 
	us = 1
	
if(testGyro(bus)==1):
	#print("IMU OK")
	file.write("Gyro OK\n") 
	test = test + 1

	##GPIO.output(23,GPIO.HIGH)
else:
	#print("IMU NOT OK")
	file.write("Gyro NOT OK\n") 
	g = 1

	
if(testTEMP(bus)==1):
	#print("TEMP OK")
	file.write("TEMP OK") 
	test = test + 1
	
	#GPIO.output(22,GPIO.HIGH)
else:
	#print("TEMP NOT OK")
	file.write("TEMP NOT OK") 
	te = 1

while t < 60:
	if (test == 3):
			green()
			red_off()

	elif (g == 1): #gyro problem
			green()
			blink_red()
		
	elif (us == 1): #usb problem
			red()
			green_off()

	elif (te == 1): #temp sens problem
			blink_red()
			green_off()
	t = t + 1 

file.close()
time.sleep(10)
GPIO.cleanup()

#GPIO.output(24,GPIO.LOW)
#GPIO.output(23,GPIO.LOW)
#GPIO.output(22,GPIO.LOW)
#GPIO.output(21,GPIO.LOW)
