#HW4 Serbin Alexander
#Set up the environment.

import requests
import zipfile
import re
import numpy as np
import pandas as pd

import matplotlib.pylab as plt
import seaborn as sns

sns.set_context('notebook')
pd.set_option('float_format', '{:6.2f}'.format)

# Ignore warnings. This is a temporary bug that should disappear in future versions of the libraries used here.
import warnings
warnings.filterwarnings("ignore")



#%%
#Problem 1
#Загрузите файл с данными опроса по адресу https://drive.google.com (используя пакет requests).

url = 'https://drive.google.com/uc?export=download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
path = 'Desktop/developer_survey_2017.zip'

response = requests.get(url)
with open(path, "wb") as file:
    file.write(response.content)
    

#%%
#прочитайте данные из двух файлов внутри полученного архива в разные наборы данных pandas
#(survey_results_public.csv с ответами и survey_results_schema.csv с вопросами).

zf = zipfile.ZipFile(path)
files = zf.namelist()

print(files)

public = pd.read_csv(zf.open(files[-2]))
schema = pd.read_csv(zf.open(files[-1]))
public.columns = [x.strip() for x in public.columns]
schema.columns = [x.strip() for x in schema.columns]
public.columns

#%%
#Сколько вопросов было в опросе?
schema.head()
print(schema.shape[0])
#%%
#Сколько разработчиков приняло участие в нем?
public.iloc[:,:2].head()
print(public.shape[0])

#%%
#Problem 2

#Сосчитайте число участников опроса по странам (колонка Country).
#Выведите 10 стран с наибольшим числом респондентов.
data = public.copy()
#index = list(['Respondent', 'Country', 'VersionControl', 'HaveWorkedLanguage'])
#data.set_index(index, inplace=True)
data.columns = [x.strip() for x in data.columns]
data1 = data[['Respondent', 'Country']].groupby(['Country']).count()
data2 = data1.sort_values(by=['Respondent'],ascending = False)
data2[:10]
#%%
#Покажите число респондентов и их долю в общем количестве. Прокомментируйте результаты.
data3 = data2/data.shape[0]
data3[:10]

#%%
#Problem 3
#не хватило времени доделать до конца
#Сосчитайте и выедите 10 стран для которых отношение числа респондентов к населению страны наибольшее?

data4 = data2[data2['Respondent'] >= 100]
print(data4)

#%%
import urllib.request
resp = urllib.request.urlopen('https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population')
html = resp.read()
#%%
import requests
url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population' 
r = requests.get(url)
with open('test.html', 'w') as output_file:
  output_file.write(r.text)
  
  
  
#%%
#Problem 4
#Покажите, какими
#системами управления версиями (колонка VersionControl) пользуются участники опроса
d = public.copy()
da = d[['Respondent', 'VersionControl']].groupby(['VersionControl']).count()
da2 = da.sort_values(by=['Respondent'],ascending = False)
da2[:10]

#%%
#Problem 5
#Пожалуйста, создайте новую переменную, в которой будет содержаться список всех
#языков, встречавшихся среди ответов.
d = public.copy()
lang = d['HaveWorkedLanguage'].dropna()
lang
languages = []

for df in lang:
    allresp = df.split(';')
    for l in allresp:
        l = l.replace(' ','') # если не сделать, то пробелы встречаются справа и слева и учитывается два раза слово
        if languages.count(l) == 0:
            languages.append(l)
            
print(languages)

#%%
#Problem 6
#Теперь сосчитайте, сколько респондентов пользуются каждым из указанных языков.
#Покажите 10 наиболее популярных. Еть ли среди них Python?

a = pd.Series(0, index = languages)# штука, которая позволяет одновременно счиатать вхождение элементов
lang = d['HaveWorkedLanguage'].dropna()
for df in lang:
    allresp = df.split(';')
    for l in allresp:
        l = l.replace(' ','') # если не сделать, то пробелы встречаются справа и слева и учитывается два раза слово
        a[l] = a[l] + 1
a2 = a.sort_values(ascending = False)
a2[:10]

#%%
#Problem 7
#Интересно, какие языки программирования популярны в разных странах? Для каждой
#страны, представленной в опросе найдите наиболее популярный язык программирования.
#Выведите его для 10 стран с наибольшим числом респондентов. (Для этого я бы реко-
#мендовал добавить в набор данных колонки бинарных переменных, соответствующими
#каждому языку программирования, и равные единице если язык перечислен в колонке
#HaveWorkedLanguage.)
#Создаем датафейм, в котором будем проставлять единицы
d = public.copy()
g = range(36625)
c = d[['Country','HaveWorkedLanguage']].dropna()
k = pd.DataFrame(np.zeros((c.shape[0],len(languages))),columns=languages)
#bigdata = pd.concat([c, k], axis=1)
#bigdata = pd.concat([c, k], axis=1, join='inner')
#bigdata = bigdata.dropna()
c.index = range(36625)
k.index = range(36625)
bigdata = pd.concat([c, k], axis=1, join='inner')



#Проставляем единицы


#%%делаю на 1000 наблюдений, а не на все. Тенденция будет сохряняться
lang = bigdata['HaveWorkedLanguage']
lang
for i in range(0, 5000):
    allresp = lang[i].split(';')
    for l in allresp:
        l = l.replace(' ','') # если не сделать, то пробелы встречаются справа и слева и учитывается два раза слово
        bigdata[l].iloc[i] = bigdata[l].iloc[i] + 1
b = bigdata.groupby('Country').sum()
#%%
b1 = b.max(axis=1)
b2 = b.idxmax(axis=1)
b3 = pd.concat([b1, b2], axis=1, join='inner')
#b3.columns
b4 = b3.sort_values(by=[0], ascending = False)
b4[:10]
b5 = b4[b4[0] != 'JavaScript']
b5
# код правильный, но работает долго. НЕ могу его поправить. Буду делать дальше.




#%%
#Problem 8
#Придумайте интересный для вас вопрос, относящийся к исследуемому набору данных,
#и ответьте на него. Оригинальность вопроса поощряется.


datat = data.copy()
dat = datat['Gender'].dropna()
s = dat[dat == 'Male']
# Количество мужчин в опросе
(s.count()/dat.count())*100
#Количество женщин
100*(dat.count() - s.count())/dat.count()
u = datat['Salary'].dropna()
y = datat['ExpectedSalary'].dropna()

plt.hist(u)
plt.hist(y)

