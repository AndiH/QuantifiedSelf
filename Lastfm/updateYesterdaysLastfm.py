import datetime
import pylast, oursql
import lastfmKeys, sqlInfo

tableName = "LastfmLIGHT"
yourUsername = "iCai"

network = pylast.LastFMNetwork(api_key = lastfmKeys.key, api_secret = lastfmKeys.secret)
user = network.get_user(yourUsername)
nOfPlays = user.get_playcount()

db_connection = oursql.connect(host=sqlInfo.host, user=sqlInfo.user, passwd=sqlInfo.password, db=sqlInfo.database)
cur = db_connection.cursor()

yesterday = datetime.date.today() - datetime.timedelta(days=1)

data = (int(yesterday.strftime("%s")), nOfPlays, nOfPlays)

cur.execute('INSERT INTO ' + tableName + ' (date, totalplays) VALUES (?,?)' + ' ON DUPLICATE KEY UPDATE totalplays=?', data)

cur.close()
db_connection.close()
