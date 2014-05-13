#-------------------------------------------------------------------------------
# Name:        MFRC522.py
# Purpose:     Basic hardware interface class for the Mifare MFRC-522 module 13.56 MHz card/tag reader
#
# Author:      Justin, Kelly (Previous authors: Mario Gomez, Jakub Dvorak)
# Updated:     2014-MAY
#-------------------------------------------------------------------------------

import RPi.GPIO as GPIO
import spi
import signal


class PCD:
	IDLE = 0x00
	AUTHENT = 0x0E
	RECEIVE = 0x08
	TRANSMIT = 0x04
	TRANSCEIVE = 0x0C
	RESETPHASE = 0x0F
	CALCCRC = 0x03


class PICC:
	REQIDL = 0x26
	REQALL = 0x52
	ANTICOLL = 0x93
	SElECTTAG = 0x93
	AUTHENT1A = 0x60
	AUTHENT1B = 0x61
	READ = 0x30
	WRITE = 0xA0
	DECREMENT = 0xC0
	INCREMENT = 0xC1
	RESTORE = 0xC2
	TRANSFER = 0xB0
	HALT = 0x50


class MI:
	OK = 0
	NOTAGERR = 1
	ERR = 2


class MFRC522:
	# These are all hex codes that provide english front to each action.
	NRSTPD = 22
	MAX_LEN = 16

	Reserved00 = 0x00
	CommandReg = 0x01
	CommIEnReg = 0x02
	DivlEnReg = 0x03
	CommIrqReg = 0x04
	DivIrqReg = 0x05
	ErrorReg = 0x06
	Status1Reg = 0x07
	Status2Reg = 0x08
	FIFODataReg = 0x09
	FIFOLevelReg = 0x0A
	WaterLevelReg = 0x0B
	ControlReg = 0x0C
	BitFramingReg = 0x0D
	CollReg = 0x0E
	Reserved01 = 0x0F

	Reserved10 = 0x10
	ModeReg = 0x11
	TxModeReg = 0x12
	RxModeReg = 0x13
	TxControlReg = 0x14
	TxAutoReg = 0x15
	TxSelReg = 0x16
	RxSelReg = 0x17
	RxThresholdReg = 0x18
	DemodReg = 0x19
	Reserved11 = 0x1A
	Reserved12 = 0x1B
	MifareReg = 0x1C
	Reserved13 = 0x1D
	Reserved14 = 0x1E
	SerialSpeedReg = 0x1F

	Reserved20 = 0x20
	CRCResultRegM = 0x21
	CRCResultRegL = 0x22
	Reserved21 = 0x23
	ModWidthReg = 0x24
	Reserved22 = 0x25
	RFCfgReg = 0x26
	GsNReg = 0x27
	CWGsPReg = 0x28
	ModGsPReg = 0x29
	TModeReg = 0x2A
	TPrescalerReg = 0x2B
	TReloadRegH = 0x2C
	TReloadRegL = 0x2D
	TCounterValueRegH = 0x2E
	TCounterValueRegL = 0x2F

	Reserved30 = 0x30
	TestSel1Reg = 0x31
	TestSel2Reg = 0x32
	TestPinEnReg = 0x33
	TestPinValueReg = 0x34
	TestBusReg = 0x35
	AutoTestReg = 0x36
	VersionReg = 0x37
	AnalogTestReg = 0x38
	TestDAC1Reg = 0x39
	TestDAC2Reg = 0x3A
	TestADCReg = 0x3B
	Reserved31 = 0x3C
	Reserved32 = 0x3D
	Reserved33 = 0x3E
	Reserved34 = 0x3F

	serNum = []


	def __init__(self, spd = 1000000):
		spi.openSPI(speed = spd)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(22, GPIO.OUT)
		GPIO.output(self.NRSTPD, 1)
		self.MFRC522_Init()

	def MFRC522_Reset(self):
		self.Write_MFRC522(self.CommandReg, PCD.RESETPHASE)

	def Write_MFRC522(self, addr, val):
		spi.transfer(((addr << 1) & 0x7E, val))

	def Read_MFRC522(self, addr):
		val = spi.transfer((((addr << 1) & 0x7E) | 0x80, 0))
		return val[1]

	def SetBitMask(self, reg, mask):
		tmp = self.Read_MFRC522(reg)
		self.Write_MFRC522(reg, tmp | mask)

	def ClearBitMask(self, reg, mask):
		tmp = self.Read_MFRC522(reg)
		self.Write_MFRC522(reg, tmp & (~mask))

	def AntennaOn(self):
		temp = self.Read_MFRC522(self.TxControlReg)
		if (~(temp & 0x03)):
			self.SetBitMask(self.TxControlReg, 0x03)

	def AntennaOff(self):
		self.ClearBitMask(self.TxControlReg, 0x03)

	def MFRC522_ToCard(self, command, sendData):
		backData = []
		backLen = 0
		status = MI.ERR
		irqEn = 0x00
		waitIRq = 0x00
		lastBits = None
		n = 0
		i = 0

		if command == PCD.AUTHENT:
			irqEn = 0x12
			waitIRq = 0x10

		if command == PCD.TRANSCEIVE:
			irqEn = 0x77
			waitIRq = 0x30

		self.Write_MFRC522(self.CommIEnReg, irqEn | 0x80)
		self.ClearBitMask(self.CommIrqReg, 0x80)
		self.SetBitMask(self.FIFOLevelReg, 0x80)

		self.Write_MFRC522(self.CommandReg, PCD.IDLE)

		# Main writer to the card. Bit by bit send.
		while (i < len(sendData)):
			self.Write_MFRC522(self.FIFODataReg, sendData[i])
			i = i + 1

		self.Write_MFRC522(self.CommandReg, command)

		if command == PCD.TRANSCEIVE:
			self.SetBitMask(self.BitFramingReg, 0x80)

		i = 2000

		while True:
			n = self.Read_MFRC522(self.CommIrqReg)  # Listens to the SPI - for data
			i = i - 1

			if ~((i != 0) and ~(n & 0x01) and ~(n & waitIRq)):  # Acts on data or time out?
				break

		self.ClearBitMask(self.BitFramingReg, 0x80)

		if i != 0:
			if (self.Read_MFRC522(self.ErrorReg) & 0x1B) == 0x00:
				status = MI.OK

				if n & irqEn & 0x01:
					status = MI.NOTAGERR

				if command == PCD.TRANSCEIVE:
					n = self.Read_MFRC522(self.FIFOLevelReg)
					lastBits = self.Read_MFRC522(self.ControlReg) & 0x07
					if lastBits != 0:
						backLen = (n - 1) * 8 + lastBits
					else:
						backLen = n * 8

					if n == 0:
						n = 1
					if n > self.MAX_LEN:
						n = self.MAX_LEN

					i = 0
					while i < n:
						backData.append(self.Read_MFRC522(self.FIFODataReg))
						i = i + 1
			else:
				print("I errored!")
				status = MI.ERR

		return (status, backData, backLen)


	def MFRC522_Request(self, reqMode):
		status = None
		backBits = None
		TagType = []

		self.Write_MFRC522(self.BitFramingReg, 0x07)

		TagType.append(reqMode)
		(status, backData, backBits) = self.MFRC522_ToCard(PCD.TRANSCEIVE, TagType)

		if ((status != MI.OK) | (backBits != 0x10)):
			status = MI.ERR

		return (status, backBits)


	def MFRC522_Anticoll(self):
		'''
		In the context of RFID, anti-collision refers to different ways to keep radio waves from one device
		from interfering with radio waves from another device. RFID readers may make use of anti-collision
		algorithms to enable a single reader to read more than one tag in the reader's field.

		Tag collision in RFID systems happens when multiple tags are energized by the RFID tag reader simultaneously,
		and reflect their respective signals back to the reader at the same time. This problem is often seen whenever
		a large volume of tags must be read together in the same RF field. The reader is unable to differentiate these
		signals; tag collision confuses the reader.
		'''

		backData = []
		serNumCheck = 0

		serNum = []

		self.Write_MFRC522(self.BitFramingReg, 0x00)

		# Problem is here
		serNum.append(PICC.ANTICOLL)
		serNum.append(0x20)

		(status, backData, backBits) = self.MFRC522_ToCard(PCD.TRANSCEIVE, serNum)

		if (status == MI.OK):
			i = 0
			if len(backData) == 5:
				while i < 4:
					serNumCheck = serNumCheck ^ backData[i]
					i = i + 1
				if serNumCheck != backData[i]:
					status = MI.ERR
			else:
				status = MI.ERR

		return (status, backData)

	def MFRC522_Init(self):
		GPIO.output(self.NRSTPD, 1)

		self.MFRC522_Reset()

		self.Write_MFRC522(self.TModeReg, 0x8D)
		self.Write_MFRC522(self.TPrescalerReg, 0x3E)
		self.Write_MFRC522(self.TReloadRegL, 30)
		self.Write_MFRC522(self.TReloadRegH, 0)

		self.Write_MFRC522(self.TxAutoReg, 0x40)
		self.Write_MFRC522(self.ModeReg, 0x3D)
		self.AntennaOn()

