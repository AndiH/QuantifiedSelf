# Quantified Self: Liberate Fitbit data

These Python scripts connectes to the Fitbit API, retrieves yesterdays data and saves it into a sqlite database.

It's work in progress and at the date of writing this readme just a proof on concept.

## Files
  * `initDb.py` — Initializes the database file. Use flag `-f` to force a `drop table` before creating the table skeleton. For flushing your database.
  * `anafitbit.py` — Connects to Fitbit, retrieves yesterdays information, reformats it and writes the data into a sqlite database.
  * `keys.py` — **NOT COMMITTED** File providing costumer key and secret as well as user key and secret.
