#!/usr/bin/env python
import sqlite3 as sql
# import argparse
import datetime, time

class readFromWhatPulseDb:
	"""Reads from Whatpulse SQLite3 database and returns info"""
	def __init__(self):
		userPrefixDir = "/Users/Andi"
		whatpulseDataDir = "/Library/Application Support/WhatPulse/"
		dataBaseFilename = "whatpulse.db"

		combinedPathToFile = userPrefixDir + whatpulseDataDir + dataBaseFilename

		# self.keyarray, self.clickarary = {}, {}

		dbConnection = sql.connect(combinedPathToFile)
		with dbConnection:
			dbCursor = dbConnection.cursor()
			dbCursor.execute("select * from keypresses")
			keyRows = dbCursor.fetchall()
			dbCursor.execute("select * from mouseclicks")
			clickRows = dbCursor.fetchall()
		
		# SOME whatpulse version introduced a change to its database structure where it now creates an entry per hour the program was active on the day - hence, we need to merge all entries of one day
		keyRowsDict = self.convertThreeTupleListToDict(keyRows)
		clickRowsDict = self.convertThreeTupleListToDict(clickRows)
		keyRows = sorted(keyRowsDict.items())
		clickRows = sorted(clickRowsDict.items())

		bothRowsDict = self.combineTwoDicts(keyRowsDict, clickRowsDict)
		bothRows = sorted(bothRowsDict.items())
		# for row in keyRows:
		# 	self.keyarray.update({int(datetime.datetime.strptime(row[0], "%Y-%m-%d").strftime("%s")):row[1]})
		# for row in clickRows:
		# 	self.clickarary.update({int(datetime.datetime.strptime(row[0], "%Y-%m-%d").strftime("%s")):row[1]})
		self.masterarray = [] # this should actually be a dict() / {}
		
		for (date, (kRow, cRow)) in bothRows:
			# TODO: Check for existance of dates in both arrays
			self.masterarray.append((int(datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%s")), kRow, cRow))
	def returnData(self):
		return self.masterarray
	def printData(self):
		print self.masterarray
	def convertThreeTupleListToDict(self, l):
		tempDict = {}
		for key, thing, hour in l:
			if (tempDict.has_key(key)):
				tempDict[key] += thing
			else:
				tempDict[key] = thing
		return tempDict
	def combineTwoDicts(self, d1, d2):
		tempDict = {}
		if (len(d2) > len(d1)):
			temp = d1
			d1 = d2
			d2 = temp
		for (key, value) in d1.items():
			value2 = -1
			if (d2.has_key(key)):
				value2 = d2[key]
			tempDict[key] = (value, value2)
		return tempDict
		
if __name__ == '__main__':
	readFromWhatPulseDb().printData()
