# Quantified Self: Liberate Fitbit data

This Python scripts connect to the Fitbit API, retrieve the results to a given date and save the repsonse into a MySQL database. (Old version: SQLite 3 db. If you're interested in that, check backlog of this repo prior to Jan 2014.)

It's the backend powering http://quantified.andreasherten.de/.

It's work in progress and subject to a lot of changes. 

## Files
  * `initDbMySql.py` — Initializes the database file.
  * `updateFitbitDb.py` — Provides a class to connect to the Fitbit API (by means of Python's Fitbit package) and retrieve the data of a given day into a MySQL database.
  * `fitbitKeys.dummy.json` — Dummy example file for storage of all keys related to the Fitbit API.
  * `anafitbit.py` — Uses `updateFitbitDb.py` to retrieve the last 10 days of Fitbit data.
  * `fbHist.py` — Updates a table with historical Fitbit data. Check -h for parameters. Minimal parameters: One argument for a month of 2013 to retrieve completely, e.g. `python fbHist.py 10`. *Note Fitbit API rate limits (150 call/hour)*
  * `printTableMySql.py` — Prints * from a MySQL table. Check -h for parameters.
