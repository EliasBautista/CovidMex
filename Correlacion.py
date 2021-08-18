# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 19:46:44 2020

@author: Elias
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("covid_mx.csv")
df.head()
df.corr(method="pearson")
df.corr()
plt.matshow(df.corr())


plt.subplots(figsize=(15,7))
plt.plot(df["Confirmed Cases"],df["Deceased"])
plt.ylabel("Fallecimientos")
plt.xlabel("Deceased")
plt.show()
plt.close()

dd = pd.read_csv("casos_confirmados.csv")
dd.head()
df.corr(method="pearson")
df.corr()
plt.matshow(df.corr())


plt.subplots(figsize=(15,7))
plt.plot(df["Confirmed Cases"],df["Deceased"])
plt.ylabel("Fallecimientos")
plt.xlabel("Deceased")
plt.show()