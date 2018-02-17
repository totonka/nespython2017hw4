# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 12:25:44 2018

@author: Alexander
"""
#%%
import requests
import zipfile
import io
import numpy as np
import pandas as pd

import matplotlib.pylab as plt
import seaborn as sns



#%%
#1
"""Загрузите файл с данными опроса по адресу https://drive.google.com/uc?export=
download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM (используя пакет requests), и прочитайте дан-
ные из двух файлов внутри полученного архива в разные наборы данных pandas
(survey_results_public.csv с ответами и survey_results_schema.csv с вопросами). Сколь-
ко вопросов было в опросе? Сколько разработчиков приняло участие в нем?"""

url = 'https://drive.google.com/uc?export= download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM' 
zip = requests.get(url) 
my_zip = zipfile.ZipFile(io.BytesIO(zip.content)) 
my_zip.namelist() 
data_answ = my_zip.open('survey_results_public.csv') 
data_question =my_zip.open('survey_results_schema.csv')
dfa = pd.read_csv(data_answ, header=0)
dfq = pd.read_csv(data_question, header=0)

#dfa = pd.read_csv('survey_results_public.csv') #Ответы
#dfq = pd.read_csv('survey_results_schema.csv') #Вопросы

#Считаем кол-во вопросов,то бишь кол-во строк в базе с вопросами
dfq.iloc[:,:2]
#или
len(dfa.columns)
#154
#Получим кол-во респондентов
dfa.iloc[:,:2]
#51392


#%%
#2
"""Сосчитайте число участников опроса по странам (колонка Country). Выведите 10 стран
с наибольшим числом респондентов. Покажите число респондентов и их долю в общем
количестве. Прокомментируйте результаты."""

#dfc = dfa.groupby('Country')
country = dfa['Country'].copy()
print(country)
#country.groupby('Country')
dfa.groupby('Country').Country.count()
country_sorted = country.value_counts(sort=True, ascending=False)
country_sorted.head(10)
#United States         11455
#India                  5197
#United Kingdom         4395
#Germany                4143
#Canada                 2233
#France                 1740
#Poland                 1290
#Australia               913
#Russian Federation      873
#Spain                   864




#%%
#3
"""Что если число участников определяется просто населением стран, в которых они живут?
Сосчитайте и выедите 10 стран для которых отношение числа респондентов к населению
страны наибольшее? Для определенности население стран мира возьмите на страничке
https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population. Для
простоты при объединении наборов данных ограничьтесь странами, число участников в
которых не меньше ста. Прокомментируйте результаты."""


#url = 'https://https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population' 
#response = requests.get(url) 
#wiki = pd.read_html(response.content)[1]

#url = 'https://https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
#html = urllib.request.urlopen(url).read()
#soup = BeautifulSoup(html, 'html.parser')

#r = requests.get(url, allow_redirects=True)
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib

url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'

html = urllib.request.urlopen(url).read() 
soup = BeautifulSoup(html, 'html.parser')
table =soup.find_all('table')
population = pd.read_html(str(table[1]))
print(population)
#population = pd.DataFrame(population)
Splitpop = population[population.Population].str.split('  ', expand=True)

#soup = BeautifulSoup(data)
#%%


#response = urllib.request.urlopen('https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population')
#html = response.read()
#soup = BeautifulSoup(html)
#
#table = soup.find("table", {"class" : "detail-char"})







#%%
#4
"""Мы с вами освоили Git в качестве системы управления версиями. Покажите, какими
системами управления версиями (колонка VersionControl) пользуются участники опроса
(упорядочите их по количеству ответов)."""
#Dataframe.groupby('Country').Country.count()
version = dfa['VersionControl'].copy()
print(version)
#version.groupby('VersionControl')
dfa.groupby('VersionControl').VersionControl.count()#Можно так
version_sorted = version.value_counts(sort=True, ascending=False, dropna=True)#И так
version_sorted.head(10)

#Git                                            21266
#Subversion                                      2790
#Team Foundation Server                          2255
#I don't use version control                     1468
#I use some other system                          924
#Zip file back-ups                                609
#Mercurial                                        591
#Copying and pasting files to network shares      510
#Visual Source Safe                               196
#Rational ClearCase                               121



#%%
#5
"""Теперь посмотрим какие языки программирования популярны. В колонке HaveWorkedLanguage
перечислены языки, которыми респондент недавно пользовался. Проблема в том, что мож-
но было отмечать несколько вариантов ответа (они разделены точкой с запятой). Пожалуйста,
создайте новую переменную, в которой будет содержаться список всех
языков, встречавшихся среди ответов."""

dfa['HaveWorkedLanguage'].head()

raw_dfasynt=dfa['HaveWorkedLanguage'].str.split(';', expand=True)
dfasynt=raw_dfasynt.dropna()
lang=np.unique(dfasynt)
lang=list(lang)
print(lang)
#df1=df[df.stolb.notnull()]



#%%
#6






#%%
#7









#%%
#8
"""Придумайте интересный для вас вопрос, относящийся к исследуемому набору данных,
и ответьте на него. Оригинальность вопроса поощряется."""


"""Для какого количества респондентов программирование является профессиональной деятельностью,для кого-хобби?"""


dfa.groupby('ProgramHobby').ProgramHobby.count()
hobby_sorted = dfa.ProgramHobby.value_counts(sort=True, ascending=False)
hobby_sorted








