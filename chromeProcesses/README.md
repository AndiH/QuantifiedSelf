# Quantified Self: Count Chrome Tabs

These Python scripts do two things:
  1. Record the number of open Chrome tabs and save this number to a database
  2. Give you some visualizations of it.

## Recording Chrome Tabs
Since Chrome runs each tab in its own process, it's easy to find out the number of tabs. There are some helper processes, though, which have to be ommitted.
### Files
  * `createLocalDb.py` — Small script to initialize a local SQLite3 database for the Chrome processes.
  * `countChrome.py` — Python script to record Chrome processes. Saves into aforementioned database. Be sure to fix the absolute path to the database.
  * `com.andi.chromeCount.plist` — launchd plist file for calling `countChrome.py` every 5 minutes. I use Lingon 3 to manage that launchd entry, but with this plist file you should be able to get the cron job done manually.

## Processing & Visualizing Tabs
At first my plan was to create some graphs with Excel / Numbers / … from the dataset. When I imported the .csv it turned out that it had too many lines and slowed down the spreadsheet applications quite a lot. So I decided to create a small Python script which averages all entries of one hour to one single entry in a new file.  
Since I needed to learn Python (more properly) for that I was hooked after the first lines of code and decided to go a bit further: Do the whole postprocessing with Python.
### Files
  * *Outdated* `convertChromeProcessesTimestamp.py` — An old version of `countChrome.sh` did not save the UNIX epoch timestamp but a human readable date. This was not that clever of me, so this script converts human readable times again into epoch timestamps. You actually don't need it for anything here, it's just there for completeness.
  * `chromeProcesses.py` — Combines the output of `countChrome.sh` to entries for one hour, averaging over the tab counts within given hour (*rebin*, as we physicists say…).  
  I didn't end up using this script. It was intended to reduce the amount of data to a Excel-processable amount.
  * `chromeProcesses_visualization.py` — The **heart of this project**.  
  It imports the csv data, prints it as a scatter plot (by means of prettyprintplot ([olgabot/prettyplotlib](https://github.com/olgabot/prettyplotlib)) and mathplotlib) and adds a linear regression.  
  During plotting of these points, the number of Chrome processes are converted to tabs by reducing them by a factor of **15**, which empirically seems to be the amount of Chrome helper processes.  
  Call it with  
  ```python
  python chromeProcesses_visualization.py chromeProcesses_converted.csv
  ```  
  * `chromeProcesses_converted.csv` — The csv file with open Chrome processes, for reference.
  
### Can I Haz Picture plz?
![image](https://raw.github.com/AndiH/QuantifiedSelf/master/chromeProcesses/eval/processesVsTime.png)
