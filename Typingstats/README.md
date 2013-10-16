# Quantified Self: Typingstats

Typingstats is an AppStore Tool for monitoring your keystrokes.

It saves its data to
```
~/Library/Containers/com.jabwd.Typingstats/Data/Library/Application\ Support/Typingstats/keypresses.db
```
as a sqlite3 database.

From this file I extracted with Navicat the table `keyPresses` into a csv file (my Python sqlite3 module seems to be broken).

On that file, the uploaded scripts here work.

In the numbers file, there's also a match between `keyID` and the name of the key.

## Todos

  * Fix sqlite3 plugin for Python or write something in PHP to extract the database to `csv`
  * Make automatical match between name of key and `keyID`
  * Extract different, more interesting information
