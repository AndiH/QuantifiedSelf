import psutil
import sqlite3 as sql
import datetime
import sys

def getPathToDB():
  return '/Users/Andi/Documents/Coding/QuantifiedSelf/chromeProcesses/chromeProcesses.db'

def getChromeProcesses():
	chromeOffSet = 13
	nOfChromeProcesses = 0

	for process in psutil.process_iter():
		if 'Chrome' in process.name:
			nOfChromeProcesses += 1

	return nOfChromeProcesses - chromeOffSet

def saveToDatabase():
	con = None
	try:
		con = sql.connect(getPathToDB())
		cur = con.cursor()
		cur.execute("INSERT OR REPLACE INTO chrome VALUES (?,?)", (datetime.datetime.now().strftime("%s"),getChromeProcesses()))

		con.commit()

	except sql.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)

	finally:
		if con:
			con.close()

if __name__ == '__main__':
	saveToDatabase()
