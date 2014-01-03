#!/usr/bin/env python
import sqlite3 as sql
import argparse
import datetime

def updateDb(args):
	date = args.date
	hashValue = args.hash
	commitMessage = args.message

	if (-1 == date):
		date = datetime.datetime.now()
	else:
		date = datetime.datetime.fromtimestamp(date)

	print date, hashValue, commitMessage
	dbConnection = sql.connect('gitCommits.db')
	with dbConnection:
		dbCursor = dbConnection.cursor()
		dbCursor.execute("INSERT INTO commits VALUES (?,?,?)", (hashValue, date.strftime("%s"),commitMessage))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Update local SQLite3 DB with commit')
	parser.add_argument('hash', metavar='HASH', type=str, help='Hash value of commit')
	parser.add_argument('-d', '--date', default=-1, type=int, help='Date of commit')
	parser.add_argument('-msg', '--message', default='Lorem', help='Commit message')
	args = parser.parse_args()
	updateDb(args)
