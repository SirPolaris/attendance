__author__ = 'Kelly'

import MySQLdb


class mySQLInterface:
	host = "localhost"
	user = "pi"
	passwd = "raspberry"
	db = "pi"

	def connect(self):
		return MySQLdb.connect \
			(
				host = self.host,
				user = self.user,
				passwd = self.passwd,
				db = self.db
			)

	def disconnect(self):
		MySQLdb.close()
		return 0

	def read(self):
		return

	def insert(self):
		return

	def executeProc(self, command):
		#Calls home and executes a stored proc returns the result
		return

	def parse(selfs, impString):
		#Using impString - parse via a delimiter, so we have all the elements of the message as requested.
		parsedString = []  # Object Holder for parsed data.

		#For each "Word chunk" in impString loop

		#Seek from start tp first delimiter

		#Save that word chunk
		parsedString[0] = "word chunk"

		#if there is no more delimiters - break
		#break

		return parsedString
