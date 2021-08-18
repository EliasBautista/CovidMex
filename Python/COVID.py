# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 23:04:41 2020

@author: Elias
"""



import matplotlib.pyplot as plt
import geopandas as gpd
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib
import datetime , json5, glob2, unidecode
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
plt.rcParams.update({'font.size': 17, 'lines.linewidth':4})


path = 'Mexico_States.shp'
data = gpd.read_file(path)
data['NAME'] = data['NAME'].str.lower()

df = pd.read_csv('casos_confirmados.csv')
df = df.dropna()
df.head()
center_states = ['distrito federal', 'queretaro', 'puebla', 'mexico', 'morelos', 'hidalgo','tlaxcala']
cases_per_state = dict()
for state in df.State.unique():
    key = state.lower()
    if key == 'ciudad de mexico':
        key = 'distrito federal'
    if key == 'queretaro':
        key = 'querétaro'
    cases_per_state[key] = len(df[df['State'] == state])

data['CPSTATE']= data['NAME'].map(cases_per_state)
data['coords'] = data['geometry'].apply(lambda x: x.representative_point().coords[:])
data['coords'] = [coords[0] for coords in data['coords']]
center_mx = data.loc[data['NAME'].isin(center_states)]

data['CPSTATE'] = data['CPSTATE']*8
center_mx = data.loc[data['NAME'].isin(center_states)]

fig, ax1 = plt.subplots(figsize=(25,15))

left, bottom, width, height = [0.5, 0.55, 0.25, 0.25]
ax2 = fig.add_axes([left, bottom, width, height])

data.plot(ax=ax1, column='CPSTATE', cmap='Reds',edgecolor="black", legend=True, legend_kwds={'label': "Official confirmed COVID-19 cases", 'shrink':0.5})
for idx, row in data.iterrows():
    if row['NAME'] not in center_states:
        ax1.annotate(s=row['CPSTATE'], xy=row['coords'],horizontalalignment='center')
        
center_mx.plot(ax=ax2, column='CPSTATE', cmap='Reds',edgecolor="black", legend=False)
for idx, row in center_mx.iterrows():
    ax2.annotate(s=row['CPSTATE'], xy=row['coords'],horizontalalignment='center')
    
ax1.axis('off')
ax2.axis('off')
ax1.legend(fontsize=8)
plt.show()
plt.close()