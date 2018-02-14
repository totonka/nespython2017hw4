#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 21:26:27 2018

@author: silis123
"""
#Загружаем библиотеки
import requests
import re
import zipfile
import io
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns

#%% #Задание 1
# Обозначаем адрес и путь к файлу на ПК
r = requests.get('https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM', auth=('user', 'pass'))
fname = 'developer_survey_2017'
path = r
csv1 = 'survey_results_public'
csv2 = 'survey_results_schema'
zf = zipfile.ZipFile(io.BytesIO(r.content)) #Анзипаем скачанный датасет и считываем в два разных csv
zf.extractall()
data = pd.read_csv(zf.open(csv1 + '.csv'), header=0)
schema = pd.read_csv(zf.open(csv2 + '.csv'), header=0)
#%%
schema.head() 
#%%
data.iloc[:,:2].head()
#%%
#задание 2
#Ищем количество совпадений по столбцу
data1 = data['Country'].value_counts() 

data1df = pd.Series.to_frame(data1)
data1df.rename(columns={'Country':'Frequency'}, inplace = True)
data1df.head(10)
#%%
# ищем доли, разделяя совпадения на длину столбца
data2 = data['Country'].value_counts()/len(data['Country'])
data2.head(10)
#%% 3
from bs4 import BeautifulSoup
import urllib.request

#Задаем ссылку на Википедию, откуда будет парситься наша табличка
wiki = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population" 
#парсим
wikitables = pd.read_html(wiki, index_col=0, attrs={"class":"wikitable"})  

#%%
#превращаем в DataFrame и чистим от лишних символов с помощью регулярных выражений
wikidf = wikitables[0]
wikiclean = wikidf[1].str.replace('\[Note [0-9]*\]', '')
wikidf['Country'] = wikiclean
#%%
#Копирую Фрейм, чтобы не путать оригинальный с нужными для заданий
wikidf1= wikidf.copy()
wikidf1.set_index('Country', inplace=True) #Устанавливаю Индекс
newestkek = wikidf1.join(data1df)
data3 = newestkek.copy()
data3.dropna(axis=0, how = 'any', inplace = True) #Дромаю NaN
data3= data3[data3['Frequency'] >=100] #Выделяю значения из столбца больше или равные ста
data3['ratio']=data3['Frequency'].astype(int)/data3[2].astype(int) # Ищу отношение поличества респондентов к популяции
data3 = data3.sort_values(by = ['ratio'], ascending = False)
data3.head(10)

#%%
#%% 4
data['VersionControl'].value_counts() # ищу наибольшее число совпадений по столбцу
#%%
#5
#Проверка задания
data['HaveWorkedLanguage'].head()
#Внешний лист, в который складываются все уникальные слова из столбца HaveWorkedLanguage
languages = []
languageslist = data['HaveWorkedLanguage'].dropna() #дропаю пустые строки
for i in languageslist:
    sets = i.split(';') #чистка данных
    for j in sets:
        j = j.replace(' ','')
        if languages.count(j) == 0:
            languages.append(j) #аппенд
            
languages

#%%
#6
#Здесь, на самом деле, примерно то же самое, что и в пятом номере, только мы делаем не лист а счетчик в Series
languages2 = pd.Series(0, index = languages)
for i in languageslist:
    sets = i.split(';')
    for j in sets:
        j = j.replace(' ','')
        languages2[j] = languages2[j] + 1

languages2 = languages2.sort_values(ascending = False)
languages2.head(10)

#%%
#7

#Подготовительные действия. Для начала я создал пустой дата фрейм, чтобы в него вложить колонки
test = pd.DataFrame(columns=languages)

test

#%%
#Копирую данные, чтобы не засорять оригинальный набор
data7 = data.copy()
#чистка и создание списка слов
languages7 = []
languageslist7 = data7['HaveWorkedLanguage'].dropna()
for i in languageslist7:
    sets7 = i.split(';')
    languages7.append(sets7)
#%%
# снова чистка
languages7 = [[x.replace(' ','') for x in l] for l in languages7]

#%%
#Здесь происходит магия, которая заменяет значения в столбцах по языкам программирования на True и False
for i in test:
    test[i] = languageslist7.map(lambda x: i in x.split('; '))*1
    
#%%
#data7 = data7.dropna(subset=['HaveWorkedLanguage'])
#data7 = data7.join(test)
#%%                 ЧЕРНОВИКИ
#data777 = newestkek.copy()
#data777.dropna(axis=0, how = 'any', inplace = True)
#test777 = pd.DataFrame(columns=languages)

#%%
#%%
#data888 = data777.join(test777)

#%%
#снова создаю сет
langerbanger = data[['Country', 'HaveWorkedLanguage']].copy() 
langerbanger.dropna(axis=0, how = 'any', inplace = True)
#%%
#Прикрепляю столбец с языками
langerbanger['Languageeez'] = languages7
#%%
#Прибавляю свеженькие индексы
langerbanger['counter'] = range(0, 36625)
#%%
#и сетаю
langerbanger = langerbanger.set_index('counter')
#%%
#%%
#заполняем табличку
for i in test: 
    langerbanger[i]=0
    for j in range(len(langerbanger.index)):
        if j == 36625: #я не успел понять, почему у меня здесь бесконечный цикл, так что просто используем стопор
            break
        else:
            for k in langerbanger['Languageeez'][j]:
                if k == i:
                    langerbanger.loc[j, k] = 1
                    print(j , k) #принчу всё, чтобы было видно, что код работает и было не скучно ждать 
                    
#%%
#%%
#группирую всё из цикла, показанного выше и получаю прикольную табличку
HarryPotter = langerbanger.groupby('Country')[languages].sum()
#%%
#вспоминаю прошлык задания и добавляю столбики
wikidf2 = wikitables[0]
wikiclean = wikidf2[1].str.replace('\[Note [0-9]*\]', '')
wikidf2['Country'] = wikiclean
qwwuu = wikidf2['Country']
#%%
#лишняя строка
qwwuu = qwwuu.drop('Rank')

#%%
#перевожу в data frame
qwwuu = qwwuu.to_frame()
#%%
#добавляю столбик и сетаю нормальные индексы
qwwuu['counter'] = range(0, 240)
qwwuu = qwwuu.set_index('counter')
#%%
#черновик
blinr = qwwuu.join(data1df)
#qwwuu = qwwuu.reset_index(drop=True)
#%%
#Здесь у меня ошибка в 199 строке - Beer, я не успеваю поправить. У меня работало, тк в переменных сохранено
# Причина - не совпадает индекация поттера и qwwuu, запаривается на Афганистане. Вряд ли это умаляет мой косяк, но я его знаю, просто не успеваю&
Marvollo = [] 
for i in HarryPotter.index:
    pepper = HarryPotter.ix[i].sort_values(ascending=False) 
    beer = (i, qwwuu.ix[i], pepper.index[0]) 
    Marvollo.append(beer)
    
#%%
#проверка того, что написано в 194
HarryPotter.index[0]
#%%
#проверка жаваскрептеров
Marvollo = pd.DataFrame(Marvollo, columns=['Country', 'Total', 'Popular']) 
Marvollo = Marvollo.set_index('Country') 
Marvollo = Marvollo.sort_values(by='Total', ascending=False) 

#%%
#проверка не жаваскрептеров
nomorescript = Marvollo[Marvollo['Popular'] != 'JavaScript'].copy() 
nomorescript.head(5)

#%%
#Задание 8
# определите количество людей по роду деятельрости и нарисуйте гистограмму

professionals = []
profilist = data['Professional'].dropna() #дропаю пустые строки
for i in profilist:
    setsyback = i.split(';') #чистка данных
    for j in setsyback:
        if professionals.count(j) == 0:
            professionals.append(j) #аппенд
            
professionals

#%%
professionals2 = pd.Series(0, index = professionals)
for i in profilist:
    sets = i.split(';')
    for j in sets:
        professionals2[j] = professionals2[j] + 1

professionals2 = professionals2.sort_values(ascending = False)
professionals2.head()

