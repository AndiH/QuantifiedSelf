#!/usr/bin/env python
import sys, argparse
sys.path.append('../common')
import sqlInfo
import sqliteToMySql

parser = argparse.ArgumentParser(description='Synchronizes the last 50 rows of the local Chrome Processes SQLite database with the remote MySQL one.')
parser.add_argument('--initialize', action='store_true', help="Does not only use first 50 entries of the SQLite database but synchronizes every row of the database. Use this to initialize a new remote database.")
args = parser.parse_args()

sqlite_path = "/Users/Andi/Documents/Coding/QuantifiedSelf/chromeProcesses/chromeProcesses.db"
sqlite_tablename = "chrome"

mysql_host = sqlInfo.host
mysql_user = sqlInfo.user
mysql_password = sqlInfo.password
mysql_db = sqlInfo.database
mysql_tablename = "Chrome"
initialize = args.initialize

cellsToSynchronize = ["date", "processes"]

syncer = sqliteToMySql.sqliteToMySql(sqlite_path, sqlite_tablename, mysql_host, mysql_user, mysql_password, mysql_db, mysql_tablename, cellsToSynchronize, initialize)
syncer.main()
