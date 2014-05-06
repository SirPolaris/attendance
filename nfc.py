# This class is the main interface to MFRC522.py it calls the class and encapsulates the wait and anticollision loop.

import MFRC522
import time


def readNfc ():
	reading = True
	MIFAREReader = MFRC522

	while reading:
		print("------ Start of loop -------")
		# Because we import the "Modual" then access the classes, we but it in a
		# holder to do work. (No Data types!)

		#while continue_reading:
		(status, TagType) = MIFAREReader.MFRC522.MFRC522_Request(MIFAREReader.MFRC522(), MIFAREReader.PICC.REQIDL)

		if status == 0:  # MI.OK
			print("REQIDL - OK")
		if status == 1:
			print("REQIDL - ARGERR")
		if status == 2:
			print("REQIDL - DNC")

		(status, backData) = MIFAREReader.MFRC522().MFRC522_Anticoll()

		if status == 0:
			print("AntiCol - OK")
		if status == 1:
			print("AntiCol - ARGERR")
		if status == 2:
			print("AntiCol - DNC")

		if status == MIFAREReader.MI.OK:
			MIFAREReader.MFRC522().AntennaOff()
			print("DATA:" + backData[0]) + str(backData[1]) + str(backData[2]) + str(backData[3]) + str(backData[4])
			return str(backData[0]) + str(backData[1]) + str(backData[2]) + str(backData[3]) + str(backData[4])

		time.sleep(4)  # so we can see whats going on

