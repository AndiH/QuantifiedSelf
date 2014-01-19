#!/usr/bin/env python
import sqlite3 as sql

dbConnection = sql.connect('gitCommits.db')
with dbConnection:
	dbCursor = dbConnection.cursor()
	dbCursor.execute("DROP TABLE IF EXISTS commits")
	dbCursor.execute("CREATE TABLE commits (hash TEXT PRIMARY KEY, date INT, message TEXT, filesAdded TEXT, filesChanged TEXT, filesDeleted TEXT, linesAdded INT, linesDeleted INT, repo TEXT, pc TEXT)")
