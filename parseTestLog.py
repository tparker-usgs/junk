#!/usr/bin/env python
import re
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import numpy as np

date = None
f = open('testbuild.log.bak', 'r')
date_pattern = re.compile('.* UTC 2017')
time_pattern = re.compile('(\d{2})m(\d\d?\.\d*)s$')

#Date line: Tue Jul 11 18:00:01 UTC 2017

dates = []
times = []
for line in f:
    m = date_pattern.match(line)
    if m:
        date = datetime.strptime(line, '%a %b %d %H:%M:%S UTC %Y\n')
        print "Date line: " + line,
        print "Date: " + str(date)
        continue

    m = time_pattern.match(line)
    if m:
        time = float(m.group(2))
        time += float(m.group(1)) * 60
        time /= 60
        if date:
            dates.append(mdates.date2num(date))
            times.append(time)
            date = None
        continue

    print "Junk: " + line,
    time = None
    date = None

df = pd.DataFrame({'date': dates, 'runtime': times})
print df
fig, ax = plt.subplots()
ax.set_xlim(dates[0]-1, dates[len(dates)-1]+1)
ax.set_ylim(20,60)
#sns.tsplot(data=df.runtime, time=df.date, ax=ax, interpolate=False)
sns.regplot('date', 'runtime', df, ax=ax)
# assign locator and formatter for the xaxis ticks.
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m.%d %H:%M'))

# put the labels at 45deg since they tend to be too long
fig.autofmt_xdate()
plt.show()
