#!/usr/bin/env python
import oursql

class writeToMySqlDb(object):
	"""docstring for writeToMySqlDb"""
	def __init__(self, keyFile, tableName = "Computerinput"):
		super(writeToMySqlDb, self).__init__()

		hostName = "andreasherten.de"
		dbName = "quantified"
		self.db_connection = oursql.connect(host=hostName, user=keyFile.user, passwd=keyFile.password, db=dbName)

		self.cur = self.db_connection.cursor()
		self.tableName = tableName
	def __del__(self):
		self.cur.close()
		self.db_connection.close()

	def insertArrayIntoDb(self, theData):
		executionString = "INSERT INTO " + self.tableName
		manipulatedData = theData + theData[1:3]
		self.cur.execute(executionString + ' (Date, Keystrokes, Mouseclicks) VALUES (?, ?, ?)' + ' ON DUPLICATE KEY UPDATE Keystrokes=?, Mouseclicks=?' , manipulatedData)
	def readFromDb(self):
		self.cur.execute('SELECT * from ' + self.tableName) #+ ' ORDER BY Date')
		for row in self.cur.fetchall():
			print row, row[0]
