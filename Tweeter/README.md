# Quantified Self: Tweet that!

A small Python script to tweet some information of my Quantified Self stuff (keypresses, mouseclicks atm) to a dedicated Twitter account ([@QuandiH](http://twitter.com/QuandiH)).

It uses Tweepy for Twitter and oursql for MySQL  communication.

It's really a bare script with no features at all. There could be much more error detection, e.g.

## Files
  * `quandih.py` — Takes care of the tweeting. It's called by a cronjob once per night.
  * `setup.py` — Small setup script to get your API keys after creating a new Twitter application on their website. Found somewhere in the Internets™.
  * `twitterkeys.dummy.py` — Put your twitter API stuff in here and rename to `twitterkeys.py`
  * `sqlInfo.dummy.py` — Put the necessary MySQL information to connect to your database into this file and rename it to `sqlInfo.py`.