#!/usr/bin/env python
import sys, datetime, calendar
import numpy as np
import oursql

from itertools import cycle
import colorsys

import prettyplotlib as ppl # makes nicer colors and generally better to look at graphs
import matplotlib.pyplot as plt
import matplotlib as mpl
from prettyplotlib import brewer2mpl

sys.path.append("..")
import sqlInfo

def saveAllTheFiles(fig, name):
	fig.savefig(name + '.png', dpi=200, bbox_inches='tight')
	fig.savefig(name + '.pdf', dpi=200, bbox_inches='tight')
	fig.savefig(name + '.svg', dpi=200, bbox_inches='tight')



db_connection = oursql.connect(host=sqlInfo.host, user=sqlInfo.user, passwd=sqlInfo.password, db=sqlInfo.database)
cur = db_connection.cursor()
cur.execute("select * from Fitbit order by date ASC")
rows = cur.fetchall()

allTheData = []
dates = []
steps = []
floors = []
allImportantData = []
for row in rows:
	allTheData.append(row)
	dates.append(row[0])
	steps.append(row[-3])
	floors.append(row[-2])
	allImportantData.append([row[0], row[-3], row[-2]])

cur.close()
db_connection.close()

data = np.asarray(allImportantData)

color_cycle = cycle(mpl.rcParams['axes.color_cycle'])

x = data[:,0]
fig = plt.figure(figsize=(14,8))
ax = fig.add_subplot(111)
# fig, ax = plt.subplots()
# ax.axis('tight')
currentColor = next(color_cycle)
_tempColor = colorsys.rgb_to_hsv(currentColor[0], currentColor[1], currentColor[2])
currentMarkerColor = colorsys.hsv_to_rgb(_tempColor[0], _tempColor[1], _tempColor[2]/2)
ppl.plot(ax, x, data[:,1], label="#Stepss", color=currentColor) 
# ax.plot(x, data[:,1], label="#Stepss", color="b") 
ax.set_xlabel("Date")
ax.set_ylabel("Steps", color=currentMarkerColor)
for tick in ax.get_yticklabels():
	tick.set_color(currentMarkerColor)
# ppl.bar(ax, x, data[:,1], grid='y')
startDate = x[0]
endDate = x[-1]
printList = range(int(startDate), int(endDate), 2000000)
ax.set_xticks(printList)
ax.set_xticklabels([datetime.datetime.fromtimestamp(date).strftime("%d.%m.%Y") for date in printList])
fig.autofmt_xdate()
 
currentColor = next(color_cycle)
_tempColor = colorsys.rgb_to_hsv(currentColor[0], currentColor[1], currentColor[2])
currentMarkerColor = colorsys.hsv_to_rgb(_tempColor[0], _tempColor[1], _tempColor[2]/2)
ax2 = ax.twinx()
# ax2.plot(x, data[:,2], label="#Floors", color="red")
ppl.plot(ax2, x, data[:,2], label="#Floors", color=currentColor)
ax2.set_ylabel("Floors", color=currentMarkerColor)
for tick in ax2.get_yticklabels():
	tick.set_color(currentMarkerColor)

saveAllTheFiles(fig, "fitbit")

### Statistics PER WEEKDAY
# 
# 
weekdaySteps = {}
weekdayFloors = {}
for entry in data:
	date = datetime.datetime.fromtimestamp(entry[0])
	weekday = calendar.weekday(date.year, date.month, date.day)
	if (weekday not in weekdaySteps.keys()):
		weekdaySteps[weekday] = []
	weekdaySteps[weekday].append(entry[1])
	if (weekday not in weekdayFloors.keys()):
		weekdayFloors[weekday] = []
	weekdayFloors[weekday].append(entry[2])

reformattedData = np.asarray([[weekdaySteps[firstThing][secondThing] for firstThing in range(7)] for secondThing in range(51)])

xLabels = ["Mondays", "Tuesdays", "Wednesdays", "Thursdays", "Fridays", "Saturdays", "Sundays"]

fig2 = plt.figure(figsize=(14,8))
ax2 = fig2.add_subplot(111)

ppl.boxplot(ax2, reformattedData, xticklabels=xLabels)
# ax2.xaxis.set_ticklabels(xLabels)
saveAllTheFiles(fig2, "fitbit-per_weekday--boxplot")

averages = [np.average(weekdaySteps[day]) for day in weekdaySteps] # np.std(weekdaySteps[0])
stdDeviations = [np.std(weekdaySteps[day]) for day in weekdaySteps]
currentColor = next(color_cycle)
currentColor = next(color_cycle)
fig3 = plt.figure(figsize=(14,8))
ax3 = fig3.add_subplot(111)
ax3.errorbar(range(1,8), averages, yerr=stdDeviations, color=currentColor, fmt='o', markeredgecolor=currentColor, elinewidth=1)
ax3.xaxis.set_ticks(range(1,8))
ax3.xaxis.set_ticklabels(xLabels)
ax3.set_xlim(left=0.5, right=7.5)
ax3.set_ylim(bottom=0, top=35000)
saveAllTheFiles(fig3, "fitbit-per_weekday--mean")

ax2.errorbar(range(1,8), averages, yerr=stdDeviations, color=currentColor, fmt='o', markeredgecolor=currentColor, elinewidth=2)
saveAllTheFiles(fig2, "fitbit-per_weekday--boxplot_and_mean")


#### Statistics per WEEK
#
weekSteps = {}
for entry in data:
	date = datetime.datetime.fromtimestamp(entry[0])
	week = date.isocalendar()
	_week = "0" + str(week[1]) if week[1] < 10 else week[1]
	formattedWeek = str(week[0]) + "-" + str(_week)
	if (formattedWeek not in weekSteps.keys()):
		weekSteps[formattedWeek] = []
	weekSteps[formattedWeek].append(entry[1])

# print weekSteps
reducedWeekSteps = sorted([[day, sum(weekSteps[day])] for day in weekSteps])
reducedWeekSteps_dates = [firstEntry[0] for firstEntry in reducedWeekSteps]
reducedWeekSteps_steps = [firstEntry[1] for firstEntry in reducedWeekSteps]

lastYear = "2012"
reducedWeekSteps_dates_light = []
for dates in reducedWeekSteps_dates:
	# if lastYear in dates:
	# 	newDate = str(dates[-2]) + str(dates[-1])
	# else:
	# 	newDate = str(dates)
	# 	lastYear = str(dates[0:4])
	newDate = str(dates[-2]) + str(dates[-1])
	reducedWeekSteps_dates_light.append(newDate)

fig4 = plt.figure(figsize=(16,8))
ax4 = fig4.add_subplot(111)

currentColor = next(color_cycle)

ppl.bar(ax4, range(len(reducedWeekSteps_steps)), reducedWeekSteps_steps, xticklabels=reducedWeekSteps_dates_light, grid='y', color=currentColor) #,annotate=True

ax4.axis('tight')
ax4.set_xlim(left=0, right=53)
ax4.set_ylim(bottom=0, top=140000)
ax4.set_ylabel("Steps")
ax4.set_xlabel("Week Number")
# ax4.xaxis.set_ticklabels(reducedWeekSteps_dates_light, rotation=33)

saveAllTheFiles(fig4, "fitbit-per_week")
# plt.show()

