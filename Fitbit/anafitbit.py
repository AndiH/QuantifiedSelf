import fitbitKeys, sqlInfo
import updateFitbitDb as updateFitbitDb
import datetime

fbUpdater = updateFitbitDb.updateFitbitDb(fitbitKeys, sqlInfo)

yesterday = datetime.date.today() - datetime.timedelta(days=1)
lastTenDays = []
for i in range(0, 10):
	lastTenDays.append(datetime.date.today() - datetime.timedelta(days=i))

for date in reversed(lastTenDays):
	fbUpdater.updateDate(date)
