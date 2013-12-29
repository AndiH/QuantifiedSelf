#!/usr/bin/env python
# Simple script that takes info from Whatpulse's SQLite3 database and posts it to my own (remote) MySQL server
import keys as keys
from readFromWhatPulseDb import readFromWhatPulseDb
from writeToMySqlDb import writeToMySqlDb

data = readFromWhatPulseDb().returnData() # Read all data from Whatpulse's SQLite3

# print data # Check how the data looks

writer = writeToMySqlDb(keys) # Initialize MySQL connection

for entry in data:
	writer.insertArrayIntoDb(entry) # Update MySQL db row-wise

# writer.readFromDb() # Print data as it is in MySQL db. For debug
