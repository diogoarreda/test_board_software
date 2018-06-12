import serial
import time 

i = 0

ser = serial.Serial("/dev/ttyAMA0",
	baudrate = 9600, 
	parity = serial.PARITY_NONE, 
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = 1	
) #Opening Port 0, coerent with the servo drivers specs

while i != 5:
	ser.write("sim")
	data=ser.read(4)
	
	if data == "sim":
		i = 5
		print "UART successful working"
	else:
		print "Error on UART Communication"
		i = i+1

ser.close()
