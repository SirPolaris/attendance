## Main Program File

import sys  # this if for error handling

import mysqlInterface as mySQL



## Local vars
continueRunning = True


###### Device Vars #####
# Supporting Classes
class hasNetwork:


	LAN = False
Wireless = False
Radio3G = False
RadioLocalMegaHurts = False

# Operational vars
bootPath = "boot.bst"

# Default Values
DeviceName = "C-UNIT1"  # Device Name
hasDisplay = False  # LCD display unit
hasGPS = False  # GPS sensor
hasNetwork.LAN = False  # LAN connection
hasNetwork.Wireless = False  # Wireless radio
hasNetwork.Radio3G = False  # Cellular Radio
hasNetwork.RadioLocalMegaHurts = False  # Family Radio Broadcasting


def importMessageTypes():
	mySQL.mySQLInterface().executeProc("ReturnDataTypes")
	return


def selfCheck():
	return


def selfUpdate():
	return


def pullDataFromBoot():
	return


def checkForMessagesFromHome():
	return


# Communicate Home
# This is used for sending health status home. As well as alerting home of critical warning/errors
def sendMessageHome(packet, type):
	# Packet = "Help I am on fire!"
	# Type = 0 (Critical Message)
	# mySQl.SendMessage(type, packet);
	# The other end processes it as a alert. Stores it in a log that archived or somthing.
	# Other code will sends out emails, texts, update website. We want to keep the device lean
	return


# On StartUp preform these actions
def onStartup():
	# Initialise variables
	# Preform preflight selfcheck
	selfCheck()
	#If Diagnostic mode = true e-mail a log, flash lights
	return


def gpsHandler():
	return


def attemptToRecover():
	# On unexpected error use a try catch network to attempt to recover from unexpected things.
	return


def clearVars():
	# Set all vars to 0 state
	return


def reboot():
	# Clear variables
	clearVars()
	# Call int main
	int_main()
	return


# Initialise
def int_main():
	#Startup

	# Main Process Loop
	# Loop indefinitely until ordered to shutdown.
	while (continueRunning == True):
		try:  #Try
		#On exspected Error
		#If error is cleaned up and handled. Do not break, attempt to recover.
		#Else unexpected. No handling attempt to recover.
		#On Interupt/Signal/Message

		except:  #Catch
			#On unexpected Error
			#Attempet to recover. If not reboot.
			try:
				attemptToRecover()
				e = sys.exc_info()[0]
				sendMessageHome("<p>Error: %s</p>" % e, 0)
			except:
				#If it returns a failure - Kill the program
				continueRunning = False

	return


