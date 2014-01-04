import oursql
import sqlKeys
from mySqlHandler import mySqlHandler
import sys, getopt


def main(argv):
	fbTableName = 'Fitbit'
	handler = mySqlHandler(sqlKeys, tableName=fbTableName)

	handler.cur.execute("CREATE TABLE " + fbTableName + " (date INT, PRIMARY KEY(date), elevation FLOAT, sedentaryMinutes INT, lightlyActiveMinutes INT, caloriesOut INT, caloriesBMR INT, marginalCalories INT, fairlyActiveMinutes INT, veryActiveMinutes INT, activityCalories INT, steps INT, floors INT, activeScore INT)")

if __name__ == "__main__":
   main(sys.argv)
