# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 17:03:20 2020

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
plt.rcParams.update({'font.size': 15, 'lines.linewidth':4})

# Actualización de los datos confirmados (acumulados)
c_pday = [3,4,5,5,5,5,5,6,6,7,7,7,11,15,26,41,53,82,93,118,164,203,251,316,367,405,475,585,717,848,993,1094,1215,1378,1510,1688,1890,2143,2439,2785,3181,3441,
          3844,4219,4661,5014,5399,5847,6297,6875,7497,8261,8772,9501,10544,11633,12872,13842,14677,15529,16752,17799,19224,20739,22088,
          23471,24905,26025,27634,29616,31522,33460,35022,36327,38324,40186,42595,45032,47144,49219,51633,54346,
         56594,59567,62527,65856,68620,71105,74560,78023,81400,84627,87512,90664,93435]
mx_confirmed_cases = np.array(c_pday)

def get_date_list(base, total=len(mx_confirmed_cases)):
    return [(base - datetime.timedelta(days=x)).strftime("%d-%b-%Y") for x in range(total)][::-1]

# Crear un frame de datos
mx_covid = pd.DataFrame(mx_confirmed_cases, columns=['Confirmed Cases'])

# Muertes confirmadas
d_pday = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,5,6,8,12,16,20,28,29,37,50,60,79,94,125,141,174,194,233,273,296,332,406,449,486,546,650,686,712,
          857,970,1069,1221,1305,1351,1434,1569,1732,1859,1972,2061,2154,2270,2507,2704,2961,3160,3353,
          3465,3573,3926,4220,4477,4767,5045,5177,5332,5666,6090,6510,6989,7179,7394,7633,
          8134,8597,9044,9415,9779,9930,10167]
mx_covid['Deceased'] = d_pday

# Recuperar las fechas de los casos confirmados
date_list = get_date_list(datetime.datetime.today() - datetime.timedelta(days=1))
mx_covid['Dates'] = date_list


# Guardar el frame de datos
mx_covid.to_csv('covid_mx.csv',index=False)
# mx_covid.head()


def simulate_infections_predict(incubation_days, scaling_factor, predict_days=10, base=mx_covid['Confirmed Cases']):
    added_infected = dict()
    last_day = 1
    for i, x in enumerate(base):
        if added_infected.get(i) is None:
            added_infected[i] = x
        else:
            added_infected[i] += x
        if added_infected.get(i+incubation_days) is None:
            added_infected[i+incubation_days] = x*scaling_factor 
        else:
            added_infected[i+incubation_days] += x*scaling_factor 
        last_day = i+incubation_days
    for day in range(predict_days):
        day_pinc = last_day-(incubation_days-1)
        prev_infected = added_infected[day_pinc]/8
        added_infected[last_day+1] = int(prev_infected*scaling_factor)
        last_day+=1
    return [added_infected[x] for x in range(len(added_infected))]

pred_dates=get_date_list(datetime.datetime.today() + datetime.timedelta(days=15),total=len(mx_confirmed_cases)+15)
pred_per_day=np.array(simulate_infections_predict(5, 12))
fig, ax = plt.subplots(figsize=(12,8))
ax.set_title('Predicción para los proximos {} dias.'.format(len(pred_per_day)-len(mx_covid['Confirmed Cases'])))
ax.plot(pd.to_datetime(pred_dates), pred_per_day, label='Prediccion estimada')
ax.plot(pd.to_datetime(mx_covid['Dates']), mx_covid['Confirmed Cases']*8, label='Estimaciones actuales x8')
ax.legend(loc='upper left', shadow=True, bbox_to_anchor=[0, 1], ncol=2, title="Estimacion", fancybox=True)
for line, name in zip(ax.lines, ['infectados de COVID-19 el {}'.format(pred_dates[-1])]):
    y = line.get_ydata()[-1]
    ax.annotate('{} {}'.format(y, name), xy=(1,y), xytext=(6,0), color=line.get_color(), 
                xycoords = ax.get_yaxis_transform(), textcoords="offset points",
                size=14, va="center")
fig.autofmt_xdate()

plt.show()
plt.close()




