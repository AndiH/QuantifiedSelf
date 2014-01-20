import oursql
import sqlInfo
import sys


def main(argv):
	fbTableName = 'LastfmLIGHT'
	db_connection = oursql.connect(host=sqlInfo.host, user=sqlInfo.user, passwd=sqlInfo.password, db=sqlInfo.database)
	cur = db_connection.cursor()

	cur.execute("CREATE TABLE IF NOT EXISTS " + fbTableName + " (date INT NOT NULL, PRIMARY KEY(date), totalplays INT)")

if __name__ == "__main__":
   main(sys.argv)
