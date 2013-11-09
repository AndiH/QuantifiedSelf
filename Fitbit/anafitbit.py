import fitbit
import json
import keys as keys
import sqlite3 as sql
import sys, datetime

consumerkey = keys.ckey
consumersecret = keys.csecret
userkey = keys.ukey
usersecret = keys.usecret

yesterday = datetime.date.today() - datetime.timedelta(days=1)
history = []
for i in range(2, 10):
	history.append(datetime.date.today() - datetime.timedelta(days=i))

fbApiConnection = fitbit.Fitbit(consumerkey, consumersecret, user_key=userkey, user_secret=usersecret)

todaysActivity = fbApiConnection.activities(yesterday)

formattedActivity = json.dumps(todaysActivity)

data = json.loads(formattedActivity)

# print data["summary"]["elevation"]

formattedDataArray = (yesterday.strftime("%s"), data["summary"]["elevation"], data["summary"]["sedentaryMinutes"], data["summary"]["lightlyActiveMinutes"], data["summary"]["caloriesOut"], data["summary"]["caloriesBMR"], data["summary"]["marginalCalories"], data["summary"]["fairlyActiveMinutes"], data["summary"]["veryActiveMinutes"], data["summary"]["activityCalories"], data["summary"]["steps"], data["summary"]["floors"], data["summary"]["activeScore"])

# print json.dumps(todaysActivity, indent=4, separators=(',', ': '))
# print formattedDataArray

dbConnection = sql.connect('fbData.db')

with dbConnection:
	dbCursor = dbConnection.cursor()
	dbCursor.execute('INSERT INTO fitbitdata VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', formattedDataArray) 
