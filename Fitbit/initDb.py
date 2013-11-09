import sqlite3 as sql
import sys, getopt

def main(argv):
	force = bool(False)
	opts, args = getopt.getopt(argv,"hf",["help", "force"])
	for opt, arg in opts:
		if opt in ("-f", "--force"):
			force = True
		if opt in ("-h", "--help"):
			print "-f   --force      Drops table of file fbData.db before recreating it."
			sys.exit()

	dbConnection = sql.connect('fbData.db')

	with dbConnection:
		dbCursor = dbConnection.cursor()
		if (force):
			dbCursor.execute("drop table if exists fitbitdata")
		dbCursor.execute("create table fitbitdata (date INT PRIMARY KEY, elevation REAL, sedentaryMinutes INT, lightlyActiveMinutes INT, caloriesOut INT, caloriesBMR INT, marginalCalories INT, fairlyActiveMinutes INT, veryActiveMinutes INT, activityCalories INT, steps INT, floors INT, activeScore INT)")




if __name__ == "__main__":
   main(sys.argv[1:])
