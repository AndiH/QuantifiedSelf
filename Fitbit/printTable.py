import sqlite3 as sql
import argparse

parser = argparse.ArgumentParser(description='Prints * from table of SQLite3 db file')
parser.add_argument('db', metavar='DBFILE', type=str, help='Name of the SQLite3 db file')
parser.add_argument('t', metavar='TABLE', type=str, help='Name of the table to be printed')
args = parser.parse_args()

dbConnection = sql.connect(args.db)
with dbConnection:
	dbCursor = dbConnection.cursor()
	dbCursor.execute("select * from " + args.t)
	rows = dbCursor.fetchall()
	for row in rows:
		print row
