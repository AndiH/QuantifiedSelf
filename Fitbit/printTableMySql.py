#!/usr/bin/env python
# Usage: printTableMySql.py Fitbit
from mySqlHandler import mySqlHandler
import argparse
import time
import sqlKeys

parser = argparse.ArgumentParser(description='Prints * from a table of a MySql db')
parser.add_argument('t', metavar='TABLE', type=str, help='Name of the table to be printed')
args = parser.parse_args()
tableName = args.t

handler = mySqlHandler(sqlKeys, tableName=tableName)
handler.cur.execute("select * from " + tableName + " order by date DESC")
rows = handler.cur.fetchall()
for row in rows:
	print time.strftime('%d-%m-%Y', time.localtime(row[0])), row
