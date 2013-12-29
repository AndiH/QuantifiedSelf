# Quantified Self: Whatpulse Computer Input

These Python scripts transfer the data stored in your local [Whatpulse](http://whatpulse.org/) SQLite3 db to a MySQL db on your (my ;)) server. Data tackled at the moment: Key presses and mouse clicks.

`updateSqlDbWithWhatpulseInfo.py` is run every hour on my local machine to push data into a remote MySQL database. The result is then displayed on a website.

For the time being, displayed the temporary testing site [quantified.andreasherten.de/keys.php](quantified.andreasherten.de/keys.php).

## Files
  * `readFromWhatPulseDb.py` — Provides a class to read the data (key presses, mouse clicks) from Whatpulse's SQLite 3 database. `returnData()` returns a list of (data, keypresses, mouseclicks). If called directly from the shell, `readFromWhatPulseDb.py` displays the content of Whatpulse's database (`printData()` method).
  * `writeToMySqlDb.py` — Provides a class to update a (*my*) MySQL database with Whatpulse's data. [Oursql](https://pypi.python.org/pypi/oursql) is used. Method `insertArrayIntoDb()` takes care of inserting into the database (updating presses and clicks, if current processed date exists already); `readFromDb()` provides a method to retrieve the content of the database (for debug stuff). **Note**: The necessary `keys.py` to be provided as the `keyFile` initialization argument is not included in this repository. Syntax should be self-explanatory, though.
  * `updateSqlDbWithWhatpulseInfo.py.py` — Wraps the two previous files together: Reads Whatpules database and writes stuff to my MySQL database. This file is called every hour by the launchctl thingy.

## Todo
  * Tidy up code
  * Make more abstract classes to be used in the other QS sub-projects
  * Get the other QS sub-projects running on MySQL
  * Don't always update ALL dates, limit operation to last 3 days
