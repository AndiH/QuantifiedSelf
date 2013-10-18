#!/bin/bash
# Will print to amount of currently running chrome processes to a file
# Run every 5 minutes via cronjob a lá */5 * * * * ./Users/Andi/Desktop/countChrome.sh
# Or, better on OS X, use launchd
# 
# 29.8.2013 Andreas Herten http://www.andreasherten.de/

PATH=/usr/local/bin:/usr/bin:/bin

NUMBEROFCHROMEPROCESSES=$(pgrep -i Chrome | wc -l | sed 's/^ *//g')
TODAY=$(date +"%s") # Instead of %s epoch time, an older version of this file had here Y-%m-%d %H:%M:%S. Not a good idea.

OUTPUTFILE="chromeProcesses.csv"
ABSOLUTEDIR="/Users/Andi/Desktop"

echo "$TODAY"";""$NUMBEROFCHROMEPROCESSES">>$ABSOLUTEDIR/$OUTPUTFILE
