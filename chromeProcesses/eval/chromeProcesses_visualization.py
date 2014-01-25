#!/usr/bin/env python
############################
# File converts a cvs of time stamps and number of open chrome tabs into a scatter plot including a linear regression
# A. Herten, 18.10.2013
############################

import numpy as np #numerical stuff
import pylab as pl #for poly line fit
import sys, datetime #for converting to human readable date
# import matplotlib.pyplot as plt
import prettyplotlib as ppl # makes nicer colors and generally better to look at graphs
from prettyplotlib import plt # This is "import matplotlib.pyplot as plt" from the prettyplotlib library
from prettyplotlib import mpl # This is "import matplotlib as mpl" from the prettyplotlib library

# small function to convert epoch time to human readable format
def convertDate(date):
	# return datetime.datetime.fromtimestamp(date).strftime("%d.%m.%Y %H:00")
	return datetime.datetime.fromtimestamp(date).strftime("%d.%m.%Y")

def saveAllTheFiles(fig, name):
	fig.savefig(name + '.png', dpi=200, bbox_inches='tight')
	fig.savefig(name + '.pdf', dpi=200, bbox_inches='tight')
	fig.savefig(name + '.svg', dpi=200, bbox_inches='tight')

# change font to Open Sans (has some kerning issues, though)
mpl.rcParams.update({'font.family':'Open Sans'})

# get name of file to process
inputFileName = sys.argv[1]

# load csv file with EPOCHTIME;NOFPROCESSES
data = np.loadtxt(inputFileName, delimiter=";")

# Not all of the recorded chrome processes are actually proper tabs, some processes are workers only. Substract them here.
notActuallyChromeTabs = 15
data[:,1] = [int(x) - notActuallyChromeTabs for x in data[:,1]]

print "In average, you have open", np.average(data[:,1]), "Chrome tabs."


# create a list with the x ticks, which should be printed
startDate = data[:,0][0]
endDate = data[:,0][-1]
printList = range(int(startDate), int(endDate), 2000000)

# convert epoch times (x ticks) to human readable form
humanName = []
for i in printList:
	humanName.append(convertDate(i))
	# print convertDate(i)

# fit a pol1 through the values and make a 1d function of it
fit = pl.polyfit(data[:,0], data[:,1], 1)
# print fit[0]
fitfn = pl.poly1d(fit)

# plot stuff
#   first plot the scatter plot with all the values (for this, use prettyplotlib)
#   superimpose the linear regression on top
#   finally, change the number of shown x ticks to the one we specified before and change their labels to dates of human readable form

# fig, ax = plt.subplots(figsize=(14,8)) #shorthand
fig = plt.figure(figsize=(14,8))
ax = fig.add_subplot(111)
ppl.scatter(ax, data[:,0], data[:,1], label="#Tabs") # used prettyplotlib to plot, if not uses, use sx.scatter and remove ax as the first argument
ppl.plot(ax, data[:,0], fitfn(data[:,0]), label="Fit (m="+str(round(fit[0],8))+")")
ax.set_xticks(printList)
ax.set_xticklabels(humanName);
ax.axis('tight')
ppl.legend(ax, loc=4)
ax.set_ylim(0, 78)

saveAllTheFiles(fig, "processesVsTime")


### CUT
xMaxCut = 1390417683
cutData = np.asarray([[x,y] for x,y in zip(data[:,0], data[:,1]) if x < xMaxCut])
cutFig = plt.figure(figsize=(14,8))
cutAx = cutFig.add_subplot(111)
ppl.scatter(cutAx, cutData[:,0], cutData[:,1], label="#Tabs")
ppl.plot(cutAx, cutData[:,0], fitfn(cutData[:,0]), label="Fit (m="+str(round(fit[0],8))+")")
cutAx.set_xticks(printList)
cutAx.set_xticklabels(humanName)
cutAx.axis('tight')
ppl.legend(cutAx, loc=4)
cutAx.set_ylim(40, 78)

saveAllTheFiles(cutFig, "processesVsTime--cut")


### ZOOM
xMin = 1.3851*10**9
xMax = 1.38515*10**9
zoomData = np.asarray([[x,y] for x,y in zip(data[:,0], data[:,1]) if x > xMin and x < xMax])

zoomPrintlist = range(int(xMin), int(xMax), 8000)
zoomHumanName = [datetime.datetime.fromtimestamp(x).strftime("%d.%m.%Y %H:%M") for x in zoomPrintlist]
zoomFig = plt.figure(figsize=(14,8))
zoomAx = zoomFig.add_subplot(111)
ppl.scatter(zoomAx, zoomData[:,0], zoomData[:,1], label="#Tabs")
zoomAx.set_xticks(zoomPrintlist)
zoomAx.set_xticklabels(zoomHumanName)
zoomAx.axis('tight')
ppl.legend(zoomAx, loc=4)

saveAllTheFiles(zoomFig, "processesVsTime--zoom")

# plt.show()
