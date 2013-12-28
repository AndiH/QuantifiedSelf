#!/usr/bin/env python
import sqlite3 as sql
# import argparse
import datetime, time

class readFromWhatPulseDb:
	def __init__(self):
		userPrefixDir = "/Users/Andi"
		whatpulseDataDir = "/Library/Application Support/WhatPulse/"
		dataBaseFilename = "whatpulse.db"

		combinedPathToFile = userPrefixDir + whatpulseDataDir + dataBaseFilename

		dbConnection = sql.connect(combinedPathToFile)
		with dbConnection:
			dbCursor = dbConnection.cursor()
			dbCursor.execute("select * from keypresses")
			rows = dbCursor.fetchall()

		self.masterarray = []
		for row in rows:
			self.masterarray.append((int(datetime.datetime.strptime(row[0], "%Y-%m-%d").strftime("%s")), row[1],-1))
	def returnData(self):
		return self.masterarray
	def printData(self):
		print self.masterarray

if __name__ == '__main__':
	readFromWhatPulseDb().printData()
