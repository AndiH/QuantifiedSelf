# Quantified Self: Typingstats

Typingstats is an AppStore Tool for monitoring your keystrokes.

It saves its data to
```
~/Library/Containers/com.jabwd.Typingstats/Data/Library/Application\ Support/Typingstats/keypresses.db
```
as a sqlite3 database.

From this file I extracted with Navicat the table `keyPresses` into a csv file (my Python sqlite3 module seems to be broken).

The Python scripts in this repository work on this `keyPresses.csv` file.

## File Descriptions

  * `keyPressesPerDay.py` — Reads in the raw `keyPresses.csv` and prints out a file containing the amount of key presses per day (*who would have thought…*).
  * `keyHeatmap.py` — Reads in a file (e.g. `keyPresses.csv`) and converts it into a heatmap (which key was hit how many times?). The result is printed into `INPUTFILE_processed.csv`.
  * `keyHeatmap_visulization.py` — A first test of trying to visualize the previously generated heatmap.csv. Not ready yet, though.
  * `mapKeyIDKeyName.csv` — A list of Typingstats' key IDs and corresponding key names. Not yet implemented into a Python file, though. 

## Todos

  * Fix sqlite3 plugin for Python or write something in PHP to extract the database to `csv`
  * Make automatical match between name of key and `keyID` by means of `mapKeyIDKeyName.csv`
  * Extract different, more interesting information
  * Plot information with matplotlib / ppl, e.g. as a [bar plot](https://github.com/olgabot/prettyplotlib/wiki/Examples-with-code#bar-with-each-bar-labeled-on-x-axis)
