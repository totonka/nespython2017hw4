#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 01:42:50 2018

@author: nik
"""
# HA_4
#%%
import re
import requests
import zipfile
import os
import seaborn as sns

import numpy as np
import pandas as pd
#%%
url = 'https://drive.google.com/uc?export= download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
response = requests.get(url)

path = '/Users/nik/Documents/РЭШ/3 модуль/Data_analysis/data/HA_4.zip'

response = requests.get(url)
with open(path, "wb") as file:
    file.write(response.content)
#%%
zf = zipfile.ZipFile(path)
files = zf.namelist()

print(files[-2])
#%%
survey_results_schema = pd.read_csv(zf.open(files[-1]))
survey_results_schema.columns = [x.strip() for x in survey_results_schema.columns]

survey_results_public = pd.read_csv(zf.open(files[-2]))
survey_results_public.columns = [x.strip() for x in survey_results_public.columns]

print(survey_results_schema.shape,'\n\n', survey_results_schema.dtypes)
print(survey_results_public.shape,'\n\n',survey_results_public.dtypes)

#%% Task 1
print('Number of questions %d' %np.shape(survey_results_schema.iloc[:,1])[0], '\n',
      'Number of respondents %d' %np.shape(survey_results_public.iloc[:,0])[0])
#%% Task 2
number_resp_countries = survey_results_public['Country'].value_counts()
perc_resp_countries = survey_results_public['Country'].value_counts()/survey_results_public['Country'].shape[0]
print(number_resp_countries.head(),'\n',perc_resp_countries.head())
#%% Task 3
url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
response = requests.get(url)
#%%
population_raw = pd.read_html(url)
population = population_raw[1]
#%%
pop = population.rename(columns=population.iloc[0])
pop.drop(0,axis=0,inplace=True)
#leave only countries where from number of respondents > 100
#firstly let's find unique countries
pool_countries = np.unique(survey_results_public['Country'])
#Let's calculate number of respondents from each country
counts = survey_results_public.groupby("Country").size()
#Copy our data with index 'Country'
a = survey_results_public.set_index('Country')
#Find countries where from a little respondents
loosers = [x for i,x in enumerate(counts.index.values) if counts[i]<100]
#Drop countries with little respondents
a.drop(loosers,inplace=True)
#Return old index and get back column 'Country'
a.reset_index(inplace=True)
#%%
#Create column 'Country' where clear name of counrty will be contained
pop['Country']= [pop['Country (or dependent territory)'].iloc[i].split('[')[0].split(' (')[0] for i in range(0,240)]
#Find all countries which are not in dataframe pop from Wiki 
mask = a['Country'].isin(pop['Country'])
mask = [not i for i in mask]
#There are countries which are not in Wiki table
missed = set(a['Country'][mask])
#Now we need to replace Russia and Slovakia in Russian Federation and Slovak Republic pop['Country']
pop['Country'].replace(to_replace = ['Russia', 'Slovakia'], value=['Russian Federation','Slovak Republic'],inplace=True)
#Change index in pop on the country
pop.set_index('Country', inplace=True)
#Let's make DataFrame with population to merge it with another DataFrame with number of respondents
df_counts = counts.to_frame()
df_pop = pop['Population'].to_frame()
t = pd.merge(df_pop,df_counts, how='inner', left_index=True, right_index=True)
#Let's rename column with counts
t.rename(columns={0:'Counts'},inplace=True)
#Change the type of population data
t['Population'] = t['Population'].astype(str).astype(int)
t['Ratio'] = t.eval('Counts / Population')
t['Ratio'] = t['Ratio'].map(lambda x: '%11.6f' % x)
t.sort_values('Ratio', inplace=True,ascending=False)
loosers = [i for i,c in zip(t.index.values,t['Counts']) if c<100]
t.drop(loosers,inplace=True)
t.head(10)
#%% Task 4
counts_versions = survey_results_public.groupby("VersionControl").size()
counts_versions.sort_values(ascending=False)
#%% Task 5
s = list(survey_results_public["HaveWorkedLanguage"].str.split('; ', expand=True).stack().unique())
print(s)
#%% Task 6
s_counts = survey_results_public["HaveWorkedLanguage"].str.split('; ', expand=True).stack().value_counts()
s_counts.head(10)
#%% Task 7
languages = survey_results_public.HaveWorkedLanguage.apply(lambda x: str(x).split("; "))
#for lang in s:
np.where(languages.isin(s))
#%% Task 8
a = survey_results_public.set_index('Country')
sns.boxplot(x=t.index[:5],y=t['Population'][:5], linewidth=.5)
