#!/usr/bin/env python
import keys as keys
from readFromWhatPulseDb import readFromWhatPulseDb
from writeToMySqlDb import writeToMySqlDb

data = readFromWhatPulseDb().returnData()

print data

writer = writeToMySqlDb(keys)

for entry in data:
	writer.insertArrayIntoDb(entry)
	
writer.readFromDb()
