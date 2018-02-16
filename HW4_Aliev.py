#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 19:43:15 2018

@author: khankishialiev
"""
#%%
import re
import requests
import zipfile
import os

import numpy as np
import pandas as pd

pd.set_option('float_format', '{:6.6f}'.format)
#%%
url = 'https://drive.google.com/uc?export= download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
response = requests.get(url)
#%%
fnames = re.findall('zip\/(.*?\.zip)', str(response.content))
print(fnames)
#%%
path = './data1/'
os.makedirs(path, exist_ok=True)

filepath = path + 'ddd.zip'
if not os.path.isfile(filepath):
    response = requests.get(url)
    with open(filepath, "wb") as file:
        file.write(response.content)
#%%
zf = zipfile.ZipFile(path + 'ddd.zip')
#%%
data = pd.read_csv(zf.open('survey_results_public.csv'))
schema = pd.read_csv(zf.open('survey_results_schema.csv'))
#%%
#Task1
print('Вопросов было ',schema.shape[0]-1)
#%%
count = 0
for i in range(len(data['Professional'])):
    if data['Professional'][i] == 'Professional developer':
        count += 1
print('В опросе приняло участие столько девелоперов: ', count)
#%%
#Task2
pd.set_option('float_format', '{:6.6f}'.format)
countries = dict.fromkeys(data['Country'], 0)
for i in range(len(data['Country'])):
    countries[data['Country'][i]] += 1
df = pd.DataFrame({
        'Country': list(countries.keys()),
        'Count': list(countries.values())
        })
df1 = df.sort_values(['Count'], ascending = False)   
print(df1[:10])

respondent_count = data.shape[0]
df2 = df1[:10].copy()
df2['Count'] = df2['Count'] / respondent_count
print(df2)
#%%
#Task4
a = data['VersionControl'].dropna()
versions = dict.fromkeys(a, 0)
for i in range(len(data['VersionControl'])):
    if data['VersionControl'][i] == data['VersionControl'][i]:
        versions[data['VersionControl'][i]] += 1
        
df = pd.DataFrame({
        'Count': list(versions.values()),
        'VersionControl': list(versions.keys())
        })
df1 = df.sort_values(['Count'], ascending = False) 
print(df1)
#%%
#Task5
languages = {}
for i in range(len(data['HaveWorkedLanguage'])):
    if data['HaveWorkedLanguage'][i] == data['HaveWorkedLanguage'][i]:
        newkeys = data['HaveWorkedLanguage'][i].split(sep = ';')
        for i in range(len(newkeys)):
            newkeys[i] = newkeys[i].strip()
            languages[newkeys[i]] = 0
         
a = list(languages.keys())
print(a)

#%%
#Task6
for i in range(len(data['HaveWorkedLanguage'])):
    if data['HaveWorkedLanguage'][i] == data['HaveWorkedLanguage'][i]:
        newkeys = data['HaveWorkedLanguage'][i].split(sep = ';')
        for i in range(len(newkeys)):
            newkeys[i] = newkeys[i].strip()
            languages[newkeys[i]] += 1

df = pd.DataFrame({
        'Language': list(languages.keys()),
        'Count': list(languages.values())
        })
    
df1 = df.sort_values(['Count'], ascending = False)
print(df1[:10])
#%%
newcols = list(languages.keys())
for i in range(len(newcols)):
    df[newcols[i]] = 0
#%%
#for i in range(len(data['HaveWorkedLanguage'])):
   # if data['HaveWorkedLanguage'][i] == data['HaveWorkedLanguage'][i]:
    #    newkeys = data['HaveWorkedLanguage'][i].split(sep = ';')
     #   for i in range(len(newkeys)):
      #      newkeys[i] = newkeys[i].strip()
       #     df[newkeys[i]][i] += 1
            
#%%
#Task 8
В какой стране наибольшее количество самообучившихся, которые знают Питон. Вывести топ 10.
