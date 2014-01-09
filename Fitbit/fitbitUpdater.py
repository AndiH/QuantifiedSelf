import fitbitKeys, sqlInfo
import updateFitbitDb
import timerangegenerator

dateRange, tableName = timerangegenerator.parse()

fbUpdater = updateFitbitDb.updateFitbitDb(fitbitKeys, sqlInfo, tableName=tableName)

for date in dateRange:
	fbUpdater.updateDate(date)
