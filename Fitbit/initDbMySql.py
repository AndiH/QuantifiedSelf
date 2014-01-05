import oursql
import sqlInfo
import sys


def main(argv):
	fbTableName = 'Fitbit'
	db_connection = oursql.connect(host=sqlInfo.host, user=sqlInfo.user, passwd=sqlInfo.password, db=sqlInfo.database)
	cur = db_connection.cursor()

	cur.execute("CREATE TABLE " + fbTableName + " (date INT, PRIMARY KEY(date), elevation FLOAT, sedentaryMinutes INT, lightlyActiveMinutes INT, caloriesOut INT, caloriesBMR INT, marginalCalories INT, fairlyActiveMinutes INT, veryActiveMinutes INT, activityCalories INT, steps INT, floors INT, activeScore INT)")

if __name__ == "__main__":
   main(sys.argv)
