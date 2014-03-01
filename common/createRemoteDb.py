import oursql
import sqlInfo
import sys
import argparse

class createRemoteDb(object):
	def __init__(self, tableName, cells, defaultCredentials = True):
		self.tableName = tableName
		self.cells = str(" (") + ", ".join(cells) + str(")")
		if (defaultCredentials):
			''' Pass your own set of sql connection details to override default stuff '''
			self.credentials = sqlInfo
		else:
			self.credentials = defaultCredentials
		self.main()
	def main(self):
		con = None
		cur = None
		try:
			con = oursql.connect(host=self.credentials.host, user=self.credentials.user, passwd=self.credentials.password, db=self.credentials.database)
			cur = con.cursor()
			cur.execute("CREATE TABLE " + self.tableName + self.cells)
		except oursql.Error, e:
			print "Error %s:" % e.args[0]
			sys.exit(1)
		finally:
			if con:
				con.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='File for creating a remote MySQL database.')
	parser.add_argument('--tablename', type=str, help="Name of the table to be created.")
	parser.add_argument('--cells', type=list, help="A list of strings of cell names and their data types.")
	args = parser.parse_args()
	creator = createRemoteDb(args.tablename, args.cells)
