import pandas as pd
import re
import zipfile
import requests
import io
import urllib.request
from bs4 import BeautifulSoup


url = 'https://drive.google.com/uc?export= download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
res = requests.get(url)
zf = zipfile.ZipFile(io.BytesIO(res.content))
zf.namelist()
dataFile = zf.open('survey_results_public.csv')
schemaFile =zf.open('survey_results_schema.csv')
df1 = pd.read_csv(dataFile)
df2 = pd.read_csv(schemaFile)


#Task_1
print('Task_1\n')
data = df1[['Respondent', 'Professional']]
developer = data.groupby(['Professional'])['Respondent'].count()

schema = df2[['Column', 'Question']]
question = schema['Question'].count()

print('В опросе было', question, 'вопроса.')
print('В опросе приняли участие', developer['Professional developer'], 'разработчик.')

data = data.set_index('Respondent')
schema = schema.set_index('Column')

print(data.head())
print(schema.head())


#Task_2
print('\nTask_2\n')
country = df1.groupby(['Country'])['Country'].count()
country = country.sort_values(ascending=False)
country.index.name = None
print('10 стран с наибольшим числом респондентов:', country.head(10), sep='\n')

respondent = df1['Respondent'].count()
share = country/respondent
share.index.name = None
print('\nДоля в общем кол-ве респондентов:', share.head(10), sep='\n')


#Task_3
print('\nTask_3\n')
url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
tags = soup.find_all('table')

t = tags[1].getText()
tt = re.findall('\n\n\n.+\n\s?([\w\s]+)', t)
nn = re.findall('.+\d{2},\d{3}', t)
tt = tt[:199]
ttt = []
for i in range(len(tt)):
    st = re.sub('\n[0-9]*', '', tt[i])
    st = st.strip(' ')
    nt = int(nn[i].replace(',', ''))
    ttt.append((st, nt))
population = pd.DataFrame(ttt, columns=['Country', 'Population'])
population = population.set_index('Country')

country1 = pd.DataFrame(country.copy())
country1 = country1[country1['Country'] > 100]
population1 = population[population['Population'] > 100000]

lal = pd.merge(country1, population1, right_index=True, left_index=True)
lal['Ratio'] = lal['Country']/lal['Population']
lal = lal.sort_values(by='Ratio', ascending=False)
print('10 стран для которых отношение числа респондентов к населению страны наибольшее:', lal.head(10), sep='\n')


#Task_4
print('\nTask_4\n')
control = df1.groupby(['VersionControl'])['VersionControl'].count()
control = control.sort_values(ascending=False)
control.index.name = None
print('Системы управления версиями, которыми пользуются участники опроса:', control, sep='\n')


#Task_5
print('\nTask_5\n')
myList = []
for i in df1['HaveWorkedLanguage']:
    if type(i) == str:
        a = re.findall(';?[\s]?([^;]+)', i)
        myList += a
mySet = set(myList)
languages = list(mySet)
print('Список всех языков, встречавшихся среди ответов:', languages, sep='\n')


#Task_6
print('\nTask_6\n')
myDict = {}
for i in mySet:
    c = myList.count(i)
    myDict[i] = c
mySer = pd.Series(myDict)
mySer = mySer.sort_values(ascending=False)
print('10 наиболее пополярных языков:', mySer[:10], sep='\n')


#Task_7
print('\nTask_7\n')
langS = df1[['Country', 'HaveWorkedLanguage']].copy()
for i in mySet:
    langS[i] = 0
for j in range(len(langS.index)):
    q = langS['HaveWorkedLanguage'][j]
    if type(q) == str:
        a = re.findall(';?[\s]?([^;]+)', q)
        for k in a:
            langS.loc[j, k] = 1
bum = langS.groupby('Country')[languages].sum()

bumbum = []
for i in bum.index:
    fix = bum.ix[i].sort_values(ascending=False)
    bumbu = (i, country.ix[i], fix.index[0])
    bumbum.append(bumbu)
bumbum = pd.DataFrame(bumbum, columns=['Country', 'Total', 'Popular'])
bumbum = bumbum.set_index('Country')
bumbum = bumbum.sort_values(by='Total', ascending=False)
print('Самые популярные языки (10 стран с наибольшим числом респондентов):', bumbum.head(10), sep='\n')

script = bumbum[bumbum['Popular'] != 'JavaScript'].copy()
print('\nСамый популярный язык не JavaScript:', script.head(5), sep='\n')


#Task_8
print('\nTask_8\n')
import statsmodels.api as sm

df = df1[['CareerSatisfaction', 'JobSatisfaction']]
df = df[df['CareerSatisfaction'].notnull()]
df = df[df['JobSatisfaction'].notnull()]
print(df.head())

mod  = sm.OLS(df['CareerSatisfaction'], sm.add_constant(df['JobSatisfaction']))
res = mod.fit()
print(res.summary())
