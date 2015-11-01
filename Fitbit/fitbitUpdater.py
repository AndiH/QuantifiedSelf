#!/usr/bin/env python
import sqlInfo
import updateFitbitDb
import timerangegenerator

dateRange, tableName = timerangegenerator.parse()

fbUpdater = updateFitbitDb.updateFitbitDb("fitbitKeys.json", sqlInfo, tableName=tableName)

for date in dateRange:
	fbUpdater.updateDate(date)
