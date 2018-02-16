# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 10:12:05 2018

@author: ashigoreva
"""

#%%
import re
import requests
import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import zipfile, io

#%%
pd.set_option('float_format', '{:6.5f}'.format)
np.set_printoptions(precision=3, suppress=True)

#%%
#1
url = 'https://drive.google.com/uc?export= download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
zip = requests.get(url)
my_zip = zipfile.ZipFile(io.BytesIO(zip.content))
my_zip.namelist()


file1 = my_zip.open('survey_results_public.csv')
file2 =my_zip.open('survey_results_schema.csv')

data0 = pd.read_csv(file1,  header = 0)
schema0 = pd.read_csv(file2, header = 0)

data = data0.copy()
schema = schema0.copy()

data = data.set_index('Respondent')
schema = schema.set_index('Column')
# input
data.iloc[:,:1].head()
schema.head()
# Сколько вопросов было в опросе?

print(len(data.columns))
#  Сколько разработчиков приняло участие в нем?
data.Professional.value_counts()
print(data.Professional.value_counts()['Professional developer'])


data.Professional.value_counts().plot(kind='barh')

#%%
#2
# absolute
print(data.Country.value_counts()[:10])
data.Country.value_counts()[:10].plot(kind='bar')

# percentage
# Method 1
data_by_country = data.Country.value_counts()
data_by_country_freq = (data_by_country/data_by_country.sum())[:10]
print(data_by_country_freq)
# Method 2
print(data.Country.value_counts(normalize=True)[:10])

#%%
#3
# Парсинг и обработка таблицы из Википедии
url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
response = requests.get(url)
wiki = pd.read_html(response.content)[1]
wiki.columns = wiki.iloc[0]
wiki = wiki.reindex(wiki.index.drop(0))
wiki.head()

# чистим столбик Страны от лишних символов (для конката)
for i in range (1,len(wiki)):
    wiki['Country (or dependent territory)'][i] = re.sub(r'\s\(.*\)', "", wiki['Country (or dependent territory)'][i]) 
    
for i in range (1,len(wiki)):    
    wiki['Country (or dependent territory)'][i] = re.sub(r'\[.*\]', "", wiki['Country (or dependent territory)'][i])

wiki.head()

# Делаем столбик Страны индексом 
wiki1 = wiki.copy()
wiki2 = wiki1.rename(columns = {'Country (or dependent territory)':'Country'})
wiki2 = wiki2.set_index('Country')

# Что мы имеем: new_table (с агрегированными значениями количества участников по странам)
# и таблицу wiki с населением стран
new_table = pd.DataFrame(data_by_country)
wiki3 = wiki2.Population
wiki3.head()


# Самая веселая часть - конкат с условием
new_table1 = new_table[new_table.Country > 100]
result = pd.concat([new_table1, wiki3], axis=1, join='inner')

# Считаем новую колонку Ratio
result.dtypes
result['Population'] = result['Population'].astype(int)
result['Ratio'] = result['Country']/result['Population']
pd.set_option('float_format', '{:6.6f}'.format)
result.head()

# Сортируем по убыванию
final = result.sort_values(['Ratio'], ascending=[False])
print(final.head(10))

#%%
#4 value_counts сам уже в порядке убывания делает
print(data.VersionControl.value_counts())

#%%
#5
# убираем строки с NaN
data.head()
lang = data['HaveWorkedLanguage']
lang = lang[lang.notnull()]
len(lang)

# сплитуем столбец, чтобы его победить
for i in lang.index:
    lang[i] = lang[i].split("; ")

print(lang.head())

# находим уникальные значения языков
languages = []
for i in lang:
        for j in i:
            if not j in languages:
                languages.append(j)
                
print(languages, '\n',len(languages))               

#%%
#6
lang1 = lang.copy()
lang = pd.DataFrame(lang)
lang1 = pd.DataFrame(lang1)

# создаем столбцы для каждого языка:
for x in languages:
    lang1[x] = 0
    

# заполняем столбцы с языками/ смогла сделать только True/False
# P.S. цикл считает долго (около 23 минут). Как раз можно выпить чаёк с лимоном
    
    #порядок языков:
#['Swift', 'JavaScript', 'Python', 'Ruby', 'SQL', 'Java', 'PHP', 'Matlab', 'R', 
# 'Rust', 'CoffeeScript', 'Clojure', 'Elixir', 'Erlang', 'Haskell', 'C#', 
# 'Objective-C', 'C', 'C++', 'Assembly', 'VB.NET', 'Perl', 'Scala', 'F#', 
# 'TypeScript', 'Lua', 'VBA', 'Groovy', 'Go', 'Smalltalk', 'Visual Basic 6', 
# 'Common Lisp', 'Dart', 'Julia', 'Hack']
    
for x in languages:
    for i in lang1.index: 
        lang1.loc[i,'x']=(x in lang1.loc[i,'HaveWorkedLanguage'])
        print(x,i)


df1 = []
for x in languages:  
    a = (x, lang1[x].sum())
    df1.append(a)
df1 = pd.DataFrame(df1, columns=['Language','Number'])
print(df1)

# Сортируем по убыванию
df2 = df1.sort_values(['Number'], ascending=[False])
print(df2.head(10))

#%%
#7
data_new = data[data['HaveWorkedLanguage'].notnull()]

cosmos = pd.concat([data_new, lang1], axis=1, join='inner')
cosmos.head()

# формируем датасет с удобными столбиками
languages1 = ['Country'] + languages
cosmos = cosmos[languages1]
cosmos.head()

g1 = cosmos.groupby( ["Country"] ).sum()
g1.head()

# все данные, из которых будем выбирать по условиям
cosmos1 = pd.concat([new_table, g1], axis=1, join='inner')
cosmos1.head()

# находим самые популярные языки
cosmos1['Popular language'] = 'A'
for i in range(len(cosmos1)):
    cosmos1['Popular language'][i] = cosmos1.iloc[i,1:-1].sort_values(ascending=[False]).index[0]
result3 = cosmos1[['Country','Popular language']]
print(result3[:10])   

# Страны с наиб числом участников, где JavaScript не является популярным
result4 = result3[result3['Popular language']!='JavaScript']
print(result4[:5])


#%%
#8
# Посчитать количество стран. в которых 
# средний показатель CareerSatisfaction больше среднего показателя JobSatisfaction
data.head()
list(data.columns.values)

# Выбираем нужные колонки и избавляемся от nan
data_for_analysis = data[['Country','CareerSatisfaction','JobSatisfaction']]  
data_for_analysis = data_for_analysis[data_for_analysis['CareerSatisfaction'].notnull()]
data_for_analysis = data_for_analysis[data_for_analysis['JobSatisfaction'].notnull()]
data_for_analysis.head(15)

# находим средние показатели по странам
grouped_data = data_for_analysis.groupby( ["Country"] ).mean()
grouped_data.head(15)
len(grouped_data)

results5 = grouped_data['CareerSatisfaction'][grouped_data['CareerSatisfaction']>grouped_data['JobSatisfaction']]
print(len(results5))


















    