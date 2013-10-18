############################
# File converts human readable timestamps into epoch unix timestamps in a csv file with two rows (can easily be changed, though).
# A. Herten 18.10.2013
############################

import datetime, calendar, csv, sys

inputFileName = sys.argv[1]

outputFileName = inputFileName[:-4] + '_converted.csv'
outputfile = open(outputFileName, 'wb')
writer = csv.writer(outputfile, delimiter=';') # semicolon because of stupid German localization of Numbers.app

with open(inputFileName, 'rb') as inputfile:
	reader = csv.reader(inputfile, delimiter=';')
	for row in reader:
		firstCell = row[0]
		convertedFirstCell = calendar.timegm( datetime.datetime.strptime(firstCell,"%d.%m.%Y %H:%M").utctimetuple() )
		writer.writerow([convertedFirstCell,row[1]])
		# print convertedFirstCell, row[1]
print 'Used', inputFileName, 'to write', outputFileName
