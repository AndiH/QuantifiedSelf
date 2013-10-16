import datetime, calendar, csv, sys

inputFileName = sys.argv[1]

outputFileName = inputFileName[:-4] + '_processed.csv'
outputfile = open(outputFileName, 'wb')
writer = csv.writer(outputfile, delimiter=';') # semicolon because of stupid German localization of Numbers.app

inputfile = open(inputFileName, 'rb')
reader = csv.reader(inputfile, delimiter=';')

counter = 0
numberOfProcesses = 0
numberOfOccurencesInThisHour = 0

for row in reader:
	timestamp = datetime.datetime.fromtimestamp(int(row[0]))
	currentYear = timestamp.strftime('%Y')
	currentMonth = timestamp.strftime('%m')
	currentDay = timestamp.strftime('%d')
	currentHour = timestamp.strftime('%H')
	currentMinute = timestamp.strftime('%M')
	if (counter == 0):
		lastYear = currentYear
		lastMonth = currentMonth
		lastDay = currentDay
		lastHour = currentHour
		lastMinute = currentMinute
		counter += 1
	# print currentYear, currentMonth, currentDay, currentHour, currentMinute, int(row[1])
	if ((currentYear == lastYear) and (currentMonth == lastMonth) and (currentDay == lastDay) and (currentHour == lastHour)):
		numberOfOccurencesInThisHour += 1
		numberOfProcesses += int(row[1])
	else:
		datestring = str(currentYear) + '-' + str(currentMonth) + "-" + str(currentDay) + ' ' + str(currentHour)
		convertedDatetime = calendar.timegm( datetime.datetime.strptime(datestring,"%Y-%m-%d %H").utctimetuple() )
		meanNumberOfProcesses = float(numberOfProcesses)/float(numberOfOccurencesInThisHour)

		writer.writerow([convertedDatetime,meanNumberOfProcesses])
		print "Written: ", convertedDatetime, meanNumberOfProcesses

		lastYear = currentYear
		lastMonth = currentMonth
		lastDay = currentDay
		lastHour = currentHour
		lastMinute = currentMinute
		counter += 1
		numberOfProcesses = int(row[1])
		numberOfOccurencesInThisHour = 1

