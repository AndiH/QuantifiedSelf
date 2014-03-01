#!/usr/bin/env python
import sqlite3 as sql
import sys
import oursql
# import sqlInfo
import argparse

class sqliteToMySql():
	"""Will open a local SQLite3 database and synchronize the latest 50 entries with a remote MySQL database"""
	def __init__(self, sqlite_pathToDb, sqlite_tableName, mysql_host, mysql_user, mysql_password, mysql_db, mysql_tableName, cellsToSynchronize, initialize = False):
		self.initialize = initialize
		self.sqlite_pathToDb = sqlite_pathToDb
		self.sqlite_tableName = sqlite_tableName 
		self.mysql_host = mysql_host
		self.mysql_user = mysql_user
		self.mysql_password = mysql_password
		self.mysql_db = mysql_db
		self.mysql_tableName = mysql_tableName
		self.cellsToSynchronize = cellsToSynchronize
	def readFromSqlite(self):
		con = None
		rows = None
		try:
			con = sql.connect(self.sqlite_pathToDb)
			cur = con.cursor()
			selectionstring = "SELECT * FROM " + self.sqlite_tableName + " ORDER BY `date`"
			if not (self.initialize):
				selectionstring += " DESC LIMIT 50"
			cur.execute(selectionstring)
			con.commit()
			rows = cur.fetchall()

		except sql.Error, e:
			print "Error %s:" % e.args[0]
			sys.exit(1)

		finally:
			if con:
				con.close()
			return rows
	def writeToMysqlDb(self, rows):
		con = None
		try:
			db_connection = oursql.connect(host=self.mysql_host, user=self.mysql_user, passwd=self.mysql_password, db=self.mysql_db)
			cur = db_connection.cursor()
			for row in rows:
				doublerow = row + row
				# print doublerow
				executionString = 'INSERT INTO ' + self.mysql_tableName + ' (' + ', '.join(self.cellsToSynchronize) + ') VALUES ('+ ', '.join(['?' for element in self.cellsToSynchronize]) + ') ON DUPLICATE KEY UPDATE ' + '=?, '.join(self.cellsToSynchronize) + '=?'
				# print executionString
				cur.execute(executionString , doublerow)
		finally:
			if con:
				con.close()
	def main(self):
		rows = self.readFromSqlite()
		self.writeToMysqlDb(rows)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Synchronizes the last 50 rows of a (local) SQLite database with a (remote) MySQL database. The 50 can be overridden.')
	parser.add_argument('--initialize', action='store_true', help="Does not only use first 50 entries of the SQLite database but synchronizes every row of the database. Use this to initialize a new remote database.")
	parser.add_argument('--sqlite-path', type=str, help="Complete path to the SQLite db")
	parser.add_argument('--sqlite-table', type=str, help="SQLite table name")
	parser.add_argument('--mysql-host', type=str, help="MySQL hostname")
	parser.add_argument('--mysql-user', type=str, help="MySQL username")
	parser.add_argument('--mysql-password', type=str, help="MySQL password")
	parser.add_argument('--mysql-db', type=str, help="MySQL database name")
	parser.add_argument('--mysql-table', type=str, help="MySQL table name")
	parser.add_argument('--cells', type=list, help="List of cells to synchronize")
	args = parser.parse_args()

	pusher = sqliteToMySql(args.sqlite_path, args.sqlite_table, args.mysql_host, args.mysql_user, args.mysql_password, args.mysql_db, args.mysql_table, args.cells, args.initialize)
	pusher.main()
