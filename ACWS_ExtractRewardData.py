#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 22:09:12 2020

@author: smith
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def countlist(frames):
    count=1
    retlist = []
    # Avoid IndexError for  random_list[i+1]
    for i in range(len(frames) - 1):
        # Check if the next number is consecutive
        if frames[i] + 1 == frames[i+1]:
            count += 1
        else:
            # If it is not append the count and restart counting
            retlist.append((round(frames[i]), count))
            count = 1
    # Since we stopped the loop one early append the last count
    retlist.append((round(frames[-1]), count))
    return retlist


directory = '/d1/studies/DLC_data/OperantDLC/CueVideos/predictions/'

df = pd.read_hdf('/home/smith/GA_DS/forked/ds_ga_41/project-final/C16_NP_2020-10-25DLC_resnet50_OperantWithCuesOct22shuffle1_350000.h5')
cols = df.columns
cols = cols.droplevel(level=0)
df.columns = cols


###Predict Based on event Likelihood
event = df.loc[df[('cueLight', 'likelihood')] > 0.4]
sessionStart = event.index[0]
eventFrames = event.index.tolist()
eventTimes = []
for f in eventFrames:
    time = round((f-sessionStart)/30)
    eventTimes.append(time)

eventTimes = set(eventTimes)
eventTimes = sorted(list(eventTimes))
times = countlist(eventTimes)

ts_pred = []
for t in times:
    if t[1] >= 3:
        ts_pred.append(t)

t,d = zip(*ts_pred)
t = sorted(t)
predDf = pd.DataFrame(ts_pred)
predDf.columns=['predicted_time', 'duration']



timeStamps = pd.read_excel('/d1/studies/DLC_data/OperantDLC/OperantBehavior/LeftSetC/!2020-10-25.xlsx', index_col=0, skiprows=[0,1])
mouse = timeStamps['C16-NP ']
ts_true = mouse.loc[mouse.index.str.startswith('Reward')]
ts_true.dropna(inplace=True)
ts_true = ts_true.tolist()
ts_true = ts_true[1:]
predDf['true']=ts_true

fig = plt.figure()
plt.eventplot([t, ts_true], colors=['blue', 'red'], orientation='horizontal')
fig.savefig(os.path.join(directory, 'C16_RB_10-23_Predicted_EventPlot.svg'), dpi=300)



fig1 = plt.figure(figsize=(8, 6))
ax1 = fig1.add_subplot(111, ymargin=1)
ax1.set_xlabel("Time")
ax2 = fig1.add_subplot(211, sharex=ax1, ymargin=0.5)
ax1.eventplot(t, orientation='horizontal', color='red')
ax2.eventplot(ts_true, orientation='horizontal', color='blue')
fig1.savefig(os.path.join(directory, 'C16_RB_10-23_PredictedEvents.svg'), dpi=300)



predDf.to_csv(os.path.join(directory, 'C16_NP_2020-10-11.csv'))

