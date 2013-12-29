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

		# for row in keyRows:
		# 	self.keyarray.update({int(datetime.datetime.strptime(row[0], "%Y-%m-%d").strftime("%s")):row[1]})
		# for row in clickRows:
		# 	self.clickarary.update({int(datetime.datetime.strptime(row[0], "%Y-%m-%d").strftime("%s")):row[1]})
		self.masterarray = [] # this should actually be a dict() / {}
		for kRow, cRow in zip(keyRows, clickRows):
			# TODO: Check for existance of dates in both arrays
			self.masterarray.append((int(datetime.datetime.strptime(kRow[0], "%Y-%m-%d").strftime("%s")), kRow[1], cRow[1]))
	def returnData(self):
		return self.masterarray
	def printData(self):
		print self.masterarray

if __name__ == '__main__':
	readFromWhatPulseDb().printData()
