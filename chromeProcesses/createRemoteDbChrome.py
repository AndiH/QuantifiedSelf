import sys
sys.path.append('../common')
import createRemoteDb

tableName = 'Chrome'
cells = ["date INT", "PRIMARY KEY(date)", "processes INT"]

remote = createRemoteDb.createRemoteDb(tableName, cells)
