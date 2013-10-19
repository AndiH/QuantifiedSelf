# reads in raw csv with key presses per timestamp and converts it into a heatmap (presses per key) for a given timespan

import csv, sys
# import datetime

inputFileName = sys.argv[1] # keyPresses.csv

# outputFileName = inputFileName[:-4] + '_processed.csv'
outputfileName = 'keyPresses_Heatmap.csv'
outputfile = open(outputfileName, 'wb')
writer = csv.writer(outputfile, delimiter=";") # semicolon because of stupid German localization of Numbers.app

with open(inputFileName, 'rb') as inputfile:
	reader = csv.reader(inputfile)
	startingDate = 1377986400
	endingDate = 1380492000
	heatmap = dict()
	for row in reader:
		if (int(row[1]) >= 1377986400 and int(row[1]) <= 1380492000 ):
			if (int(row[2]) in heatmap):
				heatmap[int(row[2])] += int(row[3])
			else: # no such key in dictionary
				heatmap[int(row[2])] = int(row[3])
	for key in heatmap:
		writer.writerow([key, heatmap[key]])
print "Sucessfully written to", outputfileName
