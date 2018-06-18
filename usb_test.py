#!/usr/bin/env python 
import commands 
import sys

# MOUNT_DIR = "/home/pi/tests/usb"

def run_command(command):
	ret_code, output = commands.getstatusoutput(command)
	if ret_code == 1:
		raise Exception("FAILED: %s" % command)
	return output.splitlines()

command_mount = "sudo mount /dev/sda1 /home/pi/tests/usb"
run_command(command_mount)

print("Usb mounted")

try:
	file = open("/home/pi/tests/usb/read_this.txt.txt", "r")

except IOError:
	print "Could not open file"

with file:
	print file.read()
	print "success opening the file on the usb flash"
	#if file.read() == "yes":
	#	print "pen confirmada"
	#else:
	#	print "deu merda"

	file.close()


command_unmount = "sudo umount /home/pi/tests/usb"
run_command(command_unmount)
