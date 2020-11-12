#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 15:30:42 2020

@author: smith
"""


import pandas as pd
import os
import shutil

def extractPoses(parentDirectory):
    paths = os.listdir(parentDirectory)
    folders=[]
    for path in paths:
        folder = os.path.join(parentDirectory, path)
        folders.append(folder)
        
    for fold in folders:
        files = os.listdir(fold)
        sample = fold.split('/')[-1].split('.')[0]
        basepath=fold.split('/')[:-1]
        basepath = '/'.join(basepath)
        if basepath.endswith('_filtered'):
            dtypes = ['trajectory_filtered', 'plot_filtered', 'hist_filtered', 'plot-likelihood_filtered']
        else:       
            dtypes = ['trajectory', 'plot', 'hist', 'plot-likelihood']
        for d in dtypes:
            if not os.path.exists(os.path.join(basepath, d)):
                os.mkdir(os.path.join(basepath, d))
        for file in files:
            fullpath = os.path.join(basepath, sample + '/' + file)
            f, e = os.path.splitext(fullpath.split('/')[-1])
            targpath = os.path.join(basepath, f + '/' + sample + '_' + f + e)
            shutil.copyfile(fullpath, targpath)

parentDirectory = '/d1/studies/Raspicam/MOR-Flox_Cohort3_PhysicalWithdrawal/data/plot-poses/'
extractPoses(parentDirectory)

def interpolateValues(file):
    df = pd.read_csv(file, index_col=0, skiprows=[0], header=[0,1])    
    bodyparts = set(df.columns[x][0] for x in range(len(df.columns)))
    for bp in bodyparts:
        df.loc[df[bp, 'likelihood'] < 0.4, (bp, 'x')]=None
        df.loc[df[bp, 'likelihood'] < 0.4, (bp, 'y')]=None
    df = df.interpolate(method='linear')
    df = df.dropna(how='any', axis=0)
    filename = file.strip('.csv')
    df.to_csv(filename + '_interpolated.csv')
    df.to_hdf(filename + '_interpolated.h5', key='df_with_missing')
    return(df)

file = '/d1/studies/DLC_data/Acute_Oxy_Videos/5mgkg_092820/cropped/C9_LT_5mgkg_092820DLC_resnet50_NPWSep26shuffle1_230000_filtered_annotated.csv'

df = interpolateValues(file)

directory = '/d1/studies/DLC_data/Acute_Oxy_Videos/5mgkg_092820/cropped/'
csvs=[]
        csvs.append(fullpath)

for file in csvs:
    interpolateValues(file)

files = os.listdir(directory)
for file in files:
    if file.endswith('230000.csv'):
        fullpath=os.path.join(directory, file)
        csvs.append(fullpath)

for file in csvs:
    interpolateValues(file)

directory = '/d1/studies/DLC_data/OperantDLC/analyzedVids/csvs/train/'

def trimCSVs(frames, directory):
    files = os.listdir(directory)
    saveDir = os.path.join(directory, 'trimmedCSVs/')
    for f in files:
        if f.endswith('.csv'):
            sampleName = f.split('DLC')[0]
            fullpath = os.path.join(directory, f)
            df = pd.read_csv(fullpath, index_col=0)
            df = df[:frames+2]
            df.to_csv(os.path.join(saveDir, sampleName + '_trimmed.csv'))
    
trimCSVs(27000, directory)


def h5toCSV(directory):
    files = os.listdir(directory)
    for f in files:
        if f.endswith('.h5'):
            sampleName = f.split('DLC')[0]
            n, e = os.path.splitext(f)
            fullpath=os.path.join(directory, f)
            df = pd.read_hdf(fullpath)
            df.to_csv(os.path.join(directory, n + '.csv'))


