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
fails = []
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
            fails.append(0)
            date = None
        continue
    elif "Command running too long, killing it." in line:
        if date:
            dates.append(mdates.date2num(date))
            times.append(1)
            fails.append(mdates.date2num(date))

    print "Junk: " + line,
    time = None
    date = None

df = pd.DataFrame({'date': dates, 'runtime': times, 'fail': fails})
df2 = df[df.fail != 0]
print df2
print(type(df2.fail))
fig, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.set_xlim(dates[0]-1, dates[len(dates)-1]+1)
ax1.set_ylim(20,60)
ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m.%d %H:%M'))
#sns.tsplot(data=df.runtime, time=df.date, ax=ax, interpolate=False)
sns.regplot('date', 'runtime', df, ax=ax1)
#sns.regplot('date', 'fail', df2, ax=ax2)

bins = int(dates[len(dates)-1] - dates[0])
print(bins)
sns.distplot(df2.fail, bins=bins, kde=False, rug=True, ax=ax2);
#sns.regplot('date', 'fail', df, ax=ax2)
ax2.set_ylabel('# Failures')
ax1.set_xlabel('Date')
ax2.set_xlabel('Date')
ax1.set_ylabel('Runtime (s)')
plt.suptitle("Trollduction Image Rebuild")
# assign locator and formatter for the xaxis ticks.

# put the labels at 45deg since they tend to be too long
fig.autofmt_xdate()

plt.show()
