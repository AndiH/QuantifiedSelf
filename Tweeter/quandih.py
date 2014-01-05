#!/usr/bin/env python

import tweepy, datetime
import oursql
import twitterkeys as tkeys
import sqlInfo
# sys.path.append("../Computerinput/")
# from ..Computerinput.mySqlHandler import mySqlHandler

CONSUMER_KEY = tkeys.ckey
CONSUMER_SECRET = tkeys.csecret
ACCESS_KEY = tkeys.akey
ACCESS_SECRET = tkeys.asecret

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

db_connection = oursql.connect(host=sqlInfo.host, user=sqlInfo.user, passwd=sqlInfo.password, db=sqlInfo.database)
cur = db_connection.cursor()

tableName = "Computerinput"
cur.execute('SELECT * from ' + tableName)
plainData = cur.fetchall()

data = list(list(plainData))

dataInt = [] # not really needed
for entry in data:
	dataInt.append(map(int, entry))
# print dataInt

yesterday = datetime.date.today() - datetime.timedelta(days=1)
yesterdayEpoch = int(yesterday.strftime("%s"))
for row in dataInt: # works also only with data, now that data is a two-level list(list())
	if (row[0] == yesterdayEpoch):
		# print row
		yesterdaysKeys = row[1]
		yesterdaysClicks = row[2]

api.update_status("Yesterday (" + str(yesterday.strftime("%d.%m.%Y")) + "), @AndiH pressed " + str(yesterdaysKeys) + " keys and clicked " + str(yesterdaysClicks) + " times.")
