import csv
import datetime

rownum = 0
keystrokes = int(0)


outputfileName = 'keyPresses_PressesPerDay.csv'
outputfile = open(outputfileName, 'wb')
writer = csv.writer(outputfile, delimiter=';') # delimiter needs to be semicolon since I'm in Germany and a comma is a decimal separator there (and Numbers.app cares about that in the csv file, doh)

with open('keyPresses.csv', 'rb') as inputfile:
    reader = csv.reader(inputfile)
    for row in reader:
        # print row

    	currentdate = row[1]
    	if (rownum == 0):
    		previousdate = row[1]
    		rownum = 1

        if (currentdate == previousdate):
        	keystrokes += int(row[3])
        else:
        	readableDate = datetime.datetime.fromtimestamp(int(currentdate)-1).strftime('%Y-%m-%d')
        	writer.writerow([readableDate,keystrokes])
        	keystrokes = int(row[3])
        previousdate = currentdate
    print("Successfully written to %s" % outputfileName)