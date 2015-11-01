#!/usr/bin/env python
import fitbit
import json
import oursql

class updateFitbitDb(object):
	""" Class to retrieve your Fitbit information and save it into a sqlite3 db."""
	def __init__(self, fitbitKeyFile, sqlInfo, tableName='Fitbit'):
		with open(fitbitKeyFile) as datafile:
			self.fitbitKeys = json.load(datafile)
		self.tableName = tableName
		# self.fbApiConnection = fitbit.Fitbit(self.fitbitKeys.ckey, self.fitbitKeys.csecret, user_key=self.fitbitKeys.ukey, user_secret=self.fitbitKeys.usecret)
		self.fbApiConnection = fitbit.Fitbit(self.fitbitKeys["client_id"], self.fitbitKeys["client_secret"], oauth2 = True, access_token = self.fitbitKeys["access_token"], refresh_token = self.fitbitKeys["refresh_token"])

		newTokens = self.fbApiConnection.client.refresh_token()
		self.fitbitKeys["refresh_token"] = newTokens["refresh_token"]
		self.fitbitKeys["access_token"] = newTokens["access_token"]
		with open(fitbitKeyFile, "w") as datafile:
			json.dump(self.fitbitKeys, datafile)

		self.db_connection = oursql.connect(host=sqlInfo.host, user=sqlInfo.user, passwd=sqlInfo.password, db=sqlInfo.database)
		self.cur = self.db_connection.cursor()
	def __del__(self):
		self.cur.close()
		self.db_connection.close()
	def printKeys(self):
		""" Prints your key (costumer and user) strings """
		print self.fitbitKeys["client_id"], self.fitbitKeys["client_secret"], self.fitbitKeys["access_token"], self.fitbitKeys["refresh_token"]
	def updateDate(self, theDate):
		""" Main function of this class. Retrieves theDate date's Fitbit data and inserts it into sqlFile sqlite3 db. If a date already exists the data is updated. """
		activity = self.fbApiConnection.activities(theDate)
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

		doubleData = formattedDataArray + formattedDataArray[1:]
		self.cur.execute('INSERT INTO ' + self.tableName + ' (date, elevation, sedentaryMinutes, lightlyActiveMinutes, caloriesOut, caloriesBMR, marginalCalories, fairlyActiveMinutes, veryActiveMinutes, activityCalories, steps, floors, activeScore) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)' + ' ON DUPLICATE KEY UPDATE elevation=?, sedentaryMinutes=?, lightlyActiveMinutes=?, caloriesOut=?, caloriesBMR=?, marginalCalories=?, fairlyActiveMinutes=?, veryActiveMinutes=?, activityCalories=?, steps=?, floors=?, activeScore=?', doubleData)
