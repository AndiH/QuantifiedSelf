import oursql
import sqlInfo
import sys


def main(argv):
	tableName = 'Commits'
	db_connection = oursql.connect(host=sqlInfo.host, user=sqlInfo.user, passwd=sqlInfo.password, db=sqlInfo.database)
	cur = db_connection.cursor()

	cur.execute("CREATE TABLE " + tableName + " (hash CHAR(40), PRIMARY KEY(hash), date INT, message TEXT, filesAdded TEXT, filesChanged TEXT, filesDeleted TEXT, linesAdded INT, linesDeleted INT, repo TEXT, pc TEXT)")

if __name__ == "__main__":
   main(sys.argv)
