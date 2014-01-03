#!/usr/bin/env python
import sqlite3 as sql

dbConnection = sql.connect('gitCommits.db')
with dbConnection:
	dbCursor = dbConnection.cursor()
	# if (force):
	# 	dbCursor.execute("drop table if exists fitbitdata")
	dbCursor.execute("CREATE TABLE commits (hash TEXT PRIMARY KEY, date INT, message TEXT)")
