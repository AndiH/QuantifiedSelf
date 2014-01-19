#!/usr/bin/env python
import sqlite3 as sql
import argparse

parser = argparse.ArgumentParser(description='Initializes the local database for Git commits.')
parser.add_argument('--dropDB', action='store_true', help='drop the database if it already exists')
args = parser.parse_args()

dbConnection = sql.connect('gitCommits.db')
with dbConnection:
	dbCursor = dbConnection.cursor()
	if args.dropDB:
		dbCursor.execute("DROP TABLE IF EXISTS commits")
	dbCursor.execute("CREATE TABLE commits (hash TEXT PRIMARY KEY, date INT, message TEXT, filesAdded TEXT, filesChanged TEXT, filesDeleted TEXT, linesAdded INT, linesDeleted INT, repo TEXT, pc TEXT)")

