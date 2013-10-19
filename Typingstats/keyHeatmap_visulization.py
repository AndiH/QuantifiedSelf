import numpy as np #numerical stuff
import pylab as pl #for poly line fit
import sys, datetime #for converting to human readable date
# import matplotlib.pyplot as plt
import prettyplotlib as ppl # makes nicer colors and generally better to look at graphs
from prettyplotlib import plt # This is "import matplotlib.pyplot as plt" from the prettyplotlib library
from prettyplotlib import mpl # This is "import matplotlib as mpl" from the prettyplotlib library


# change font to Open Sans (has some kerning issues, though)
# mpl.rcParams.update({'font.family':'Open Sans'})

# get name of file to process
inputFileName = sys.argv[1] # keyPresses_Heatmap.csv

# load csv file with EPOCHTIME;NOFPROCESSES
data = np.loadtxt(inputFileName, delimiter=";")
# data[:,1] = [x - notActuallyChromeTabs for x in data[:,1]]
# 
print data[:,0], data[:,1]

fig = plt.figure(figsize=(14,8))
ax = fig.add_subplot(111)
# ppl.bar(ax, data[:,0], data[:,1])
ax.bar(data[:,0], data[:,1])
# ax.axis('tight')

plt.show()


# xy = [(x_int[i],y_int[i]) for i in range(0,len(x_int))]
# xy_sorted = np.array(sorted(xy, key=lambda yz: yz[1], reverse=True))
# ax.bar(xy_sorted[:,0], xy_sorted[:,1])
