# Sample, in-development file to showcase a working updateFitbitDb.py
import keys as keys
import updateFitbitDb as updateFitbitDb
import sys, datetime

today = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(days=1)
daybeforeyesterday = yesterday - datetime.timedelta(days=1)

testObj = updateFitbitDb.updateFitbitDb(keys, "fbData.db")

testObj.printKeys()
testObj.updateDate(today)
testObj.updateDate(yesterday)
testObj.updateDate(daybeforeyesterday)
