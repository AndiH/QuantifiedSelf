#!/usr/bin/env python
# Usage: printTableMySql.py Fitbit
import argparse
import time
import oursql
import sqlInfo

parser = argparse.ArgumentParser(description='Prints * from a table of a MySQL db')
parser.add_argument('-t', '--table', default='Fitbit', help='Name of SQL table name')
args = parser.parse_args()
tableName = args.table

db_connection = oursql.connect(host=sqlInfo.host, user=sqlInfo.user, passwd=sqlInfo.password, db=sqlInfo.database)
cur = db_connection.cursor()

cur.execute("select * from " + tableName + " order by date ASC")
rows = cur.fetchall()
for row in rows:
	print time.strftime('%d-%m-%Y', time.localtime(row[0])), row

cur.close()
db_connection.close()
