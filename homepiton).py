# -*- coding: utf-8 -*-
"""
Редактор Spyder

Это временный скриптовый файл.
"""
import re
import requests

import matplotlib.pylab as plt
import numpy as np
import pandas as pd

##Задание1
import requests, zipfile, io
pd.set_option('float_format', '{:6.5f}'.format)
np.set_printoptions(precision=3, suppress=True)
zip_file_url = 'https://drive.google.com/uc?export= download&id=0B6ZlG_Eygdj-c1kzcmUxN05VUXM'
r = requests.get(zip_file_url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()
z.namelist()

file_pu = z.open('survey_results_public.csv')
file_sc =z.open('survey_results_schema.csv')
df_pu = pd.read_csv(file_pu)
df_sc = pd.read_csv(file_sc, header = 0)

data = df_pu.set_index('Respondent')
schema = df_sc.set_index('Column')
schema.head()
data.iloc[:,:].head()

len(data)
len(schema)

##Задание2
print(data.Country.value_counts().head(10))

print((data.Country.value_counts()/len(data)).head(10))

##Задание3

url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population' 
response = requests.get(url) 
wiki = pd.read_html(response.content)[1] 
wiki.columns = wiki.iloc[0] 
wiki = wiki.reindex(wiki.index.drop(0)) 
wiki.head() 

for i in range (1,len(wiki)): 
    wiki['Country (or dependent territory)'][i] = re.sub(r'\s\(.*\)', "", wiki['Country (or dependent territory)'][i]) 

for i in range (1,len(wiki)): 
    wiki['Country (or dependent territory)'][i] = re.sub(r'\[.*\]', "", wiki['Country (or dependent territory)'][i]) 

wiki1 = wiki.copy() 
wiki2 = wiki1.rename(columns = {'Country (or dependent territory)':'Country'}) 
wiki2 = wiki2.set_index('Country') 

our = pd.DataFrame(data.Country.value_counts()) 
wiki3 = wiki2.Population

ourr = our[our.Country > 100] 
jo = pd.concat([ourr, wiki3], axis=1, join='inner') 
jo['Population'] = jo['Population'].astype(int) 
jo['Ratio'] = jo['Country']/jo['Population'] 
pd.set_option('float_format', '{:6.6f}'.format) 
 
ans = jo.sort_values(['Ratio'], ascending=[False]) 
print(ans.head(10))

##Задание4
print(data.VersionControl.value_counts())

##Задание5
#долго думает (1min)
x=df_pu.HaveWorkedLanguage
xx=x.dropna()
xx=xx.reset_index (drop=True)
y=np.array([])

for i in range(len(xx)):
    result=re.split(r'; ', xx[i])
    if set(y)&set(result)!=set(result):
        y=np.append(y, result, axis= 0)
languages=list(set(y))    
print(languages)    

##Задание6
##работает, но очень долго (20min)

res=pd.DataFrame(columns=('lang','coun'))    

for i in range(len(xx)):
    result=re.split(r'; ', xx[i])
    for j in range(len(result)):
        res=res.set_value(len(res),'lang',result[j])
print(res.lang.value_counts().head(10))            

##Задание7
#я бы дальше склеяла в одну таблицу... 
#но даже для одной страны капец как долго считается (10 мин)
final=pd.DataFrame(columns=('lang','coun'))

coun10=data.Country.value_counts().head(10)
v=list(coun10.index)
for k in range(len(v)):
    z=data.HaveWorkedLanguage[data.Country==v[k]]
    zz=z.dropna()
    zz=zz.reset_index (drop=True)
    yy=np.array([])

    for i in range(len(zz)):
        result=re.split(r'; ', zz[i])
        for j in range(len(result)):
            final=final.set_value(len(final),'lang',result[j])
    print(final.lang.value_counts().head(1))

##Задание8
#Какой процент мужчин и женщин профессиональных разработчиков абсолютно счастлив на работе?
fem = data[data.Gender=='Female']
fp=fem[fem.Professional=='Professional developer']
fp10=fp[fp.JobSatisfaction==10]  

m = data[data.Gender=='Male'] 
mp= m[m.Professional=='Professional developer']
mp10=mp[mp.JobSatisfaction==10]

a=len(fp10)/len(fp)*100
b=len(mp10)/len(mp)*100
print(round(a,2),'% женщин и ',round(b,2),'% мужчин')
