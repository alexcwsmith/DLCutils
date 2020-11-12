#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 02:04:48 2020

@author: smith
"""


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


directory = '/d1/studies/DLC_data/OperantDLC/analyzedVids/predictions/'

folders = ["/d1/studies/DLC_data/OperantDLC/analyzedVids/csvs/C9_LT",
    "/d1/studies/DLC_data/OperantDLC/analyzedVids/csvs/C10_NP",
    "/d1/studies/DLC_data/OperantDLC/analyzedVids/csvs/C12_NP",
    "/d1/studies/DLC_data/OperantDLC/analyzedVids/csvs/C12_RT",
    "/d1/studies/DLC_data/OperantDLC/analyzedVids/csvs/C13_NP",
    "/d1/studies/DLC_data/OperantDLC/analyzedVids/csvs/C13_RT",
    "/d1/studies/DLC_data/OperantDLC/analyzedVids/csvs/C14_LT",
    "/d1/studies/DLC_data/OperantDLC/analyzedVids/csvs/C14_RT",
    "/d1/studies/DLC_data/OperantDLC/analyzedVids/csvs/C15_NP",
    "/d1/studies/DLC_data/OperantDLC/analyzedVids/csvs/C15_RT",
    "/d1/studies/DLC_data/OperantDLC/analyzedVids/csvs/C16_NP",
    "/d1/studies/DLC_data/OperantDLC/analyzedVids/csvs/C16_RB"]


ctrl = ['C9_LT', 'C12_NP', 'C13_RT', 'C14_LT', 'C15_RT', 'C16_RB']
cKO = ['C10_NP', 'C12_RT', 'C13_NP', 'C14_RT', 'C15_NP', 'C16_NP']

coords_ctrl = []
coords_cKO = []

for folder in folders:
    mouse = folder.split('/')[-1]
    dirs = os.listdir(folder)
    for file in dirs:
        fullpath = os.path.join(folder, file)
        date = file.split('DLC')[0].split('-')[1:3]
        day = '_'.join(date)
        df = pd.read_csv(fullpath, index_col=0, skiprows=[0,2])
        noseX = np.mean(df['nose'])
        noseY = np.mean(df['nose.1'])
        if mouse in ctrl:
            coords_ctrl.append((mouse, day, noseX, noseY))
        elif mouse in cKO:
            coords_cKO.append((mouse, day, noseX, noseY))
        else:
            raise ValueError("Mouse not assigned to either group")
            
data_ctrl = pd.DataFrame(coords_ctrl)
data_ctrl.columns=['Mouse', 'Session', 'X', 'Y']
data_ctrl = data_ctrl.sort_values(by='Session', ascending=True)
means_ctrl = data_ctrl.groupby('Session').mean().reset_index()
fig_ctrl = means_ctrl.plot(x='Session', y=['X', 'Y'], ylabel='Mean Nose Position (Pixel)').get_figure()
fig_ctrl.savefig(os.path.join(directory, 'Control_SessionXY_means.png'))

data_cKO = pd.DataFrame(coords_cKO)
data_cKO.columns=['Mouse', 'Session', 'X', 'Y']
data_cKO = data_cKO.sort_values(by='Session', ascending=True)
means_cKO = data_cKO.groupby('Session').mean().reset_index()
fig_cKO = means_cKO.plot(x='Session', y=['X', 'Y'], ylabel='Mean Nose Position (Pixel)').get_figure()
fig_cKO.savefig(os.path.join(directory, 'cKO_SessionXY_means.png'))
   
    
distance_ctrl = data_ctrl
distance_ctrl['X'] = distance_ctrl['X'] - 110
distance_ctrl['Y'] = distance_ctrl['Y'] - 120
dist_means_ctrl = distance_ctrl.groupby('Session').mean().reset_index()
fig_dist_ctrl = dist_means_ctrl.plot(x='Session', y=['X', 'Y'], title='Distance from Active Lever').get_figure()
fig_dist_ctrl.savefig(os.path.join(directory, 'Control_DistanceFromActiveLever.svg'))

distance_cKO = data_cKO
distance_cKO['X'] = distance_cKO['X'] - 110
distance_cKO['Y'] = distance_cKO['Y'] - 120
distance_cKO.set_index('Session', drop=True, inplace=True)
dist_means_cKO = distance_cKO.groupby('Session').mean().reset_index()
fig_dist_cKO = dist_means_cKO.plot(x='Session', y=['X', 'Y'], title='Distance from Active Lever').get_figure()
fig_dist_ctrl.savefig(os.path.join(directory, 'cKO_DistanceFromActiveLever.svg'))

combined_dist = dist_means_ctrl.set_index('Session', drop=True)
combined_dist.columns=['X_ctrl', 'Y_ctrl']
combined_dist.set_index('Session', inplace=True)
dist_means_cKO.set_index('Session', inplace=True)
combined_dist['X_cKO'] = dist_means_cKO['X']
combined_dist['Y_cKO'] = dist_means_cKO['Y']
combined_dist.reset_index(inplace=True)
fig_comb_dist = combined_dist.plot(x='Session', y=['X_ctrl', 'Y_ctrl', 'X_cKO', 'Y_cKO']).get_figure()
fig_comb_dist.savefig(os.path.join(directory, 'Combined_DistanceFromLever.svg'))


distance_cKO2 = distance_cKO.drop(labels=['Mouse'], axis=1)
distance_cKO2.columns=['X_cKO', 'Y_cKO']













