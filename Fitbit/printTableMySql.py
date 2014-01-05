#!/usr/bin/env python
# Usage: printTableMySql.py Fitbit
import argparse
import time
import sqlInfo
import oursql

parser = argparse.ArgumentParser(description='Prints * from a table of a MySql db')
parser.add_argument('t', metavar='TABLE', type=str, help='Name of the table to be printed')
args = parser.parse_args()
tableName = args.t

db_connection = oursql.connect(host=sqlInfo.host, user=sqlInfo.user, passwd=sqlInfo.password, db=sqlInfo.database)
cur = db_connection.cursor()

cur.execute("select * from " + tableName + " order by date DESC")
rows = cur.fetchall()
for row in rows:
	print time.strftime('%d-%m-%Y', time.localtime(row[0])), row

cur.close()
db_connection.close()
