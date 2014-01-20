# Quantified Self: Lastfm Plays

This *preliminary* script saves the total number of tracks played by a specific user on Lastfm into a database.  
Taking a difference between two absolute play numbers, the number of played tracks at a given day can easily be retrieved.

I have some more planned for the future (see Todos below), but for the time being this is it. 


## Files
  * `createDb.py` — Creates a MySQL database somewhere. Package `oursql` is needed, as well as `sqlInfo.py` for the login info (see another folder of this QS repo for an example, e.g. /Fitbit/). *Not tested.*
  * `updateYesterdaysLastfm` – Updates the MySQL database with the Lastfm total plays as of the time of the script's execution. Uses the `pylast` package. An API key for the Lastfm API is needed, see next point.
  * `lastfmKeys.dummy.py` — API key and secret of Lastfm API.


## Todo
  * Save not only the play counts but the tracks into a database. This blows up everything, but shouldn't be too much. With this, faster evaluation of listening habits and other stuff are possible – without the need to call Lastfm for every bit.
