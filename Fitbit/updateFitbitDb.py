import fitbit
import json
import sqlite3 as sql
import datetime

class updateFitbitDb(object):
	""" Class to retrieve your Fitbit information and save it into a sqlite3 db."""
	def __init__(self, keyFile, sqlFile=None):
		self.keyFile = keyFile
		self.sqlFile = sqlFile
	def printKeys(self):
		""" Prints your key (costumer and user) strings """
		print self.keyFile.ckey, self.keyFile.csecret, self.keyFile.ukey, self.keyFile.usecret
	def updateDate(self, theDate):
		""" Main function of this class. Retrieves theDate date's Fitbit data and inserts it into sqlFile sqlite3 db. If a date already exists the data is updated. """
		fbApiConnection = fitbit.Fitbit(self.keyFile.ckey, self.keyFile.csecret, user_key=self.keyFile.ukey, user_secret=self.keyFile.usecret)
		activity = fbApiConnection.activities(theDate)
		formattedActivity = json.dumps(activity)
		data = json.loads(formattedActivity)
		formattedDataArray = (theDate.strftime("%s"), 
			data["summary"]["elevation"], 
			data["summary"]["sedentaryMinutes"], 
			data["summary"]["lightlyActiveMinutes"], 
			data["summary"]["caloriesOut"], 
			data["summary"]["caloriesBMR"], 
			data["summary"]["marginalCalories"], 
			data["summary"]["fairlyActiveMinutes"], 
			data["summary"]["veryActiveMinutes"], 
			data["summary"]["activityCalories"], 
			data["summary"]["steps"], 
			data["summary"]["floors"], 
			data["summary"]["activeScore"])

		dbConnection = sql.connect(self.sqlFile)
		with dbConnection:
			dbCursor = dbConnection.cursor()
			dbCursor.execute('INSERT OR REPLACE INTO fitbitdata VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', formattedDataArray) 
			
