#!/usr/bin/env python
# Simple script that takes info from Whatpulse's SQLite3 database and posts it to my own (remote) MySQL server
import keys as keys
from readFromWhatPulseDb import readFromWhatPulseDb
from mySqlHandler import mySqlHandler

data = readFromWhatPulseDb().returnData() # Read all data from Whatpulse's SQLite3

# print data # Check how the data looks

sql = mySqlHandler(keys) # Initialize MySQL connection

for entry in data:
	sql.insertArrayIntoDb(entry) # Update MySQL db row-wise

# sql.readFromDb() # Print data as it is in MySQL db. For debug
