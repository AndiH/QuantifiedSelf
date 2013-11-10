# Quantified Self: Liberate Fitbit data

This Python scripts connect to the Fitbit API, retrieve the results to a given date and save the repsonse into a SQLite 3 database.

It's the backend powering http://quantified.andreasherten.de/. The website-creating PHP file is also given in the `/site/` directory.

It's work in progress and subject to a lot of changes. Also, I'm too lazy to upload all Javascript and Webfont files for `/site`, this is going to happen when I streamlined the `index.php` a bit.

## Files
  * `initDb.py` — Initializes the database file. Use flag `-f` to force a `drop table` before creating the table skeleton. For flushing your database.
  * `updateFitbitDb.py` — Provides a class to connect to the Fitbit API (by means of Python's Fitbit package) and retrieve the data of a given day into a SQLite3 database.
  * `anafitbit.py` — Uses `updateFitbitDb.py` to retrieve the last 10 days of Fitbit data.
  * `keys.dummy.py` — Dummy twin file to my real `keys.py` to show you how the file has to look like. Your's should probably contain less `A`s…
  * `site/index.php` — The file powering http://quantified.andreasherten.de/. Quite messy and needs to be tidied up. To do. Also, all external files are not commited. It should just show you have the website is generated.
