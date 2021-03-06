import sqlite3 as sql
import argparse
import time

parser = argparse.ArgumentParser(description='Prints * from table of SQLite3 db file')
parser.add_argument('db', metavar='DBFILE', type=str, help='Name of the SQLite3 db file')
parser.add_argument('t', metavar='TABLE', type=str, help='Name of the table to be printed')
args = parser.parse_args()

dbConnection = sql.connect(args.db)
with dbConnection:
	dbCursor = dbConnection.cursor()
	dbCursor.execute("select * from " + args.t + " order by date DESC")
	rows = dbCursor.fetchall()
for row in rows:
	print time.strftime('%d-%m-%Y', time.localtime(row[0])), row
