import psutil
import sqlite3 as sql
import datetime
import sys

def getPathToDB():
  return '/Users/Andi/Documents/Coding/QuantifiedSelf/chromeProcesses/chromeProcesses.db'

def getChromeProcessesOld(): # The way it was done before... subtracting a fixed threshold is wrong, though
	chromeOffSet = 13
	nOfChromeProcesses = 0

	for process in psutil.process_iter():
		if 'Chrome' in process.name:
			nOfChromeProcesses += 1

	print nOfChromeProcesses
	return nOfChromeProcesses - chromeOffSet

def getChromeProcessesProper():
	nOfChromeProcesses = 0
	for process in psutil.process_iter():
		if ('Chrome Helper' in process.name) and (len(process.cmdline) > 1):
			if ("--type=renderer" in process.cmdline) and not ("--extension-process" in process.cmdline): # Thx to Axel Rauschmayer for this criterion http://www.2ality.com/2013/09/osx-kill-chrome-tabs.html
				nOfChromeProcesses += 1
	return nOfChromeProcesses

def saveToDatabase():
	con = None
	try:
		con = sql.connect(getPathToDB())
		cur = con.cursor()
		cur.execute("INSERT OR REPLACE INTO chrome VALUES (?,?)", (datetime.datetime.now().strftime("%s"),getChromeProcessesProper()))

		con.commit()

	except sql.Error, e:
		print "Error %s:" % e.args[0]
		sys.exit(1)

	finally:
		if con:
			con.close()

if __name__ == '__main__':
	saveToDatabase()
