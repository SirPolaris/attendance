# This class is the main interface to MFRC522.py it calls the class and encapsulates the wait and anticollision loop.

import RPi.GPIO as GPIO
import MFRC522
import time
import signal

continue_reading = True


def end_read (signal, frame):
	global continue_reading
	print("Ctrl+C captured, ending read.")
	continue_reading = False
	GPIO.cleanup()  # Suggested by Marjan Trutschl

## INT MAIN CODE ##

signal.signal(signal.SIGINT, end_read)

MIFAREReader = MFRC522.MFRC522()

while continue_reading:
	(status, TagType) = MIFAREReader.MFRC522_Request(MFRC522.PICC.REQIDL)

	if status == MFRC522.MI.OK:
		print("Card detected")

	(status, backData) = MIFAREReader.MFRC522_Anticoll()
	if status == MFRC522.MI.OK:
		print("Card read UID: " + str(backData[0]) + str(backData[1]) + str(backData[2]) + str(backData[3]) + str(
			backData[
				4]))

	#key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

	#MIFAREReader.MFRC522_SelectTag(backData)

	#status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 11, key, backData)
	#if status == MIFAREReader.MI_OK:
	#	print("AUTH OK")
	#else:
	#	print("AUTH ERROR")

