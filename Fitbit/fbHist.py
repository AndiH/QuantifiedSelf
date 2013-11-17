import keys as keys
import updateFitbitDb as updateFitbitDb
import datetime
import argparse
import calendar as cal

parser = argparse.ArgumentParser(description='Update historcal Fitbit data')
parser.add_argument('month', metavar='MONTH', type=int, help='Month to be requested')
parser.add_argument('-db', '--database', default='fbHist.db', help='DB file name')
parser.add_argument('-t', '--table', default='fitbithistory', help='Name of SQL table name')
parser.add_argument('-y', '--year', default='2013', type=int, help='Year to be requested')
args = parser.parse_args()

databaseFile = args.database
tableName = args.table
month = args.month
year = args.year

fbUpdater = updateFitbitDb.updateFitbitDb(keys, databaseFile, tableName)

listOfDates = []
for i in range(1, cal.monthrange(year,month)[1]+1):
	listOfDates.append(datetime.datetime(year=year, month=month, day=i))
print "Saving historical Fitbit data from " + str(year) + "-" + str(month)

for date in reversed(listOfDates):
	fbUpdater.updateDate(date)
