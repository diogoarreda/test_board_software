#!/usr/bin/env python 
import commands 
import sys
import smbus
import time
import serial
import RPi.GPIO as GPIO

#---------------- Initial Definitions ------------------------#

IMU_ADDRESS = 0x68
TEMP_ADDRESS = 0x48
IMU_WHO_I_AM = 0x75 				#default value of the register for MP-92/65: 0x73

led_gpio_list = [21,22,23,24] 		#Led Green: 21 -> 22 | Led Red: 23 -> 24 , Requires 220Ω to 1kΩ Resistor with the Leds
GPIO.setup(led_gpio_list, GPIO.OUT)


#------------- Function to Execute Commands on Terminal ------------------------#

def run_command(command):
	ret_code, output = commands.getstatusoutput(command)
	if ret_code == 1:
		raise Exception("FAILED: %s" % command)
	return output.splitlines()

#---------------- USB Ports Communication Test ------------------------#

#MOUNT_DIR = "/home/pi/tests/usb"

command_mount = "sudo mount /dev/sda1 /home/pi/tests/usb"
run_command(command_mount)

				# ---------------- TO BE CHECK ------------------#
command_mount = "sudo mount /dev/sda2 /home/pi/tests/usb"
run_command(command_mount)

command_mount = "sudo mount /dev/sda3 /home/pi/tests/usb"
run_command(command_mount)
				# ---------------- TO BE CHECK ------------------#

try:
	file1 = open("/home/pi/tests/usb/usb1.txt", "r") #File inside Pen 1 should be named "usb1.txt" 

except IOError:
	test_usb1 = False; 		#print "Could not open file"
with file1:
	print file1.read()
	test_usb1 = True;		#print "success opening the file on the usb flash"

				
				# ---------------- TO BE CHECK ------------------#
try:
	file2 = open("/home/pi/tests/usb/usb2.txt", "r") #File inside Pen 2 should be named "usb2.txt" 

except IOError:
	test_usb2 = False; 		#print "Could not open file"
with file2:
	print file2.read()
	test_usb2 = True;		#print "success opening the file on the usb flash"

try:
	file3 = open("/home/pi/tests/usb/usb3.txt", "r") #File inside Pen 3 should be named "usb3.txt" 

except IOError:
	test_usb3 = False; 		#print "Could not open file"
with file3:
	print file3.read()
	test_usb3 = True;		#print "success opening the file on the usb flash"
				# -------------- TO BE CHECK ------------------#

file1.close()
file2.close()
file3.close()

#---------------- UART Communication Test ------------------------#

ser = serial.Serial("/dev/ttyAMA0",
	baudrate = 9600, 
	parity = serial.PARITY_NONE, 
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1	
) 							#Opening Port 0, coerent with the servo drivers specs

#Temporary way, just connecting tx to rx on the baseboard V1.02
ser.write("sim")
data=ser.read(4)
	
if data == "sim":
	test_uart = True; 		#print "UART successful working"
else:
	test_uart = False; 		#print "Error on UART Communication"

ser.close() 				#Closing serial port (UART Communication)


#--------------- I2C Communication Tests ------------------------#

bus = smbus.SMBus(1)	# 1 = /dev/i2c-1

temp = bus.read_word_data(TEMP_ADDRESS, 0) & 0xFFFF
temp = ((temp << 8) & 0xFF00) + (temp >> 8) # gathering the 2 8-bit words that have the temperature value  
temp = (temp / 32.0) /8.0 					# converting to Celcius


#IMU detecting 	
imu_who_i_am = bus.read_word_data(IMU_ADDRESS, IMU_WHO_I_AM)	
if imu_who_i_am == 115: #115 = 0x73
	test_imu = True;
else:
	test_imu = False;

#-------------------- Test Evaluation -----------------------------#

if (
	test_imu == True and test_uart == True and 
	test_usb1 == True and test_usb2 == True and test_usb3 == True
	):

	#LED Green ON
	GPIO.output(21, GPIO.HIGH)
	GPIO.output(22, GPIO.LOW)	
else:
	#LED Red ON
	GPIO.output(23, GPIO.HIGH)
	GPIO.output(24, GPIO.LOW)	

#-------------------- Final Commands -----------------------------#
GPIO.cleanup()
command_unmount = "sudo umount /home/pi/tests/usb" #Unmount usb pen 1
run_command(command_unmount)
