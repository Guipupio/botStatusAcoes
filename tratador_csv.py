#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 22:19:43 2020

@author: pupio
"""


import pandas  as pd
import matplotlib.pyplot as plt
import numpy as np

filename = 'base_csv/relatorio_13_01_2020.csv'
ROE_MIN = 0.02
LISTA_FILTROS = ['roe', 'p/l', 'cotação', 'div.yield']
ASCENDING = [False, False, True, False]


def get_df_from_csv(filename: str, decimal= ',', sep=';', **kwargs) -> pd.DataFrame:
    return pd.read_csv(filename, decimal=decimal, sep=sep, **kwargs)

df = get_df_from_csv(filename= filename, index_col=0)

# Filtrando por ROE

# Normaliza p/l
df['p/l_normalizado'] = (df['p/l'] - df['p/l'].min())/(df['p/l'].max() - df['p/l'].min())
df['roe_normalizado'] = (df['roe'] - df['roe'].min())/(df['roe'].max() - df['roe'].min())


media = df['roe'].mean()
std = df['roe'].std()

variance = np.square(std)

f = np.exp(-np.square(df['roe'].values- media)/2*variance)/(np.sqrt(2*np.pi*variance))
plt.plot(df['roe'].values,f)

plt.ylabel('gaussian distribution')
plt.show()

df_filtrado = df[df['roe'] > ROE_MIN]
df_filtrado = df_filtrado[df_filtrado['p/l'] > 0]
df_filtrado = df_filtrado[df_filtrado['cotação'] < 60]

df_filtrado = df_filtrado.sort_values(by=LISTA_FILTROS, ascending=ASCENDING)

df_fii = df_filtrado[ df_filtrado['papel'].str.contains("11") ]
df_fii = df_fii.sort_values(by='cotação') 

    if __name__ ==  '__main__':
    pass